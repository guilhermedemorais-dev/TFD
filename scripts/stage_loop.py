"""Opt-in stage evidence checks; declarations do not authenticate reading or people."""

import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit


BUNDLE = Path(__file__).resolve().parents[1]
FALLBACK_STATUSES = {"INDEX_MISSING", "INDEX_STALE", "INDEX_INVALID", "UNAVAILABLE", "GRAPHIFY_UNAVAILABLE"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_json(event, field, root, require_file):
    path = require_file(event.get(field), root)
    if digest(path) != event.get(field + "_sha256"):
        raise ValueError(f"stage loop: {field} hash mismatch")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"stage loop: {field} must be an object")
    return value


def artifact_bindings(artifacts, hashes):
    return {key: {"path": path, "sha256": hashes[key]} for key, path in artifacts.items()}


def require_knowledge(knowledge, root, require_file, *, skip_paths=()):
    if not isinstance(knowledge, dict):
        raise ValueError("stage loop: own knowledge record required")
    navigation = knowledge.get("navigation")
    if not isinstance(navigation, dict) or any(not nonempty(navigation.get(key))
            for key in ("method", "query", "evidence", "sha256", "status")):
        raise ValueError("stage loop: navigation requires query, actual status and hashed evidence")
    method, status = navigation["method"], navigation["status"]
    if method not in {"graphify", "lexical", "reuse"}:
        raise ValueError("stage loop: unsupported navigation method")
    nav_file = require_file(navigation["evidence"], root)
    if digest(nav_file) != navigation["sha256"]:
        raise ValueError("stage loop: navigation evidence changed")
    nav_evidence = json.loads(nav_file.read_text(encoding="utf-8"))
    if not isinstance(nav_evidence, dict) or status not in (nav_evidence.get("status"), nav_evidence.get("runtime_status")):
        raise ValueError("stage loop: navigation status must match observed evidence")
    if method == "lexical" and (status not in FALLBACK_STATUSES or not nonempty(navigation.get("reason"))):
        raise ValueError("stage loop: lexical fallback needs unavailable/stale status and reason")
    if method == "graphify" and status != "GRAPHIFY":
        raise ValueError("stage loop: record actual Graphify status")
    if method == "reuse":
        if status != "VERIFIED" or any(not nonempty(navigation.get(key)) for key in
                ("original_navigation", "original_navigation_sha256", "revision", "applicability")):
            raise ValueError("stage loop: reuse requires original navigation, version and current applicability")
        if digest(require_file(navigation["original_navigation"], root)) != navigation["original_navigation_sha256"]:
            raise ValueError("stage loop: original navigation changed")
    sources = knowledge.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("stage loop: canonical sources required")
    for source in sources:
        if not isinstance(source, dict) or any(not nonempty(source.get(key)) for key in
                ("path", "sha256", "revision", "locator", "observation")) or source.get("status") != "VERIFIED":
            raise ValueError("stage loop: canonical source requires verified version, section and observation")
        kind = source.get("kind", "project")
        if kind not in {"project", "bundle", "remote"}:
            raise ValueError("stage loop: canonical source kind must be project, bundle or remote")
        if kind == "remote":
            origin = source.get("origin")
            parsed = urlsplit(origin) if nonempty(origin) else None
            if (parsed is None or parsed.scheme != "https" or not parsed.hostname or parsed.username
                    or parsed.password or any(c.isspace() for c in origin) or "\\" in origin):
                raise ValueError("stage loop: remote source needs original HTTPS origin and hashed local evidence")
        if kind == "project" and source["path"] in skip_paths:
            continue  # Historical in-place Task content is represented by submission hashes.
        source_root = BUNDLE if kind == "bundle" else root
        if digest(require_file(source["path"], source_root)) != source["sha256"]:
            raise ValueError("stage loop: canonical source changed")


