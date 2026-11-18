"""Review receipts bind declarations to actual workflow artifacts, not source truth."""

import copy
import hashlib
import json
import unittest
import subprocess
import sys

from tests import test_coverage_pipeline
from pipeline import evaluate


class TestQAConsultation(unittest.TestCase):
    def setUp(self):
        self.case = test_coverage_pipeline.TestCoveragePipeline()
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.log, self.root = self.case.log, self.case.root
        self.log["review_version"] = 1
        self.inventory = {"requirement_ids": ["REQ-01", "REQ-02"], "business_rule_ids": ["RULE-01"]}
        prd = next(e for e in self.log["events"] if e["gate"] == "G1" and e["action"] == "submit")
        prd["sha256"]["prd"] = self.case.write(prd["artifacts"]["prd"], {
            "requirements": [{"id": "REQ-01"}, {"id": "REQ-02"}],
            "business_rules": [{"id": "RULE-01", "decision": "Only authorized edits"}]})

    def consultation(self, event=None):
        event = event or self.log["events"][-1]
        gate = event["gate"]
        submit = next(e for e in reversed(self.log["events"])
                      if e["gate"] == gate and e["action"] == "submit")
        prd = next(e for e in self.log["events"] if e["gate"] == "G1" and e["action"] == "submit")
        approval = next(e for e in self.log["events"] if e["gate"] == "G1" and e["action"] == "approve")
        targets = {"prd": prd["artifacts"]["prd"], "approval": approval["evidence"]}
        targets.update({k: submit["artifacts"][k] for k in
                        (("coverage",) if gate == "G3" else ("spec", "task", "discovery"))})
        commit = "efdec594ac403754baea2bb04952dd1d68da35c7"
        sources = {"business_decision": targets["prd"],
                   "guide": "https://github.com/MatthewKerns/software-development-best-practices-guide/tree/" + commit,
                   "primary": "https://docs.python.org/3/library/hashlib.html"}
        return {"version": 1, "reviewed_by": event["actor"],
                "artifact": submit["artifacts"]["coverage" if gate == "G3" else "spec"],
                "revision": event["revision"],
                "findings_sha256": hashlib.sha256((self.root / event["evidence"]).read_bytes()).hexdigest(),
                "references": [{"kind": k, "path": p,
                                "sha256": hashlib.sha256((self.root / p).read_bytes()).hexdigest(),
                                "locator": "Approved inventory"} for k, p in targets.items()],
                "approved_inventory": copy.deepcopy(self.inventory),
                "comparison": {"omitted_ids": [], "extra_ids": [], "contradicted_ids": [],
                               "observation": "Compared approved IDs and authorization decision with target"},
                "checks": [{"kind": k, "claim_ids": ["RULE-01"], "source": s,
                            "revision": commit if k == "guide" else "3.13" if k == "primary" else "rev2",
                            "locator": "hashlib.sha256" if k == "primary" else "authorization / review section",
                            "status": "VERIFIED", "observation": "Review declaration fixture",
                            "limits": "Fixture validates bindings; does not establish actual source reading"}
                           for k, s in sources.items()]}

    def attach(self, data=None):
        event = self.log["events"][-1]
        name = event["revision"] + "-consultation.json"
        event["consultation"] = name
        event["consultation_sha256"] = self.case.write(name, data or self.consultation())

    def reviewed_g3(self):
        self.case.discovery_to_review()
        self.case.qa()
        self.attach()

    def task_to_review(self):
        self.case.submit_task()
        # This fixture's helper creates the previous G3 review before the task.
        previous = next(e for e in self.log["events"] if e["gate"] == "G3" and e["action"] == "review")
        previous["consultation"] = "coverage-r1-consultation.json"
        previous["consultation_sha256"] = self.case.write(previous["consultation"], self.consultation(previous))
        self.case.write("spec-qa.json", {"artifact": "spec.md", "revision": "task-r1", "verdict": "PASS", "findings": []})
        self.log["events"].append(self.case.workflow.event(
            self.case.workflow.plan[7], "task-r1", "review", "independent-spec-qa",
            reviewer="qa_spec", verdict="PASS", evidence="spec-qa.json"))
        self.attach()

    def blocked_review(self, gate):
        (self.reviewed_g3 if gate == "G3" else self.task_to_review)()
        event = self.log["events"][-1]
        event["verdict"] = "BLOCKED"
        findings = json.loads((self.root / event["evidence"]).read_bytes())
        findings.update(verdict="BLOCKED", findings=[{
            "id": "F-01", "severity": "blocker", "dimension": "Source verification",
            "evidence": "Required official source is inaccessible; external prerequisite unavailable",
            "recommendation": "Restore source access and verify it before resuming review"}])
        self.case.write(event["evidence"], findings)
        data = self.consultation()
        data["checks"][2].update(status="NOT_VERIFIED", revision="unavailable",
                                 observation="Required official source is inaccessible")
        self.attach(data)
        return event, findings

    def assert_blocked_is_terminal(self, gate):
        event, _ = self.blocked_review(gate)
        result = evaluate(self.log, self.root)
        self.assertEqual((result["gate"], result["status"]), (gate, "BLOCKED"))
        workflow = self.root / "blocked-workflow.json"
        workflow.write_text(json.dumps(self.log), encoding="utf-8")
        command = [sys.executable, "-B", str(test_coverage_pipeline.ROOT / "scripts/pipeline.py"),
                   str(workflow), "--project-root", str(self.root)]
        run = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)["status"], "BLOCKED")
        for action in ("approve", "complete", "submit"):
            with self.subTest(gate=gate, action=action):
                self.log["events"].append({**event, "action": action, "actor": "human"})
                with self.assertRaisesRegex(ValueError, "cannot advance a complete or blocked workflow"):
                    evaluate(self.log, self.root)
                self.log["events"].pop()

    def test_g3_blocked_reaches_terminal_state_and_cli_exit_two(self):
        self.assert_blocked_is_terminal("G3")

    def test_g6_blocked_reaches_terminal_state_and_cli_exit_two(self):
        self.assert_blocked_is_terminal("G6")

    def assert_blocked_bindings(self, gate):
        event, original = self.blocked_review(gate)
        for field, value in (("artifact", "different.json"), ("revision", "stale"),
                             ("verdict", "REWORK")):
            with self.subTest(gate=gate, field=field):
                self.case.write(event["evidence"], {**original, field: value})
                self.attach()
                with self.assertRaisesRegex(ValueError, "BLOCKED must match"):
                    evaluate(self.log, self.root)
        for severity in (None, "major"):
            with self.subTest(gate=gate, severity=severity):
                invalid = copy.deepcopy(original)
                invalid["findings"] = [] if severity is None else invalid["findings"]
                if severity:
                    invalid["findings"][0]["severity"] = severity
                self.case.write(event["evidence"], invalid)
                self.attach()
                with self.assertRaisesRegex(ValueError, "BLOCKED exige ao menos um achado blocker"):
                    evaluate(self.log, self.root)
        self.case.write(event["evidence"], original)
        self.attach()
        consultation = event.pop("consultation")
        with self.assertRaisesRegex(ValueError, "consultation"):
            evaluate(self.log, self.root)
        event["consultation"] = consultation
        event["consultation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "consultation"):
            evaluate(self.log, self.root)
        self.attach()
        changed = copy.deepcopy(original)
        changed["findings"][0]["recommendation"] = "Changed unblock recommendation"
        self.case.write(event["evidence"], changed)
        with self.assertRaisesRegex(ValueError, "findings hash mismatch"):
            evaluate(self.log, self.root)

    def test_g3_blocked_preserves_findings_and_consultation_bindings(self):
        self.assert_blocked_bindings("G3")

    def test_g6_blocked_preserves_findings_and_consultation_bindings(self):
        self.assert_blocked_bindings("G6")

    def test_new_mode_rejects_empty_pass_without_consultation(self):
        self.case.discovery_to_review()
        self.case.qa()
        with self.assertRaisesRegex(ValueError, "consultation"):
            evaluate(self.log, self.root)

    def test_g3_pass_compares_independent_approved_inventory(self):
        self.reviewed_g3()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")
        self.case.workflow.approve(self.case.workflow.plan[4], "coverage-r1")
        self.assertEqual(evaluate(self.log, self.root)["gate"], "G4")

    def test_legacy_omitted_prd_requirement_passes_but_new_review_blocks(self):
        self.case.coverage["requirement_ids"].remove("REQ-02")
        self.case.coverage["flows"][0]["requirement_ids"].remove("REQ-02")
        self.reviewed_g3()
        legacy = copy.deepcopy(self.log)
        legacy.pop("review_version")
        self.assertEqual(evaluate(legacy, self.root)["status"], "AWAITING_APPROVAL")
        with self.assertRaisesRegex(ValueError, "approved inventory"):
            evaluate(self.log, self.root)

    def test_wrong_actor_revision_hash_path_and_approval_binding(self):
        self.reviewed_g3()
        original = self.consultation()
        for field, value in (("reviewed_by", "someone-else"), ("revision", "old"),
                             ("artifact", "other.json"), ("findings_sha256", "0" * 64)):
            with self.subTest(field=field):
                changed = copy.deepcopy(original)
                changed[field] = value
                self.attach(changed)
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.root)
        for field, value in (("path", "../escape"), ("path", "review.md"), ("sha256", "0" * 64)):
            changed = copy.deepcopy(original)
            changed["references"][1][field] = value
            self.attach(changed)
            with self.subTest(reference=field), self.assertRaises(ValueError):
                evaluate(self.log, self.root)
        self.attach(original)
        self.log["events"][-1]["consultation_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            evaluate(self.log, self.root)

    def test_contradicted_rule_inaccessible_source_and_unpinned_guide_block_pass(self):
        self.reviewed_g3()
        original = self.consultation()
        for kind, field, value in ((0, "status", "CONTRADICTED"), (2, "status", "NOT_VERIFIED"),
                                   (1, "source", "https://github.com/MatthewKerns/software-development-best-practices-guide/tree/main"),
                                   (0, "status", "N/A"), (2, "source", "../outside.md"),
                                   (2, "observation", "")):
            changed = copy.deepcopy(original)
            changed["checks"][kind][field] = value
            self.attach(changed)
            with self.subTest(kind=kind, field=field), self.assertRaises(ValueError):
                evaluate(self.log, self.root)

    def test_g6_pass_keeps_human_approval_required(self):
        self.task_to_review()
        result = evaluate(self.log, self.root)
        self.assertEqual((result["gate"], result["status"]), ("G6", "AWAITING_APPROVAL"))
        self.case.workflow.approve(self.case.workflow.plan[7], "task-r1")
        self.assertEqual(evaluate(self.log, self.root)["gate"], "G7")

    def test_g6_rejects_mismatched_inventory_or_missing_current_reference(self):
        self.task_to_review()
        original = self.consultation()
        changed = copy.deepcopy(original)
        changed["approved_inventory"]["requirement_ids"].append("REQ-03")
        self.attach(changed)
        with self.assertRaisesRegex(ValueError, "approved inventory"):
            evaluate(self.log, self.root)
        changed = copy.deepcopy(original)
        changed["references"] = [r for r in changed["references"] if r["kind"] != "discovery"]
        self.attach(changed)
        with self.assertRaisesRegex(ValueError, "missing required references"):
            evaluate(self.log, self.root)

    def test_current_normalized_actor_and_source_sections_are_accepted(self):
        self.reviewed_g3()
        event = self.log["events"][-1]
        event["actor"] = "  INDEPENDENT-QA "
        data = self.consultation()
        data["reviewed_by"] = "independent-qa"
        data["checks"][1]["source"] = data["checks"][1]["source"].replace("/tree/", "/blob/") + "/README.md#testing"
        data["checks"][1]["locator"] = "README.md, Testing"
        self.attach(data)
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")
        event["actor"] = "discovery"
        data["reviewed_by"] = "discovery"
        self.attach(data)
        with self.assertRaisesRegex(ValueError, "author cannot review"):
            evaluate(self.log, self.root)

    def test_rework_records_unresolved_sources_and_requires_new_bound_review(self):
        self.case.discovery_to_review()
        self.case.qa(verdict="REWORK")
        self.case.write("coverage-qa.json", {
            "artifact": "coverage.json", "revision": "coverage-r1", "verdict": "REWORK",
            "findings": [{"id": "F-01", "severity": "major", "dimension": "Source verification",
                          "evidence": "Required source unavailable", "recommendation": "Consult original before PASS"}]})
        data = self.consultation()
        data["comparison"]["contradicted_ids"] = ["RULE-01"]
        data["checks"][2].update(status="NOT_VERIFIED", revision="unavailable",
                                 observation="Official source could not be consulted")
        self.attach(data)
        self.assertEqual(evaluate(self.log, self.root)["status"], "REWORK")
        self.case.evidence[0]["limits"] = "New research snapshot resolves inaccessible source"
        self.case.submit_research("G3", "coverage-r2", suffix="-r2")
        # Keep the earlier findings snapshot; a new review cannot rewrite it.
        self.case.write("coverage-r2-qa.json", {
            "artifact": "coverage-r2.json", "revision": "coverage-r2", "verdict": "PASS", "findings": []})
        self.log["events"].append(self.case.workflow.event(
            self.case.workflow.plan[4], "coverage-r2", "review", "independent-qa",
            reviewer="qa_spec", verdict="PASS", evidence="coverage-r2-qa.json"))
        self.attach()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")
        stale = self.consultation()
        stale["revision"] = "coverage-r1"
        self.attach(stale)
        with self.assertRaisesRegex(ValueError, "revision"):
            evaluate(self.log, self.root)

    def test_g6_rework_preserves_receipts_when_active_task_updates_in_place(self):
        self.task_to_review()
        self.log["events"][-1]["verdict"] = "REWORK"
        self.case.write("spec-qa.json", {
            "artifact": "spec.md", "revision": "task-r1", "verdict": "REWORK",
            "findings": [{"id": "F-01", "severity": "major", "dimension": "Source verification",
                          "evidence": "Missing original source", "recommendation": "Consult source"}]})
        self.attach()
        self.assertEqual(evaluate(self.log, self.root)["status"], "REWORK")
        prior = next(e for e in reversed(self.log["events"]) if e["action"] == "submit")
        task = json.loads((self.root / "task.json").read_bytes())
        task["contract_revision"] += 1
        self.case.write("task.json", task)
        from render_task import render_task
        (self.root / "task.md").write_text(render_task(task), encoding="utf-8")
        hashes = {key: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
                  for key, path in prior["artifacts"].items()}
        self.log["events"].append(self.case.workflow.event(
            self.case.workflow.plan[7], "task-r2", "submit", "architecture",
            artifacts=prior["artifacts"].copy(), sha256=hashes,
            task_id=task["task_id"], contract_revision=task["contract_revision"]))
        self.case.write("spec-r2-qa.json", {
            "artifact": "spec.md", "revision": "task-r2", "verdict": "PASS", "findings": []})
        self.log["events"].append(self.case.workflow.event(
            self.case.workflow.plan[7], "task-r2", "review", "independent-spec-qa",
            reviewer="qa_spec", verdict="PASS", evidence="spec-r2-qa.json"))
        self.attach()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")

    def test_malformed_missing_empty_declarations_and_na_explanation(self):
        self.reviewed_g3()
        original = self.consultation()
        malformed = (None, [], {}, {"version": True}, {"version": 2})
        for data in malformed:
            event = self.log["events"][-1]
            event["consultation_sha256"] = self.case.write(event["consultation"], data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                evaluate(self.log, self.root)
        for field in ("references", "approved_inventory", "comparison", "checks"):
            data = copy.deepcopy(original)
            del data[field]
            self.attach(data)
            with self.subTest(field=field), self.assertRaises(ValueError):
                evaluate(self.log, self.root)
        data = copy.deepcopy(original)
        data["checks"][2].update(status="N/A", observation="")
        self.attach(data)
        with self.assertRaises(ValueError):
            evaluate(self.log, self.root)
        for value in ("../escape.json", "/absolute.json", "C:/outside.json"):
            self.log["events"][-1]["consultation"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate(self.log, self.root)

    def test_cli_enforces_receipt_in_new_mode(self):
        self.reviewed_g3()
        workflow = self.root / "workflow.json"
        command = [sys.executable, "-B", str(test_coverage_pipeline.ROOT / "scripts/pipeline.py"),
                   str(workflow), "--project-root", str(self.root)]
        workflow.write_text(json.dumps(self.log), encoding="utf-8")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.log["events"][-1].pop("consultation")
        workflow.write_text(json.dumps(self.log), encoding="utf-8")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("consultation", result.stdout)

    def test_unknown_or_boolean_versions_and_missing_coverage_are_rejected(self):
        for value in (True, False, 2, "1", None):
            self.log["review_version"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "review_version"):
                evaluate(self.log, self.root)
        self.log["review_version"] = 1
        self.log.pop("coverage_version")
        with self.assertRaisesRegex(ValueError, "coverage_version"):
            evaluate(self.log, self.root)
