# Contexto TFD · 1275 palavras · 2926 tokens (o200k_base)

"""Workflow regressions for explicitly authorized reviewed-task preparation."""

import copy
import hashlib
import json
import unittest

from tests import test_pipeline as fixtures
from pipeline import evaluate
from render_task import render_task


class TestReviewedDelivery(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPipeline()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.project = self.fixture.project
        self.log = self.fixture.log
        self.plan = self.fixture.plan
        self.log["preparation"] = {
            "mode": "reviewed_task", "authorization": "approval.md",
        }

    def submit(self, stage, revision):
        self.fixture.submit(stage, revision)
        if stage[0] == "G6":
            event = self.log["events"][-1]
            task = json.loads((self.project / event["artifacts"]["task"]).read_bytes())
            task["spec"] = event["artifacts"]["spec"]
            self.replace_task(task, event)

    def replace_task(self, task, event):
        for key, content in (
            ("task", json.dumps(task).encode("utf-8")),
            ("task_view", render_task(task, "task.json").encode("utf-8")),
        ):
            (self.project / event["artifacts"][key]).write_bytes(content)
            event["sha256"][key] = hashlib.sha256(content).hexdigest()

    def review(self, stage, revision, reviewer, verdict="PASS"):
        self.fixture.review(stage, revision, reviewer, verdict)
        if stage[0] == "G6" and verdict == "PASS":
            submission = next(event for event in reversed(self.log["events"])
                              if event["action"] == "submit")
            path = f"{revision}-findings.json"
            payload = {"artifact": submission["artifacts"]["spec"],
                       "revision": revision, "verdict": "PASS", "findings": []}
            (self.project / path).write_text(json.dumps(payload), encoding="utf-8")
            self.log["events"][-1]["evidence"] = path

    def advance(self, count):
        for index, stage in enumerate(self.plan[:count]):
            revision = f"revision-{index}"
            self.submit(stage, revision)
            for reviewer in stage[3]:
                self.review(stage, revision, reviewer)
            if stage[0] in ("G2", "G3", "G4", "G5"):
                self.complete(stage, revision)
            else:
                self.fixture.approve(stage, revision)

    def complete(self, stage, revision, actor="coordinator", evidence="review.md"):
        self.log["events"].append(self.fixture.event(
            stage, revision, "complete", actor, evidence=evidence))

    def test_authorized_preparation_reaches_g6_without_human_preparation_events(self):
        self.advance(7)
        result = evaluate(self.log, self.project)
        self.assertEqual((result["gate"], result["status"]), ("G6", "AWAITING_SUBMISSION"))
        terminal = [event for event in self.log["events"] if event["action"] == "complete"]
        self.assertEqual([event["gate"] for event in terminal], ["G2", "G3", "G4", "G5"])

    def test_preparation_configuration_fails_closed(self):
        valid = self.log["preparation"]
        cases = [None, False, [], "reviewed_task", {}, {"mode": "reviewed_task"},
                 {**valid, "mode": "automatic"}, {**valid, "extra": True}]
        for config in cases:
            with self.subTest(config=config):
                self.log["preparation"] = config
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.project)

    def test_authorization_must_be_nonempty_and_inside_project(self):
        (self.project / "empty.md").write_text(" \n\t", encoding="utf-8")
        paths = [None, "", "missing.md", "empty.md", "../approval.md",
                 "/approval.md", "C:/approval.md", "docs\\approval.md", "./"]
        for path in paths:
            with self.subTest(path=path):
                self.log["preparation"]["authorization"] = path
                with self.assertRaises((ValueError, OSError)):
                    evaluate(self.log, self.project)

    def test_complete_requires_opt_in(self):
        self.fixture.complete_prefix(3)
        stage = self.plan[3]
        self.submit(stage, "discovery")
        self.complete(stage, "discovery")
        self.log.pop("preparation")
        with self.assertRaises(ValueError):
            evaluate(self.log, self.project)

    def test_complete_requires_submission_current_revision_and_nonempty_evidence(self):
        self.advance(3)
        stage = self.plan[3]
        before = copy.deepcopy(self.log["events"])
        self.complete(stage, "unsubmitted")
        with self.assertRaisesRegex(ValueError, "current submitted revision"):
            evaluate(self.log, self.project)
        self.log["events"] = before
        self.submit(stage, "discovery")
        submitted = copy.deepcopy(self.log["events"])
        (self.project / "empty.md").write_text(" \n", encoding="utf-8")
        for revision, evidence in (("stale", "review.md"), ("discovery", "empty.md")):
            with self.subTest(revision=revision, evidence=evidence):
                self.log["events"] = copy.deepcopy(submitted)
                self.complete(stage, revision, evidence=evidence)
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.project)

    def test_complete_requires_all_qa_and_distinct_coordinator(self):
        self.advance(4)
        stage = self.plan[4]
        self.submit(stage, "reviewed-discovery")
        submitted = copy.deepcopy(self.log["events"])
        self.complete(stage, "reviewed-discovery")
        with self.assertRaises(ValueError):
            evaluate(self.log, self.project)
        self.log["events"] = submitted
        self.review(stage, "reviewed-discovery", "qa_spec")
        reviewed = copy.deepcopy(self.log["events"])
        for actor in (" Author ", " QA_SPEC "):
            with self.subTest(actor=actor):
                self.log["events"] = copy.deepcopy(reviewed)
                self.complete(stage, "reviewed-discovery", actor=actor)
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.project)
        self.log["events"] = reviewed
        self.complete(stage, "reviewed-discovery")
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G4")

    def test_complete_never_replaces_retained_human_gates(self):
        for stage_index in (0, 1, 2, 7, 8, 9, 10):
            with self.subTest(gate=self.plan[stage_index][0]):
                self.log["events"] = []
                self.advance(stage_index)
                stage = self.plan[stage_index]
                revision = f"forbidden-{stage_index}"
                self.submit(stage, revision)
                for reviewer in stage[3]:
                    self.review(stage, revision, reviewer)
                self.complete(stage, revision)
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.project)

    def test_g6_accepts_bound_structured_pass_but_still_waits_for_human(self):
        self.advance(7)
        stage = self.plan[7]
        self.submit(stage, "current-spec")
        self.review(stage, "current-spec", "qa_spec")
        result = evaluate(self.log, self.project)
        self.assertEqual((result["gate"], result["status"]), ("G6", "AWAITING_APPROVAL"))
        self.fixture.approve(stage, "current-spec")
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G7")

    def test_g6_rejects_text_malformed_wrong_verdict_artifact_and_revision(self):
        self.advance(7)
        stage = self.plan[7]
        self.submit(stage, "current-spec")
        self.review(stage, "current-spec", "qa_spec")
        path = self.project / self.log["events"][-1]["evidence"]
        valid = json.loads(path.read_text(encoding="utf-8"))
        blocking = {"id": "F-01", "severity": "major", "dimension": "rastreabilidade",
                    "evidence": "Missing current acceptance", "recommendation": "Link acceptance"}
        cases = ["PASS", "{", "[]", json.dumps({**valid, "unknown": True}),
                 json.dumps({**valid, "artifact": "another-spec.md"}),
                 json.dumps({**valid, "revision": "stale"}),
                 json.dumps({**valid, "verdict": "REWORK", "findings": [blocking]}),
                 json.dumps({**valid, "findings": [blocking]})]
        for content in cases:
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    evaluate(self.log, self.project)

    def test_g6_task_must_name_submitted_spec_even_with_valid_pass(self):
        self.advance(7)
        stage = self.plan[7]
        self.submit(stage, "current-spec")
        submission = self.log["events"][-1]
        original = json.loads((self.project / "task.json").read_bytes())
        self.review(stage, "current-spec", "qa_spec")
        for spec in (None, "other-spec.md"):
            with self.subTest(spec=spec):
                task = copy.deepcopy(original)
                if spec is None:
                    task.pop("spec")
                else:
                    task["spec"] = spec
                self.replace_task(task, submission)
                with self.assertRaisesRegex(ValueError, "task.spec"):
                    evaluate(self.log, self.project)
        self.replace_task(original, submission)
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")

    def test_manual_workflow_keeps_legacy_text_review_and_optional_task_spec(self):
        self.log.pop("preparation")
        self.fixture.complete_prefix(7)
        stage = self.plan[7]
        self.fixture.submit(stage, "legacy-spec")
        self.fixture.review(stage, "legacy-spec", "qa_spec")
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")

    def test_rework_resets_reviews_and_keeps_three_replacement_limit(self):
        self.advance(7)
        stage = self.plan[7]
        for attempt in range(4):
            revision = f"spec-attempt-{attempt}"
            self.submit(stage, revision)
            result = evaluate(self.log, self.project)
            self.assertEqual(result["pending_reviewers"], ["qa_spec"])
            self.review(stage, revision, "qa_spec", "REWORK")
            self.assertEqual(evaluate(self.log, self.project)["status"],
                             "REWORK" if attempt < 3 else "BLOCKED")

    def test_preparatory_rework_needs_fresh_qa_before_completion(self):
        self.advance(4)
        stage = self.plan[4]
        self.submit(stage, "research-first")
        self.review(stage, "research-first", "qa_spec", "REWORK")
        self.submit(stage, "research-corrected")
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_QA")
        self.complete(stage, "research-corrected")
        with self.assertRaisesRegex(ValueError, "current QA"):
            evaluate(self.log, self.project)
        self.log["events"].pop()
        self.review(stage, "research-corrected", "qa_spec")
        self.complete(stage, "research-corrected")
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G4")

    def test_g7_rework_requires_fresh_applicable_qa_and_human_approval(self):
        self.advance(8)
        stage = self.plan[8]
        self.submit(stage, "implementation-first")
        self.review(stage, "implementation-first", "qa_backend")
        self.review(stage, "implementation-first", "qa_ui", "REWORK")
        self.submit(stage, "implementation-corrected")
        self.assertEqual(evaluate(self.log, self.project)["pending_reviewers"],
                         ["qa_backend", "qa_ui", "security"])
        self.fixture.approve(stage, "implementation-corrected")
        with self.assertRaisesRegex(ValueError, "current QA"):
            evaluate(self.log, self.project)
        self.log["events"].pop()
        for reviewer in stage[3]:
            self.review(stage, "implementation-corrected", reviewer)
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")
        self.fixture.approve(stage, "implementation-corrected")
        self.assertEqual(evaluate(self.log, self.project)["gate"], "G8-review")

    def test_opted_in_full_workflow_preserves_g7_qa_and_final_human_approval(self):
        self.advance(8)
        stage = self.plan[8]
        self.submit(stage, "implementation")
        self.review(stage, "implementation", "qa_backend")
        self.assertEqual(evaluate(self.log, self.project)["pending_reviewers"], ["qa_ui", "security"])
        self.review(stage, "implementation", "qa_ui")
        self.review(stage, "implementation", "security")
        self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")
        self.fixture.approve(stage, "implementation")
        for stage in self.plan[9:]:
            revision = stage[0]
            self.submit(stage, revision)
            self.assertEqual(evaluate(self.log, self.project)["status"], "AWAITING_APPROVAL")
            self.fixture.approve(stage, revision)
        self.assertEqual(evaluate(self.log, self.project), {"status": "COMPLETE"})