def require_stage_receipt(event, artifacts, hashes, root, require_file, *, role="author", skip_paths=()):
    data = bound_json(event, "stage_receipt", root, require_file)
    expected = {"gate": event["gate"], "phase": event.get("phase"), "revision": event["revision"], "role": role}
    if type(data.get("version")) is not int or data["version"] != 1 or any(data.get(k) != v for k, v in expected.items()):
        raise ValueError("stage loop: receipt must match current gate, phase, revision and role")
    if not nonempty(data.get("actor")) or data["actor"].strip().casefold() != event["actor"].strip().casefold():
        raise ValueError("stage loop: receipt actor must match current actor")
    if data.get("artifacts") != artifact_bindings(artifacts, hashes):
        raise ValueError("stage loop: receipt must bind exact submitted artifacts and hashes")
    if role != "author" and data.get("findings_sha256") != digest(require_file(event.get("evidence"), root)):
        raise ValueError("stage loop: receipt findings hash mismatch")
    require_knowledge(data.get("knowledge"), root, require_file, skip_paths=skip_paths)
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("stage loop: self-checks or reviewer checks required")
    must_pass = role != "author" and event.get("verdict") == "PASS"
    for check in checks:
        if not isinstance(check, dict) or any(not nonempty(check.get(k)) for k in ("command", "result", "observation")):
            raise ValueError("stage loop: checks require actual command, exit, result and observation")
        code = check.get("exit")
        if type(code) is not int or check["result"] not in {"PASS", "FAIL", "BLOCKED"}:
            raise ValueError("stage loop: invalid check exit or result")
        if (check["result"] == "PASS") != (code == 0):
            raise ValueError("stage loop: check result contradicts exit")
        if must_pass and check["result"] != "PASS":
            raise ValueError("stage loop: unresolved check cannot advance or PASS")
    return data


def require_handoff(event, artifacts, hashes):
    if event.get("artifacts") != artifacts or event.get("sha256") != hashes:
        raise ValueError("stage loop: handoff must bind the exact Discovery submission")


def require_task_snapshot(event, approved, root, require_file):
    from validate_task import validate_task

    task_id, revision, approved_hash = approved
    path = require_file(event["artifacts"]["task_snapshot"], root)
    if digest(path) != approved_hash or event["sha256"]["task_snapshot"] != approved_hash:
        raise ValueError("stage loop: task snapshot must match the approved G6 task hash")
    task = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_task(task, require_coverage=True)
    if errors:
        raise ValueError("stage loop: invalid approved task snapshot: " + "; ".join(errors))
    if (task["task_id"], task["contract_revision"]) != (task_id, revision):
        raise ValueError("stage loop: task snapshot identity/revision must match approved G6")
    return task, approved_hash


def require_execution(event, task, task_hash, attempt, root, require_file):
    # Existing checkpoint and sector receipt formats are retained as immutable snapshots.
    from render_task import read_sector_receipts
    from resume_task import load_checkpoint

    artifacts, hashes = event["artifacts"], event["sha256"]
    snapshot = json.loads(require_file(artifacts["sector_receipts"], root).read_text(encoding="utf-8"))
    receipts = read_sector_receipts(task, snapshot)
    if digest(require_file(artifacts["sector_receipts"], root)) != hashes["sector_receipts"]:
        raise ValueError("stage loop: sector receipts hash mismatch")
    checkpoint = require_file(artifacts["execution_checkpoint"], root)
    if digest(checkpoint) != hashes["execution_checkpoint"]:
        raise ValueError("stage loop: execution checkpoint hash mismatch")
    binding = {"task_id": task["task_id"], "contract_revision": task["contract_revision"],
               "phase": event.get("phase"), "attempt": attempt, "task_sha256": task_hash}
    micros = {m["id"]: m for m in task["microtasks"] if m.get("phase") == event.get("phase")}
    if not micros:
        raise ValueError("stage loop: G7 requires routed microtasks in the current phase")
    state = load_checkpoint(checkpoint, binding, micros, root)
    reviews = {key: review for receipt in receipts.values() for key, review in receipt.get("reviews", {}).items()}
    for key, micro in micros.items():
        items = state["items"].get(key, [])
        if len(items) != len(micro["checklist"]) or any(item.get("status") != "verified" for item in items):
            raise ValueError(f"stage loop: {key} checklist not verified")
        review = reviews.get(key, {})
        if review.get("verdict") != "PASS" or type(review.get("attempt")) is not int or review["attempt"] != attempt:
            raise ValueError(f"stage loop: {key} requires current-attempt independent PASS")
        content = require_file(review["evidence"], root).read_bytes()
        if not content.strip() or hashlib.sha256(content).hexdigest() != review.get("evidence_sha256"):
            raise ValueError(f"stage loop: {key} review evidence changed or empty")
        fingerprint = hashlib.sha256(json.dumps(review, sort_keys=True).encode() + content).hexdigest()
        if state["invalidated"].get(key) == fingerprint:
            raise ValueError(f"stage loop: {key} dependent review is invalidated")
    return state


