# Contexto TFD · 1387 palavras · 2866 tokens (o200k_base)

"""Check a project-local TFD workflow log and print its next gate."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath

from context_budget import markdown_body
from render_task import render_task
from validate_task import validate_task


PREFIX = (
    ("G0", ("constitution",), ()),
    ("G0.5", ("environment",), ()),
    ("G1", ("briefing", "prd"), ()),
    ("G2", ("sources", "evidence", "findings"), ()),
    ("G3", ("findings",), ("qa_spec",)),
    ("G4", ("architecture", "contracts"), ("qa_spec",)),
    ("G5", ("phase_plan", "estimates"), ()),
)
SUFFIX = (
    ("G8-review", ("review_packet", "local_verification"), ()),
    ("G8", ("technical_docs", "user_help"), ()),
)
TRACKS = {"backend": "qa_backend", "ui": "qa_ui", "security": "security"}
TASK_ARTIFACTS = ("task", "task_view")
PREPARATION_GATES = {"G2", "G3", "G4", "G5"}


def stages(phases):
    if not isinstance(phases, list):
        raise ValueError("phases must be a list")
    result = [(gate, None, outputs, reviewers) for gate, outputs, reviewers in PREFIX]
    if not phases:
        return result
    seen = set()
    for phase in phases:
        if not isinstance(phase, dict):
            raise ValueError("phase must be an object")
        phase_id = phase.get("id")
        if not isinstance(phase_id, str) or not phase_id.strip() or phase_id in seen:
            raise ValueError("phase IDs must be nonempty and unique")
        if any(type(phase.get(track)) is not bool for track in TRACKS):
            raise ValueError(f"{phase_id}: declare backend, ui and security applicability")
        if not (phase["backend"] or phase["ui"]):
            raise ValueError(f"{phase_id}: choose backend or UI QA for implementation")
        seen.add(phase_id)
        reviewers = tuple(role for track, role in TRACKS.items() if phase[track])
        result.extend((
            ("G6", phase_id, ("spec", "discovery", "task", "task_view"), ("qa_spec",)),
            ("G7", phase_id, ("implementation", "self_tests"), reviewers),
        ))
    return result + [(gate, None, outputs, reviewers) for gate, outputs, reviewers in SUFFIX]


def require_file(path, root):
    if not isinstance(path, str) or not path or "\\" in path or ":" in path:
        raise ValueError("evidence must use a project-relative POSIX path")
    relative = PurePosixPath(path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe evidence path: {path}")
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError(f"evidence file unavailable inside project: {path}")
    return resolved


def reviewed_preparation(log, root):
    if "preparation" not in log:
        return False
    config = log["preparation"]
    if (not isinstance(config, dict) or set(config) != {"mode", "authorization"}
            or config["mode"] != "reviewed_task"):
        raise ValueError("preparation requires mode reviewed_task and authorization only")
    if not require_file(config["authorization"], root).read_bytes().strip():
        raise ValueError("preparation authorization must be nonempty")
    return True


def require_spec_pass(evidence, spec, revision):
    checker = Path(__file__).resolve().parents[1] / "skills/TFD-qa_spec/scripts/check_findings.py"
    definition = importlib.util.spec_from_file_location("tfd_spec_findings", checker)
    module = importlib.util.module_from_spec(definition)
    definition.loader.exec_module(module)
    findings = json.loads(evidence.read_text(encoding="utf-8"))
    errors = module.validate_findings(findings)
    if errors:
        raise ValueError("G6: invalid spec QA findings: " + "; ".join(errors))
    if (findings["verdict"], findings["artifact"], findings["revision"]) != ("PASS", spec, revision):
        raise ValueError("G6: spec QA PASS must match the submitted spec and revision")


def evaluate(log, root):
    if not isinstance(log, dict) or not isinstance(log.get("events"), list):
        raise ValueError("workflow must contain phases and an events list")
    plan = stages(log.get("phases"))
    root = Path(root).resolve()
    preparation = reviewed_preparation(log, root)
    step = attempts = 0
    submission = None
    reviews = {}
    revisions = set()
    status = "AWAITING_SUBMISSION"
    latest_task_submission = max((index for index, event in enumerate(log["events"])
                                  if isinstance(event, dict) and event.get("gate") == "G6"
                                  and event.get("action") == "submit"), default=-1)
    previous_task = None
    for index, event in enumerate(log["events"]):
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        if step == len(plan) or status == "BLOCKED":
            raise ValueError("cannot advance a complete or blocked workflow")
        gate, phase, outputs, reviewers = plan[step]
        if (event.get("gate"), event.get("phase")) != (gate, phase):
            raise ValueError(f"out of order: expected {gate} {phase or ''}".strip())
        action, actor, revision = (event.get(key) for key in ("action", "actor", "revision"))
        if not all(isinstance(value, str) and value.strip() for value in (action, actor, revision)):
            raise ValueError("action, actor and revision are required")
        actor = actor.strip().casefold()
        if action == "block":
            require_file(event.get("evidence"), root)
            if submission is not None and revision != submission[0]:
                raise ValueError("block must reference the current submitted revision")
            status = "BLOCKED"
            continue
        if action == "submit":
            if status not in ("AWAITING_SUBMISSION", "REWORK"):
                raise ValueError("submit only at a new stage or after REWORK")
            if revision in revisions:
                raise ValueError("rework requires a new revision")
            if gate == "G5" and not log["phases"]:
                raise ValueError("G5 requires at least one planned phase")
            artifacts = event.get("artifacts")
            if not isinstance(artifacts, dict) or any(key not in artifacts for key in outputs):
                raise ValueError(f"{gate} requires artifacts: {', '.join(outputs)}")
            hashes = event.get("sha256")
            if not isinstance(hashes, dict) or hashes.keys() != artifacts.keys():
                raise ValueError("supply one SHA-256 per submitted artifact")
            submitted_files = {}
            if gate == "G6":
                task_id = event.get("task_id")
                contract_revision = event.get("contract_revision")
                task_paths = tuple(artifacts[key] for key in TASK_ARTIFACTS)
                task_hashes = tuple(hashes[key] for key in TASK_ARTIFACTS)
                if not isinstance(task_id, str) or not task_id or type(contract_revision) is not int or contract_revision < 1:
                    raise ValueError("G6: task_id and positive contract_revision are required")
                if previous_task:
                    old_id, old_revision, old_paths, old_hashes = previous_task
                    if task_id != old_id or task_paths != old_paths:
                        raise ValueError("G6: update the existing task ID and paths in place")
                    if contract_revision < old_revision or (task_hashes != old_hashes and contract_revision == old_revision):
                        raise ValueError("G6: changing the task requires a higher contract_revision")
                previous_task = (task_id, contract_revision, task_paths, task_hashes)
            for key, path in artifacts.items():
                if gate == "G6" and key in TASK_ARTIFACTS and index != latest_task_submission:
                    continue  # Past task revisions are receipts, not active task files.
                content = require_file(path, root).read_bytes()
                submitted_files[key] = content
                if hashlib.sha256(content).hexdigest() != hashes[key]:
                    raise ValueError(f"{gate}: artifact changed: {path}")
                if gate == "G5" and key == "phase_plan" and json.loads(content) != log["phases"]:
                    raise ValueError("phase applicability must match the submitted G5 plan")
            if gate == "G6" and index == latest_task_submission:
                task = json.loads(submitted_files["task"])
                errors = validate_task(task)
                if errors:
                    raise ValueError("invalid task: " + "; ".join(errors))
                if (task["task_id"], task["contract_revision"]) != (task_id, contract_revision):
                    raise ValueError("G6: active task does not match submitted identity and revision")
                if preparation and task.get("spec") != artifacts["spec"]:
                    raise ValueError("G6: task.spec must match the submitted spec")
                if "phases" in task and [entry["id"] for entry in task["phases"]] != [
                    entry["id"] for entry in log["phases"]
                ]:
                    raise ValueError("G6: task phases must match the G5 plan order")
                view = submitted_files["task_view"].decode("utf-8").replace("\r\n", "\n")
                if markdown_body(view) != render_task(task, PurePosixPath(task_paths[0]).name):
                    raise ValueError("G6: task_view must be generated from the submitted task JSON")
            revisions.add(revision)
            submission = (revision, actor, artifacts.get("spec"))
            reviews = {}
            attempts += 1
            status = "AWAITING_QA" if reviewers else "AWAITING_APPROVAL"
            continue
        if submission is None or revision != submission[0]:
            raise ValueError("event must reference the current submitted revision")
        if actor == submission[1]:
            raise ValueError("the author cannot review or approve their own work")
        evidence = require_file(event.get("evidence"), root)
        if action == "review":
            reviewer = event.get("reviewer")
            verdict = event.get("verdict")
            if status != "AWAITING_QA" or reviewer not in reviewers or reviewer in reviews:
                raise ValueError("review must come from a pending required sector")
            if actor in {person for _, person in reviews.values()}:
                raise ValueError("each required review needs a distinct reviewer")
            if verdict not in ("PASS", "REWORK", "BLOCKED"):
                raise ValueError("invalid reviewer verdict")
            if preparation and gate == "G6" and verdict == "PASS":
                require_spec_pass(evidence, submission[2], revision)
            reviews[reviewer] = (verdict, actor)
            if verdict == "BLOCKED" or (verdict == "REWORK" and attempts >= 4):
                status = "BLOCKED"
            elif verdict == "REWORK":
                status = "REWORK"
            elif all(role in reviews for role in reviewers):
                status = "AWAITING_APPROVAL"
        elif action in ("approve", "complete"):
            if action == "complete":
                if not preparation or gate not in PREPARATION_GATES:
                    raise ValueError("complete requires authorized preparation at G2-G5 only")
                if not evidence.read_bytes().strip():
                    raise ValueError("completion evidence must be nonempty")
            if status != "AWAITING_APPROVAL" or actor in {person for _, person in reviews.values()}:
                raise ValueError("completion requires current QA passes and an independent coordinator"
                                 if action == "complete" else
                                 "approval requires current QA passes and an independent human")
            step += 1
            attempts = 0
            submission = None
            reviews = {}
            status = "AWAITING_SUBMISSION"
        else:
            raise ValueError(f"unknown action: {action}")
    if step == len(plan):
        return {"status": "COMPLETE"}
    gate, phase, outputs, reviewers = plan[step]
    return {
        "status": status, "gate": gate, "phase": phase,
        "attempts": attempts, "required_artifacts": outputs,
        "pending_reviewers": [role for role in reviewers if role not in reviews],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.workflow.read_text(encoding="utf-8")), args.project_root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 2 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
