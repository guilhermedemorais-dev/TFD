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
from check_qa_consultation import require_consultation
from stage_loop import (require_stage_receipt, require_handoff, require_execution, require_task_snapshot, release_candidate,
                        require_deploy_authorization, require_deployment)


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


def stages(phases, stage_loop=False):
    if not isinstance(phases, list):
        raise ValueError("phases must be a list")
    result = [(gate, None, outputs, reviewers) for gate, outputs, reviewers in PREFIX]
    if stage_loop:
        required = {"G0": ("qa_spec",), "G0.5": ("qa_backend",), "G1": ("qa_spec",), "G5": ("qa_spec",)}
        result = [(gate, phase, outputs, required.get(gate, reviewers)) for gate, phase, outputs, reviewers in result]
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
            ("G7", phase_id, ("implementation", "self_tests") +
             (("task_snapshot", "execution_checkpoint", "sector_receipts") if stage_loop else ()), reviewers),
        ))
    if not stage_loop:
        return result + [(gate, None, outputs, reviewers) for gate, outputs, reviewers in SUFFIX]
    ui_review = ("qa_ui",) if any(phase["ui"] for phase in phases) else ()
    return result + [
        ("G8-review", None, ("review_packet", "local_verification"), ("qa_spec",)),
        ("G8", None, ("technical_docs", "user_help"), ("qa_spec",) + ui_review),
        ("G9", None, ("release_candidate", "operations", "rollback"), ("qa_backend", "security")),
        ("G10", None, ("deployment", "post_deploy_checks"), ("qa_backend", "security") + ui_review),
    ]


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


def require_spec_pass(evidence, spec, revision, gate="G6", verdict="PASS"):
    checker = Path(__file__).resolve().parents[1] / "skills/TFD-qa_spec/scripts/check_findings.py"
    definition = importlib.util.spec_from_file_location("tfd_spec_findings", checker)
    module = importlib.util.module_from_spec(definition)
    definition.loader.exec_module(module)
    findings = json.loads(evidence.read_text(encoding="utf-8"))
    errors = module.validate_findings(findings)
    if errors:
        raise ValueError(f"{gate}: invalid QA findings: " + "; ".join(errors))
    if (findings["verdict"], findings["artifact"], findings["revision"]) != (verdict, spec, revision):
        raise ValueError(f"{gate}: spec QA {verdict} must match the submitted spec and revision")


def discovery_coverage(artifacts, root):
    """Read the submitted research files, retaining source and evidence checks."""
    checker = Path(__file__).resolve().parents[1] / "skills/TFD-discovery/scripts/check_evidence.py"
    definition = importlib.util.spec_from_file_location("tfd_discovery_evidence", checker)
    module = importlib.util.module_from_spec(definition)
    definition.loader.exec_module(module)
    values = {key: json.loads(require_file(artifacts[key], root).read_text(encoding="utf-8"))
              for key in ("sources", "evidence", "coverage")}
    errors, blocked = module.validate(values["sources"], values["evidence"], values["coverage"])
    if errors:
        raise ValueError("invalid Discovery coverage: " + "; ".join(errors))
    return values["coverage"], blocked


def require_task_context(task, artifacts, hashes, phases, reviewed_coverage, discovery_submission,
                         *, require_spec=False, coverage_required=False):
    """Apply the same G6 bindings to the active Task and its historical G7 snapshot."""
    if require_spec and task.get("spec") != artifacts["spec"]:
        raise ValueError("G6: task.spec must match the submitted spec")
    if ("coverage_version" in task or "technical_coverage" in task) and not coverage_required:
        raise ValueError("G6: covered tasks require workflow coverage_version 1")
    if coverage_required:
        if reviewed_coverage is None:
            raise ValueError("G6 requires independent Discovery coverage PASS")
        if (artifacts["discovery"], hashes["discovery"]) != (
                discovery_submission[0]["coverage"], discovery_submission[1]["coverage"]):
            raise ValueError("G6 Discovery must match the G3 reviewed coverage")
        for field, task_field in (("requirement_ids", "requirements"), ("business_rule_ids", "business_rules")):
            if {row["id"] for row in task[task_field]} != set(reviewed_coverage[field]):
                raise ValueError(f"G6: task {task_field} must match reviewed Discovery coverage")
        for area, cell in task["technical_coverage"].items():
            if cell["status"] == "COVERED" and reviewed_coverage["areas"][area]["status"] != "COVERED":
                raise ValueError(f"G6: {area} requires reviewed Discovery evidence")
    if "phases" in task and [entry["id"] for entry in task["phases"]] != [entry["id"] for entry in phases]:
        raise ValueError("G6: task phases must match the G5 plan order")