def release_candidate(artifacts, root, require_file):
    value = json.loads(require_file(artifacts["release_candidate"], root).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or any(not nonempty(value.get(k)) for k in ("candidate", "candidate_sha256", "target")):
        raise ValueError("stage loop: release candidate requires candidate, hash and explicit target")
    if digest(require_file(value["candidate"], root)) != value["candidate_sha256"]:
        raise ValueError("stage loop: release candidate changed")
    return {k: value[k] for k in ("candidate", "candidate_sha256", "target")}


def require_deploy_authorization(event, candidate, attempt, root, require_file):
    data = bound_json(event, "deploy_authorization", root, require_file)
    if (type(data.get("version")) is not int or data["version"] != 1
            or data.get("action") != "deploy" or data.get("revision") != event["revision"]
            or not nonempty(data.get("actor")) or data["actor"].strip().casefold() != event["actor"].strip().casefold()
            or not nonempty(data.get("observation")) or data.get("release") != candidate
            or type(data.get("attempt")) is not int or data["attempt"] != attempt):
        raise ValueError("stage loop: explicit deploy authorization must bind human, revision, candidate, target and attempt")
    return {"path": event["deploy_authorization"], "sha256": event["deploy_authorization_sha256"],
            "release": candidate, "attempt": attempt}


def require_deployment(event, artifacts, authorization, attempt, root, require_file, *, require_pass=False):
    if authorization is None or authorization["attempt"] != attempt:
        raise ValueError("stage loop: current explicit G9 deploy authorization required")
    if digest(require_file(authorization["path"], root)) != authorization["sha256"]:
        raise ValueError("stage loop: deploy authorization changed")
    release = authorization["release"]
    if digest(require_file(release["candidate"], root)) != release["candidate_sha256"]:
        raise ValueError("stage loop: authorized candidate changed before deployment")
    expected = {"release": release, "attempt": attempt,
                "authorization": {k: authorization[k] for k in ("path", "sha256")}}
    for key in ("deployment", "post_deploy_checks"):
        data = json.loads(require_file(artifacts[key], root).read_text(encoding="utf-8"))
        if (not isinstance(data, dict) or type(data.get("attempt")) is not int
                or any(data.get(k) != v for k, v in expected.items())):
            raise ValueError("stage loop: deployment must match authorized candidate, target and attempt")
        checks = data.get("checks")
        if not isinstance(checks, list) or not checks or any(not isinstance(check, dict)
                or not nonempty(check.get("command")) or type(check.get("exit")) is not int
                or check.get("result") not in {"PASS", "FAIL", "BLOCKED"}
                or (check["result"] == "PASS") != (check["exit"] == 0)
                or not nonempty(check.get("observation")) for check in checks):
            raise ValueError("stage loop: deployment and post-deploy checks require actual consistent results")
        if require_pass and any(check["result"] != "PASS" for check in checks):
            raise ValueError("stage loop: deployment and post-deploy checks must be verified PASS")
