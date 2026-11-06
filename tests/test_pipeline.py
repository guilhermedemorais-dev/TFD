import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pipeline import evaluate, stages
from render_task import render_task


class TestPipeline(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.project = Path(tmp.name)
        self.log = {"phases": [{"id": "stock", "backend": True, "ui": True, "security": True}], "events": []}
        self.plan = stages(self.log["phases"])
        (self.project / "review.md").write_text("Observed QA outcome", encoding="utf-8")
        (self.project / "approval.md").write_text("Explicit human approval", encoding="utf-8")

    def event(self, stage, revision, action, actor, **data):
        gate, phase, _, _ = stage
        return dict(gate=gate, phase=phase, revision=revision, action=action, actor=actor, **data)

    def submit(self, stage, revision):
        artifacts, hashes = {}, {}
        metadata = {}
        if stage[0] == "G6":
            task = json.loads((ROOT / "examples/task.example.json").read_bytes())
            task["contract_revision"] += sum(event["gate"] == "G6" and event["action"] == "submit"
                                             for event in self.log["events"])
            metadata = {key: task[key] for key in ("task_id", "contract_revision")}
        for key in stage[2]:
            path = f"{revision}-{key}.json"
            if key == "task":
                path = "task.json"
                content = json.dumps(task).encode("utf-8")
            elif key == "task_view":
                path = "task.md"
                content = render_task(task).encode("utf-8")
            elif key == "phase_plan":
                content = json.dumps(self.log["phases"]).encode()
            else:
                content = b"observed"
            (self.project / path).write_bytes(content)
            artifacts[key] = path
            hashes[key] = hashlib.sha256(content).hexdigest()
        self.log["events"].append(self.event(stage, revision, "submit", "author", artifacts=artifacts, sha256=hashes, **metadata))

    def review(self, stage, revision, role, verdict="PASS", actor=None):
        self.log["events"].append(self.event(
            stage, revision, "review", actor or role, reviewer=role, verdict=verdict, evidence="review.md"))

    def approve(self, stage, revision):
        self.log["events"].append(self.event(stage, revision, "approve", "human", evidence="approval.md"))

    def complete_prefix(self, count):
        for i, stage in enumerate(self.plan[:count]):
            rev = f"rev{i}"
            self.submit(stage, rev)
            for reviewer in stage[3]:
                self.review(stage, rev, reviewer)
            self.approve(stage, rev)

    def test_full_workflow_requires_current_evidence_and_final_approval(self):
        self.complete_prefix(len(self.plan) - 1)
        final = self.plan[-1]
        self.submit(final, "final")
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")
        self.approve(final, "final")
        self.assertEqual(evaluate(self.log, self.project), {"status": "COMPLETE"})

    def test_g7_waits_for_all_independent_reviewers(self):
        self.complete_prefix(8)
        stage = self.plan[8]
        self.submit(stage, "implementation")
        self.review(stage, "implementation", "qa_backend")
        self.assertEqual(evaluate(self.log, self.project)["pending_reviewers"], ["qa_ui", "security"])
        self.approve(stage, "implementation")
        with self.assertRaisesRegex(ValueError, "current QA"):
            evaluate(self.log, self.project)

    def test_three_unsuccessful_reworks_block_the_stage(self):
        self.complete_prefix(7)
        stage = self.plan[7]
        for attempt in range(4):
            rev = f"spec{attempt}"
            self.submit(stage, rev)
            self.review(stage, rev, "qa_spec", "REWORK")
            self.assertEqual(evaluate(self.log, self.project)["status"], "REWORK" if attempt < 3 else "BLOCKED")

    def test_disabling_ui_after_plan_approval_is_rejected(self):
        self.complete_prefix(7)
        self.log["phases"][0]["ui"] = False
        with self.assertRaisesRegex(ValueError, "submitted G5 plan"):
            evaluate(self.log, self.project)

    def test_workflow_can_start_before_phases_are_known(self):
        self.log["phases"] = []
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G0")
        self.complete_prefix(6)
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G5")
        self.submit(self.plan[6], "empty-plan")
        with self.assertRaisesRegex(ValueError, "at least one planned phase"):
            evaluate(self.log, self.project)

    def test_rework_rejects_a_review_from_the_previous_revision(self):
        self.complete_prefix(7)
        stage = self.plan[7]
        self.submit(stage, "spec1")
        self.review(stage, "spec1", "qa_spec", "REWORK")
        self.submit(stage, "spec2")
        self.review(stage, "spec1", "qa_spec")
        with self.assertRaisesRegex(ValueError, "current submitted revision"):
            evaluate(self.log, self.project)

    def test_rework_keeps_one_active_task_and_rejects_duplicate_paths(self):
        self.complete_prefix(7)
        stage = self.plan[7]
        self.submit(stage, "spec1")
        self.review(stage, "spec1", "qa_spec", "REWORK")
        self.submit(stage, "spec2")
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_QA")
        self.assertEqual(sorted(path.name for path in self.project.glob("task.*")), ["task.json", "task.md"])
        self.log["events"][-1]["artifacts"]["task"] = "task-v2.json"
        with self.assertRaisesRegex(ValueError, "update the existing task"):
            evaluate(self.log, self.project)

    def test_gate_rejects_self_review_and_changed_artifacts(self):
        self.complete_prefix(7)
        stage = self.plan[7]
        self.submit(stage, "spec1")
        self.review(stage, "spec1", "qa_spec", actor=" Author ")
        with self.assertRaisesRegex(ValueError, "own work"):
            evaluate(self.log, self.project)
        self.log["events"].pop()
        (self.project / "spec1-spec.json").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            evaluate(self.log, self.project)

    def test_g6_requires_view_from_the_same_task_revision(self):
        self.complete_prefix(7)
        self.submit(self.plan[7], "spec1")
        event = self.log["events"][-1]
        view_path = event["artifacts"].pop("task_view")
        event["sha256"].pop("task_view")
        with self.assertRaisesRegex(ValueError, "requires artifacts: .*task_view"):
            evaluate(self.log, self.project)

        task = json.loads((ROOT / "examples/task.example.json").read_bytes())
        task["contract_revision"] += 1
        stale_view = render_task(task).encode("utf-8")
        (self.project / view_path).write_bytes(stale_view)
        event["artifacts"]["task_view"] = view_path
        event["sha256"]["task_view"] = hashlib.sha256(stale_view).hexdigest()
        with self.assertRaisesRegex(ValueError, "generated from the submitted task JSON"):
            evaluate(self.log, self.project)

    def test_all_architecture_sectors_have_bounded_skills_and_routes(self):
        names = ("product", "discovery", "architecture", "database", "backend", "frontend",
                 "ui_ux", "qa_spec", "qa_backend", "qa_ui", "security", "devops", "documentation")
        for sector in names:
            with self.subTest(sector=sector):
                name = f"TFD-{sector}"
                agent = json.loads((ROOT / f"agents/{name}/agent.json").read_text(encoding="utf-8"))
                text = (ROOT / f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(agent["sector"], sector)
                self.assertEqual(agent["skills"], [name])
                self.assertNotEqual(agent["validator"], name)
                self.assertGreaterEqual(len(agent["activates_on"]), 2)
                self.assertNotIn("escrever um anúncio publicitário", agent["activates_on"])
                self.assertLessEqual(len(text.splitlines()), 150)
                self.assertLessEqual(len(agent["description"].split()), 60)