def evaluate(log, root):
    if not isinstance(log, dict) or not isinstance(log.get("events"), list):
        raise ValueError("workflow must contain phases and an events list")
    if "stage_loop_version" in log and (type(log["stage_loop_version"]) is not int or log["stage_loop_version"] != 1):
        raise ValueError("unsupported workflow stage_loop_version")
    stage_loop = log.get("stage_loop_version") == 1
    if stage_loop and (log.get("coverage_version") != 1 or log.get("review_version") != 1):
        raise ValueError("stage_loop_version 1 requires coverage_version 1 and review_version 1")
    plan = stages(log.get("phases"), stage_loop=stage_loop)
    root = Path(root).resolve()
    preparation = reviewed_preparation(log, root)
    if "coverage_version" in log and (type(log["coverage_version"]) is not int or log["coverage_version"] != 1):
        raise ValueError("unsupported workflow coverage_version")
    coverage_required = log.get("coverage_version") == 1
    if "review_version" in log and (type(log["review_version"]) is not int or log["review_version"] != 1):
        raise ValueError("unsupported workflow review_version")
    review_required = log.get("review_version") == 1
    if review_required and not coverage_required:
        raise ValueError("review_version 1 requires coverage_version 1")
    approved_product = None
    product_submission = None
    submitted_artifacts = submitted_hashes = None
    submitted_inventory = None
    discovery_submission = None
    reviewed_coverage = None
    step = attempts = 0
    submission = None
    reviews = {}
    revisions = set()
    status = "AWAITING_SUBMISSION"
    latest_task_submission = max((index for index, event in enumerate(log["events"])
                                  if isinstance(event, dict) and event.get("gate") == "G6"
                                  and event.get("action") == "submit"), default=-1)
    previous_task = None
    phase_tasks = {}
    deploy_authorization = candidate = None
    deploy_attempts = 0
    author_checks_pass = True
    for index, event in enumerate(log["events"]):
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        if step == len(plan) or status == "BLOCKED":
            raise ValueError("cannot advance a complete or blocked workflow")
        gate, phase, outputs, reviewers = plan[step]
        if coverage_required and gate in ("G2", "G3"):
            outputs = tuple(dict.fromkeys((*outputs, "sources", "evidence", "coverage")))
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
                phase_tasks[phase] = {"identity": (task_id, contract_revision, hashes["task"]),
                                      "artifacts": artifacts.copy(), "hashes": hashes.copy(),
                                      "coverage": reviewed_coverage, "discovery": discovery_submission}
            for key, path in artifacts.items():
                if gate == "G6" and key in TASK_ARTIFACTS and index != latest_task_submission:
                    continue  # Past task revisions are receipts, not active task files.
                content = require_file(path, root).read_bytes()
                submitted_files[key] = content
                if hashlib.sha256(content).hexdigest() != hashes[key]:
                    raise ValueError(f"{gate}: artifact changed: {path}")
                if gate == "G5" and key == "phase_plan" and json.loads(content) != log["phases"]:
                    raise ValueError("phase applicability must match the submitted G5 plan")
            if coverage_required and gate == "G2":
                discovery_coverage(artifacts, root)
                discovery_submission = (artifacts.copy(), hashes.copy())
            if coverage_required and gate == "G3":
                if discovery_submission is None:
                    raise ValueError("G3 requires submitted Discovery coverage")
                original, original_hashes = discovery_submission
                if attempts == 0 and any((artifacts[key], hashes[key]) !=
                                         (original[key], original_hashes[key])
                                         for key in ("sources", "evidence", "coverage")):
                    raise ValueError("G3 coverage must match the submitted Discovery revision")
                discovery_coverage(artifacts, root)
                discovery_submission = (artifacts.copy(), hashes.copy())
            if gate == "G6" and index == latest_task_submission:
                task = json.loads(submitted_files["task"])
                errors = validate_task(task, require_coverage=True) if coverage_required else validate_task(task)
                if errors:
                    raise ValueError("invalid task: " + "; ".join(errors))
                if (task["task_id"], task["contract_revision"]) != (task_id, contract_revision):
                    raise ValueError("G6: active task does not match submitted identity and revision")
                require_task_context(task, artifacts, hashes, log["phases"], reviewed_coverage, discovery_submission,
                                     require_spec=preparation or coverage_required, coverage_required=coverage_required)
                view = submitted_files["task_view"].decode("utf-8").replace("\r\n", "\n")
                if markdown_body(view) != render_task(task, PurePosixPath(task_paths[0]).name):
                    raise ValueError("G6: task_view must be generated from the submitted task JSON")
            if stage_loop:
                skipped = tuple(artifacts[k] for k in TASK_ARTIFACTS) if gate == "G6" and index < latest_task_submission else ()
                receipt = require_stage_receipt(event, artifacts, hashes, root, require_file, skip_paths=skipped)
                author_checks_pass = all(check["result"] == "PASS" for check in receipt["checks"])
                if gate == "G7":
                    context = phase_tasks[phase]
                    task, task_hash = require_task_snapshot(event, context["identity"], root, require_file)
                    require_task_context(task, context["artifacts"], context["hashes"], log["phases"],
                                         context["coverage"], context["discovery"], require_spec=True, coverage_required=True)
                    require_execution(event, task, task_hash, attempts + 1, root, require_file)
                if gate == "G9":
                    candidate = release_candidate(artifacts, root, require_file)
                    deploy_authorization = None
                if gate == "G10":
                    if deploy_attempts >= 4:
                        raise ValueError("stage loop: deployment retry limit reached")
                    require_deployment(event, artifacts, deploy_authorization, deploy_attempts + 1, root, require_file)
                    deploy_attempts += 1
            revisions.add(revision)
            if gate == "G1":
                product_submission = (artifacts["prd"], hashes["prd"], revision)
            submitted_artifacts, submitted_hashes = artifacts.copy(), hashes.copy()
            submitted_inventory = None
            if review_required and gate == "G6" and index == latest_task_submission:
                submitted_inventory = {"requirement_ids": [row["id"] for row in task["requirements"]],
                                       "business_rule_ids": [row["id"] for row in task["business_rules"]]}
            submission = (revision, actor, artifacts.get("spec"))
            reviews = {}
            attempts += 1
            status = "AWAITING_HANDOFF" if stage_loop and gate == "G2" else ("AWAITING_QA" if reviewers else "AWAITING_APPROVAL")
            if stage_loop and gate == "G2" and not author_checks_pass:
                status = "BLOCKED" if attempts >= 4 else "REWORK"
            continue
        if submission is None or revision != submission[0]:
            raise ValueError("event must reference the current submitted revision")
        if actor == submission[1]:
            raise ValueError("the author cannot review or approve their own work")
        evidence = require_file(event.get("evidence"), root)
        if stage_loop and gate == "G2":
            if action != "handoff" or status != "AWAITING_HANDOFF":
                raise ValueError("stage loop: G2 requires internal handoff to G3, not approval or completion")
            require_handoff(event, submitted_artifacts, submitted_hashes)
            if not evidence.read_bytes().strip():
                raise ValueError("stage loop: handoff evidence must be nonempty")
            step += 1
            attempts = 0
            submission = None
            reviews = {}
            status = "AWAITING_SUBMISSION"
            continue
        if action == "review":
            reviewer = event.get("reviewer")
            verdict = event.get("verdict")
            if status != "AWAITING_QA" or reviewer not in reviewers or reviewer in reviews:
                raise ValueError("review must come from a pending required sector")
            if actor in {person for _, person in reviews.values()}:
                raise ValueError("each required review needs a distinct reviewer")
            if verdict not in ("PASS", "REWORK", "BLOCKED"):
                raise ValueError("invalid reviewer verdict")
            if stage_loop:
                skipped = tuple(submitted_artifacts[k] for k in TASK_ARTIFACTS) if gate == "G6" and index < latest_task_submission else ()
                require_stage_receipt(event, submitted_artifacts, submitted_hashes, root, require_file,
                                      role=reviewer, skip_paths=skipped)
                if verdict == "PASS" and not author_checks_pass:
                    raise ValueError("stage loop: unresolved author self-check cannot PASS")
                if gate == "G10" and verdict == "PASS":
                    require_deployment(event, submitted_artifacts, deploy_authorization, deploy_attempts,
                                       root, require_file, require_pass=True)
            if review_required and gate in ("G3", "G6") and reviewer == "qa_spec":
                target = submitted_artifacts["coverage" if gate == "G3" else "spec"]
                require_spec_pass(evidence, target, revision, gate, verdict)
                references = dict(approved_product[0])
                for kind in (("coverage",) if gate == "G3" else ("spec", "task", "discovery")):
                    references[kind] = (submitted_artifacts[kind], submitted_hashes[kind])
                inventory = (discovery_coverage(submitted_artifacts, root)[0]
                             if gate == "G3" else submitted_inventory)
                require_consultation(event, root, require_file, target, references, inventory,
                                     approved_product[1], historical_task=index < latest_task_submission)
            if coverage_required and gate == "G3" and verdict == "PASS":
                original, original_hashes = discovery_submission
                for key in ("sources", "evidence", "coverage"):
                    if hashlib.sha256(require_file(original[key], root).read_bytes()).hexdigest() != original_hashes[key]:
                        raise ValueError("G3 Discovery evidence changed after submission")
                coverage, blocked = discovery_coverage(discovery_submission[0], root)
                if blocked:
                    raise ValueError("G3: unresolved Discovery coverage: " + ", ".join(blocked))
                require_spec_pass(evidence, discovery_submission[0]["coverage"], revision, gate="G3")
                reviewed_coverage = coverage
            if (preparation or coverage_required) and gate == "G6" and verdict == "PASS":
                require_spec_pass(evidence, submission[2], revision)
            reviews[reviewer] = (verdict, actor)
            if verdict == "BLOCKED" or (verdict == "REWORK" and attempts >= 4):
                status = "BLOCKED"
            elif verdict == "REWORK":
                status = "REWORK"
            elif all(role in reviews for role in reviewers):
                status = "AWAITING_APPROVAL"
            if stage_loop and gate == "G10" and verdict == "REWORK":
                if deploy_attempts >= 4:
                    status = "BLOCKED"
                else:
                    # Every fresh deployment attempt needs G9 QA and new human authorization.
                    step -= 1
                    attempts = 0
                    submission = None
                    reviews = {}
                    deploy_authorization = None
                    status = "AWAITING_SUBMISSION"
        elif action in ("approve", "complete"):
            if action == "complete":
                terminal_deploy = stage_loop and gate == "G10"
                if not terminal_deploy and (not preparation or gate not in PREPARATION_GATES):
                    raise ValueError("complete requires authorized preparation at G2-G5 only")
                if not evidence.read_bytes().strip():
                    raise ValueError("completion evidence must be nonempty")
            if status != "AWAITING_APPROVAL" or actor in {person for _, person in reviews.values()}:
                raise ValueError("completion requires current QA passes and an independent coordinator"
                                 if action == "complete" else
                                 "approval requires current QA passes and an independent human")
            if stage_loop and not evidence.read_bytes().strip():
                raise ValueError("stage loop: approval/completion evidence must be nonempty")
            if stage_loop and gate == "G9":
                if action != "approve":
                    raise ValueError("stage loop: G9 requires explicit human deploy approval")
                deploy_authorization = require_deploy_authorization(event, candidate, deploy_attempts + 1, root, require_file)
            if stage_loop and gate == "G10":
                if action != "complete":
                    raise ValueError("stage loop: G10 completes under the preserved G9 authorization")
                require_deployment(event, submitted_artifacts, deploy_authorization, deploy_attempts,
                                   root, require_file, require_pass=True)
            if gate == "G1":
                path, sha256, prd_revision = product_submission
                approved_product = ({"prd": (path, sha256),
                                     "approval": (event["evidence"], hashlib.sha256(evidence.read_bytes()).hexdigest())},
                                    prd_revision)
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
    if coverage_required and gate in ("G2", "G3"):
        outputs = tuple(dict.fromkeys((*outputs, "sources", "evidence", "coverage")))
    return {
        "status": status, "gate": gate, "phase": phase,
        "attempts": attempts, "required_artifacts": outputs,
        "pending_reviewers": [role for role in reviewers if role not in reviews],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--init", action="store_true", help="create a new workflow with coverage and review QA enabled")
    args = parser.parse_args()
    try:
        if args.init:
            with args.workflow.open("x", encoding="utf-8") as stream:
                json.dump({"stage_loop_version": 1, "coverage_version": 1, "review_version": 1,
                           "phases": [], "events": []}, stream, indent=2)
                stream.write("\n")
        result = evaluate(json.loads(args.workflow.read_text(encoding="utf-8")), args.project_root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 2 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
