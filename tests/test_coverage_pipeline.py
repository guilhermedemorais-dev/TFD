"""Exercise coverage QA through real workflow entry points with local fixtures."""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from tests.test_discovery_coverage import fixture as coverage_fixture
from tests import test_pipeline


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pipeline import evaluate


class TestCoveragePipeline(unittest.TestCase):
    def setUp(self):
        self.workflow = test_pipeline.TestPipeline()
        self.workflow.setUp()
        self.addCleanup(self.workflow.doCleanups)
        self.workflow.complete_prefix(3)
        self.log = self.workflow.log
        self.root = self.workflow.project
        self.log["coverage_version"] = 1
        self.sources, self.evidence, self.coverage = coverage_fixture()
        self.coverage["requirement_ids"].append("REQ-02")
        self.coverage["flows"][0]["requirement_ids"].append("REQ-02")

    def write(self, name, value):
        content = json.dumps(value, ensure_ascii=False).encode()
        (self.root / name).write_bytes(content)
        return hashlib.sha256(content).hexdigest()

    def submit_research(self, gate, revision, *, suffix=""):
        files = {
            "sources": (f"sources{suffix}.json", self.sources),
            "evidence": (f"evidence{suffix}.json", self.evidence),
            "coverage": (f"coverage{suffix}.json", self.coverage),
            "findings": (f"findings{suffix}.json", {"scope": "local fixture"}),
        }
        artifacts = {key: name for key, (name, _) in files.items()}
        hashes = {key: self.write(name, value) for key, (name, value) in files.items()}
        stage = self.workflow.plan[3 if gate == "G2" else 4]
        self.log["events"].append(self.workflow.event(
            stage, revision, "submit", "discovery", artifacts=artifacts, sha256=hashes))
        return artifacts

    def discovery_to_review(self):
        artifacts = self.submit_research("G2", "research-r1")
        self.workflow.approve(self.workflow.plan[3], "research-r1")
        self.submit_research("G3", "coverage-r1")
        return artifacts

    def qa(self, verdict="PASS", *, artifact="coverage.json", revision="coverage-r1"):
        receipt = {"artifact": artifact, "revision": revision, "verdict": verdict, "findings": []}
        self.write("coverage-qa.json", receipt)
        self.log["events"].append(self.workflow.event(
            self.workflow.plan[4], revision, "review", "independent-qa",
            reviewer="qa_spec", verdict=verdict, evidence="coverage-qa.json"))

    def ready_for_task(self):
        self.discovery_to_review()
        self.qa()
        self.workflow.approve(self.workflow.plan[4], "coverage-r1")
        for i in (5, 6):
            stage = self.workflow.plan[i]
            self.workflow.submit(stage, f"stage-{i}")
            for reviewer in stage[3]:
                self.workflow.review(stage, f"stage-{i}", reviewer)
            self.workflow.approve(stage, f"stage-{i}")

    def submit_task(self, mutate=None):
        self.ready_for_task()
        task = json.loads((ROOT / "examples/task-coverage.example.json").read_bytes())
        if "phases" in task:
            task["phases"] = [{"id": "stock", "title": "Implementar cadastro"}]
            for micro in task["microtasks"]:
                micro["phase"] = "stock"
        task["spec"] = "spec.md"
        if mutate:
            mutate(task)
        from render_task import render_task
        self.write("task.json", task)
        (self.root / "task.md").write_text(render_task(task), encoding="utf-8")
        (self.root / "spec.md").write_text("Reviewed phase contract fixture", encoding="utf-8")
        artifacts = {"spec": "spec.md", "discovery": "coverage.json", "task": "task.json", "task_view": "task.md"}
        hashes = {key: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
                  for key, path in artifacts.items()}
        self.log["events"].append(self.workflow.event(
            self.workflow.plan[7], "task-r1", "submit", "architecture",
            artifacts=artifacts, sha256=hashes, task_id=task["task_id"],
            contract_revision=task["contract_revision"]))

    def test_init_enables_coverage_and_cannot_overwrite(self):
        path = self.root / "new-workflow.json"
        command = [sys.executable, "-B", str(ROOT / "scripts/pipeline.py"),
                   str(path), "--init", "--project-root", str(self.root)]
        first = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertEqual(json.loads(path.read_bytes())["coverage_version"], 1)
        self.assertEqual(json.loads(path.read_bytes())["review_version"], 1)
        self.assertEqual(json.loads(path.read_bytes())["stage_loop_version"], 1)
        second = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)

    def test_new_g2_requires_coverage(self):
        self.workflow.submit(self.workflow.plan[3], "shallow")
        with self.assertRaisesRegex(ValueError, "coverage"):
            evaluate(self.log, self.root)

    def test_g3_waits_for_independent_coverage_review(self):
        self.discovery_to_review()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        self.qa()
        self.workflow.approve(self.workflow.plan[4], "coverage-r1")
        self.assertEqual(evaluate(self.log, self.root)["gate"], "G4")

    def test_unknown_area_cannot_pass_g3(self):
        self.coverage["areas"]["backend"].update(status="UNKNOWN", reason="Missing API contract", evidence_ids=[])
        self.discovery_to_review()
        self.qa()
        with self.assertRaisesRegex(ValueError, "unresolved Discovery"):
            evaluate(self.log, self.root)

    def test_qa_receipt_must_name_the_coverage(self):
        self.discovery_to_review()
        self.qa(artifact="different.json")
        with self.assertRaisesRegex(ValueError, "PASS must match"):
            evaluate(self.log, self.root)

    def test_research_changes_after_submission_cannot_pass(self):
        self.discovery_to_review()
        self.sources[0]["revision"] = "changed"
        self.write("sources.json", self.sources)
        self.qa()
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            evaluate(self.log, self.root)

    def test_author_cannot_review_coverage(self):
        self.discovery_to_review()
        self.qa()
        self.log["events"][-1]["actor"] = "discovery"
        with self.assertRaisesRegex(ValueError, "author cannot review"):
            evaluate(self.log, self.root)

    def test_rework_uses_new_research_snapshots(self):
        self.discovery_to_review()
        self.qa(verdict="REWORK")
        self.evidence[0]["limits"] = "Clarified scope after independent review"
        self.submit_research("G3", "coverage-r2", suffix="-r2")
        self.qa(artifact="coverage-r2.json", revision="coverage-r2")
        self.workflow.approve(self.workflow.plan[4], "coverage-r2")
        self.assertEqual(evaluate(self.log, self.root)["gate"], "G4")

    def test_g6_accepts_a_task_bound_to_reviewed_coverage(self):
        self.submit_task()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")

    def test_g6_cannot_pass_with_an_unbound_text_receipt(self):
        self.submit_task()
        self.workflow.review(self.workflow.plan[7], "task-r1", "qa_spec")
        with self.assertRaises((ValueError, json.JSONDecodeError)):
            evaluate(self.log, self.root)

    def test_autonomous_preparation_still_waits_for_human_task_approval(self):
        self.log["preparation"] = {"mode": "reviewed_task", "authorization": "approval.md"}
        self.submit_task()
        for event in self.log["events"]:
            if event["gate"] in ("G2", "G3", "G4", "G5") and event["action"] == "approve":
                event.update(action="complete", actor="coordinator")
        self.write("spec-qa.json", {
            "artifact": "spec.md", "revision": "task-r1", "verdict": "PASS", "findings": []})
        self.log["events"].append(self.workflow.event(
            self.workflow.plan[7], "task-r1", "review", "independent-spec-qa",
            reviewer="qa_spec", verdict="PASS", evidence="spec-qa.json"))
        result = evaluate(self.log, self.root)
        self.assertEqual((result["gate"], result["status"]), ("G6", "AWAITING_APPROVAL"))

    def test_g6_rejects_legacy_task_in_new_workflow(self):
        def remove(task):
            task.pop("coverage_version", None)
            task.pop("technical_coverage", None)
        self.submit_task(remove)
        with self.assertRaisesRegex(ValueError, "coverage"):
            evaluate(self.log, self.root)

    def test_g6_rejects_a_new_requirement_without_discovery(self):
        def extra(task):
            for req in task["requirements"]:
                if req["id"] == "REQ-02":
                    req["id"] = "REQ-03"
            for ac in task["acceptance_criteria"]:
                ac["requirement_ids"] = ["REQ-03" if value == "REQ-02" else value
                                         for value in ac["requirement_ids"]]
        self.submit_task(extra)
        with self.assertRaisesRegex(ValueError, "must match reviewed Discovery"):
            evaluate(self.log, self.root)

    def test_g6_rejects_omission_of_a_reviewed_business_rule(self):
        def omit(task):
            task["business_rules"] = []
            task["technical_coverage"]["business"]["rule_ids"] = []
            for ac in task["acceptance_criteria"]:
                ac["rule_ids"] = []
        self.submit_task(omit)
        with self.assertRaisesRegex(ValueError, "business_rules must match reviewed Discovery"):
            evaluate(self.log, self.root)

    def test_g6_rejects_a_different_discovery_snapshot(self):
        self.submit_task()
        self.write("unreviewed.json", self.coverage)
        event = self.log["events"][-1]
        event["artifacts"]["discovery"] = "unreviewed.json"
        with self.assertRaisesRegex(ValueError, "G3 reviewed coverage"):
            evaluate(self.log, self.root)
