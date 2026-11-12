# Contexto TFD · 1704 palavras · 3602 tokens (o200k_base)

"""Resolve the next TFD action and checkpoint implementation checklist items."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

from pipeline import evaluate, require_file
from render_task import read_sector_receipts
from validate_task import glob_to_regex


def approved_artifact(log, gate, name):
    for index in range(len(log["events"]) - 1, -1, -1):
        event = log["events"][index]
        if event["gate"] == gate and event["action"] == "approve":
            return next(submit["artifacts"][name] for submit in reversed(log["events"][:index])
                        if submit["gate"] == gate and submit["action"] == "submit"
                        and submit["revision"] == event["revision"])
    return None


def canonical_path(value):
    path = PurePosixPath(value)
    if (not value or path == PurePosixPath('.') or path.is_absolute() or '..' in path.parts
            or '\\' in value or ':' in value or path.as_posix() != value):
        raise ValueError(f"expected a project-relative POSIX path: {value!r}")
    return value.casefold() if os.name == "nt" else value


def matches(path, patterns):
    for pattern in patterns:
        pattern = canonical_path(pattern.rstrip('/'))
        if glob_to_regex(pattern).fullmatch(path) or ('*' not in pattern and path.startswith(pattern + '/')):
            return True
    return False


def changed_paths(root, base):
    def git(*arguments):
        return subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True,
                              timeout=30).stdout

    if Path(os.fsdecode(git("rev-parse", "--show-toplevel").rstrip())).resolve() != root:
        raise ValueError("the project root must be the Git worktree root for path checks")
    commit = git("rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
    files = git("diff", "--name-only", "-z", "--no-renames", commit, "--")
    files += git("diff", "--cached", "--name-only", "-z", "--no-renames", commit, "--")
    files += git("ls-files", "-z", "--others", "--exclude-standard", "--")
    return sorted({os.fsdecode(path) for path in files.split(b"\0") if path})


def violations(task, micro, paths):
    return [value for value in paths if (matches(canonical_path(value), task["protected_paths"])
            or not matches(canonical_path(value), task["allowed_paths"])
            or not matches(canonical_path(value), micro["allowed_paths"]))]


@contextmanager
def checkpoint_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".lock")
    if lock.is_symlink():
        raise ValueError("checkpoint lock must not be a symbolic link")
    with lock.open("a+b") as stream:
        try:
            if os.name == "nt":
                import msvcrt
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError("checkpoint is in use; retry after the current writer finishes") from exc
        yield


def save_checkpoint(path, contents):
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write((json.dumps(contents, ensure_ascii=False, separators=(",", ":")) + '\n').encode())
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def load_checkpoint(path, binding, micros, root):
    if not path.exists():
        return {**binding, "items": {}, "rework": {}, "invalidated": {}}
    result = json.loads(path.read_bytes())
    if not isinstance(result, dict) or any(result.get(key) != value for key, value in binding.items()):
        raise ValueError("checkpoint does not match the current task, phase and attempt")
    items = result.get("items")
    rework = result.get("rework")
    invalidated = result.get("invalidated")
    if not all(isinstance(value, dict) for value in (items, rework, invalidated)):
        raise ValueError("checkpoint items, rework and invalidated reviews must be objects")
    if any(micro_id not in micros or not isinstance(hashes, list) or len(hashes) > 3
           or any(not isinstance(value, str) for value in hashes) for micro_id, hashes in rework.items()):
        raise ValueError("invalid microtask rework history")
    if any(key not in micros or not isinstance(value, str) for key, value in invalidated.items()):
        raise ValueError("invalidated reviews must identify current-phase microtasks and evidence")
    for micro_id, entries in items.items():
        if micro_id not in micros or not isinstance(entries, list) or len(entries) > len(micros[micro_id]["checklist"]):
            raise ValueError(f"invalid checkpoint route: {micro_id}")
        for index, entry in enumerate(entries):
            if entry == {"status": "started"} and index == len(entries) - 1:
                continue
            if not isinstance(entry, dict) or entry.get("status") != "verified":
                raise ValueError(f"invalid checkpoint item: {micro_id}/{index + 1}")
            content = require_file(entry.get("evidence"), root).read_bytes()
            if not content.strip() or hashlib.sha256(content).hexdigest() != entry.get("sha256"):
                raise ValueError(f"item evidence changed: {micro_id}/{index + 1}")
    return result


def next_item(micros, passed, rework, state, base):
    for micro_id, micro in micros.items():
        if micro_id in passed or set(micro.get("depends_on", [])) - passed:
            continue
        items = state["items"].get(micro_id, [])
        pending = items and items[-1]["status"] == "started"
        index = len(items) - int(bool(pending))
        route = {**base, "microtask": micro_id, "sector": micro["sector"], "owner": micro["owner"],
                 "validator": micro["validator"], "verified_items": index}
        finding = rework.get(micro_id)
        history = state["rework"].get(micro_id, [])
        if finding and finding[1] not in history:
            evidence, _ = finding
            action = "MICROTASK_REWORK_LIMIT" if len(history) == 3 else "REWORK_MICROTASK"
            return {**route, "action": action, "evidence": evidence}
        if index == len(micro["checklist"]):
            return {**route, "action": "REQUEST_MICROTASK_QA"}
        return {**route, "action": "RECONCILE_ITEM" if pending else "EXECUTE_ITEM",
                "item": index + 1, "check": micro["checklist"][index]}
    return {**base, "action": "PREPARE_GATE_SUBMISSION" if set(micros) <= passed else "DEPENDENCY_PENDING"}


def resolve_passes(micros, previously_passed, approvals, invalidated):
    passed = set(previously_passed)
    pending = {key for key, fingerprint in approvals.items() if invalidated.get(key) != fingerprint}
    while pending:
        eligible = {key for key in pending if set(micros[key].get("depends_on", [])) <= passed}
        if not eligible:
            break
        passed.update(eligible)
        pending.difference_update(eligible)
    return passed


def dependent_microtasks(micros, root_id):
    affected = {root_id}
    while True:
        added = {key for key, micro in micros.items() if affected.intersection(micro.get("depends_on", []))}
        if added <= affected:
            return affected - {root_id}
        affected.update(added)


def resume(workflow, root, args):
    ledger = workflow.read_bytes()
    log = json.loads(ledger)
    stage = evaluate(log, root)
    base = {**stage, "constitution": approved_artifact(log, "G0", "constitution"),
            "environment": approved_artifact(log, "G0.5", "environment")}
    if stage.get("gate") != "G7" or stage["status"] not in {"AWAITING_SUBMISSION", "REWORK"}:
        return {**base, "action": "FOLLOW_GATE"}

    phase, attempt = stage["phase"], stage["attempts"] + 1
    submitted = next(event for event in reversed(log["events"]) if event["gate"] == "G6"
                     and event["phase"] == phase and event["action"] == "submit")
    task_path = submitted["artifacts"]["task"]
    task = json.loads(require_file(task_path, root).read_bytes())
    base.update(task=task_path, task_id=task["task_id"], contract_revision=task["contract_revision"],
                complexity=task["complexity"], attempt=attempt)
    if "sectors" not in task:
        return {**base, "action": "LEGACY_TASK_ROUTE"}

    micros = {micro["id"]: micro for micro in task["microtasks"] if micro["phase"] == phase}
    prior_phases = [entry["id"] for entry in task["phases"]]
    prior_phases = set(prior_phases[:prior_phases.index(phase)])
    passed = {micro["id"] for micro in task["microtasks"] if micro["phase"] in prior_phases}
    if log.get("sector_receipts"):
        receipts = read_sector_receipts(task, log)
        reviews = {micro_id: review for receipt in receipts.values()
                   for micro_id, review in receipt.get("reviews", {}).items() if micro_id in micros}
    else:
        reviews = {}
    rework = {}
    approved = {}
    for micro_id, review in reviews.items():
        number = review.get("attempt", 1)
        if type(number) is not int or not 1 <= number <= attempt:
            raise ValueError(f"invalid review attempt: {micro_id}")
        content = require_file(review["evidence"], root).read_bytes()
        if not content.strip():
            raise ValueError(f"empty review evidence: {micro_id}")
        fingerprint = hashlib.sha256(json.dumps(review, sort_keys=True).encode() + content).hexdigest()
        if review["verdict"] == "PASS":
            approved[micro_id] = fingerprint
        if review["verdict"] == "REWORK" and (number == attempt or (
                stage["status"] == "REWORK" and number == attempt - 1)):
            rework[micro_id] = (review["evidence"], fingerprint)
        if review["verdict"] == "BLOCKED":
            return {**base, "action": "MICROTASK_BLOCKED", "microtask": micro_id, "evidence": review["evidence"]}
    if stage["status"] == "REWORK" and not any(
            (review["verdict"], review.get("attempt", 1)) in {
                ("REWORK", attempt - 1), ("REWORK", attempt), ("PASS", attempt)}
            for review in reviews.values()):
        return {**base, "action": "MAP_REWORK_TO_MICROTASKS"}

    binding = {key: base[key] for key in ("task_id", "contract_revision", "phase", "attempt")}
    binding["task_sha256"] = submitted["sha256"]["task"]
    key = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()[:24]
    path = workflow.with_name(workflow.stem + "-execution") / (key + ".json")
    if not path.resolve().is_relative_to(root) or path.is_symlink():
        raise ValueError("checkpoint must remain inside the project")
    base["checkpoint"] = path.relative_to(root).as_posix()

    def route():
        state = load_checkpoint(path, binding, micros, root)
        resolved = resolve_passes(micros, passed, approved, state["invalidated"])
        result = next_item(micros, resolved, rework, state, base)
        if args.git_base:
            if args.microtask not in micros:
                raise ValueError("path verification requires a microtask in the current phase")
            internal = {base["checkpoint"], path.with_suffix(".lock").relative_to(root).as_posix()}
            changed = [name for name in changed_paths(root, args.git_base) if name not in internal]
            invalid = violations(task, micros[args.microtask], changed)
            if invalid:
                return {**result, "action": "PATH_VIOLATION", "path_check": "VIOLATION", "paths": invalid}
            result["path_check"] = "PASSED"
        if not args.record:
            return result
        if args.record == "rework":
            if (result["action"], result.get("microtask")) != ("REWORK_MICROTASK", args.microtask):
                raise ValueError("record rework only for the current independently reviewed microtask")
            state["rework"].setdefault(args.microtask, []).append(rework[args.microtask][1])
            affected = dependent_microtasks(micros, args.microtask)
            for micro_id in affected | {args.microtask}:
                state["items"].pop(micro_id, None)
            state["invalidated"].update({key: approved[key] for key in affected & approved.keys()})
            save_checkpoint(path, state)
            return {**result, "recorded": args.record}
        expected = "EXECUTE_ITEM" if args.record == "started" else "RECONCILE_ITEM"
        if (result["action"], result.get("microtask"), result.get("item")) != (expected, args.microtask, args.item):
            raise ValueError("record only the current item after its expected action")
        items = state["items"].setdefault(args.microtask, [])
        if args.record == "started":
            items.append({"status": "started"})
        else:
            content = require_file(args.evidence, root).read_bytes()
            if not content.strip():
                raise ValueError("item verification evidence is empty")
            items[-1] = {"status": "verified", "evidence": args.evidence, "sha256": hashlib.sha256(content).hexdigest()}
        save_checkpoint(path, state)
        return {**result, "recorded": args.record}

    if args.record:
        with checkpoint_lock(path):
            if workflow.read_bytes() != ledger:
                raise ValueError("workflow changed while preparing the checkpoint; recover the current route")
            return route()
    return route()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--record", choices=("started", "verified", "rework"))
    parser.add_argument("--microtask")
    parser.add_argument("--item", type=int)
    parser.add_argument("--evidence", help="immutable project-relative verification evidence")
    parser.add_argument("--git-base", help="compare all changed paths in an isolated microtask worktree")
    args = parser.parse_args()
    if args.record and (not args.microtask or (args.record != "rework" and not args.item)
                        or (args.record == "verified" and not args.evidence)):
        parser.error("recording requires --microtask, --item for item actions and --evidence for verified")
    try:
        root, workflow = args.project_root.resolve(), args.workflow.resolve()
        if not workflow.is_relative_to(root):
            raise ValueError("workflow must be inside the project")
        result = resume(workflow, root, args)
        if args.git_base and "path_check" not in result:
            raise ValueError("the current gate does not permit an implementation path check")
        if args.record and "recorded" not in result and result["action"] != "PATH_VIOLATION":
            raise ValueError("the current gate does not accept an item checkpoint")
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 2 if result["action"] == "PATH_VIOLATION" else 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
