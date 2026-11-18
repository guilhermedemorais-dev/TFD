"""Stage-loop fixtures exercise receipts, never real deployment or source consultation."""

import copy
import hashlib
import json
import sys
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import test_qa_consultation
from pipeline import evaluate, stages, require_task_context
from stage_loop import artifact_bindings, require_knowledge
from pipeline import require_file


class TestStageLoop(unittest.TestCase):
    def setUp(self):
        self.fixture = test_qa_consultation.TestQAConsultation()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.task_to_review()
        self.log, self.root = self.fixture.log, self.fixture.root
        self.plan = stages(self.log["phases"], stage_loop=True)
        self.counter = 0
        self.write("canonical.md", "Approved fixture scope, not a consultation claim")
        self.write("navigation.json", {"status": "GRAPHIFY", "notice": "Synthetic navigation fixture"})
        original = list(self.log["events"])
        self.log["events"] = []
        self.log["stage_loop_version"] = 1
        submitted = None
        for event in original:
            gate = event["gate"]
            if event["action"] == "submit":
                submitted = event
                self.attach(event, submitted)
            elif event["action"] == "review":
                self.attach(event, submitted, event["reviewer"])
            elif event["action"] == "approve" and gate == "G2":
                event.update(action="handoff", artifacts=submitted["artifacts"], sha256=submitted["sha256"])
            elif event["action"] == "approve" and gate in {"G0", "G0.5", "G1", "G5"}:
                reviewer = "qa_backend" if gate == "G0.5" else "qa_spec"
                self.review(submitted, reviewer)
            self.log["events"].append(event)
        self.task_submission = submitted
        self.task = json.loads((self.root / submitted["artifacts"]["task"]).read_bytes())
        self.check = {"command": "fixture check (not a production command)", "exit": 0,
                      "result": "PASS", "observation": "Synthetic verified fixture"}

    def write(self, path, value):
        contents = value if isinstance(value, bytes) else (value.encode() if isinstance(value, str) else json.dumps(value, ensure_ascii=False).encode())
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
        return hashlib.sha256(contents).hexdigest()

    def knowledge(self):
        return {"navigation": {"method": "graphify", "query": "fixture stage requirements",
                               "evidence": "navigation.json", "sha256": self.sha("navigation.json"), "status": "GRAPHIFY"},
                "sources": [{"kind": "project", "path": "canonical.md", "sha256": self.sha("canonical.md"),
                             "revision": "fixture-r1", "locator": "Scope", "status": "VERIFIED",
                             "observation": "Checked fixture scope"}]}

    def sha(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def attach(self, event, submit, role="author"):
        self.counter += 1
        path = f"receipts/stage-{self.counter}.json"
        data = {"version": 1, "actor": event["actor"], "role": role, "gate": event["gate"],
                "phase": event.get("phase"), "revision": event["revision"],
                "artifacts": artifact_bindings(submit["artifacts"], submit["sha256"]),
                "knowledge": self.knowledge(),
                "checks": [{"command": "fixture check (not executed)", "exit": 0,
                            "result": "PASS", "observation": "Synthetic declaration fixture"}]}
        if role != "author":
            data["findings_sha256"] = self.sha(event["evidence"])
        event.update(stage_receipt=path, stage_receipt_sha256=self.write(path, data))
        return data

    def receipt(self, event):
        return json.loads((self.root / event["stage_receipt"]).read_bytes())

    def replace_receipt(self, event, data):
        event["stage_receipt_sha256"] = self.write(event["stage_receipt"], data)

    def review(self, submitted, role, verdict="PASS"):
        evidence = f"qa/{submitted['revision']}-{role}.md"
        self.write(evidence, "Synthetic independent finding; no runtime deployment")
        event = dict(gate=submitted["gate"], phase=submitted.get("phase"), revision=submitted["revision"],
                     action="review", actor="independent-" + role, reviewer=role, verdict=verdict, evidence=evidence)
        self.attach(event, submitted, role)
        self.log["events"].append(event)
        return event

    def terminal(self, submitted, action="approve"):
        path = f"approval/{submitted['revision']}.md"
        self.write(path, "Synthetic explicit approval fixture")
        event = dict(gate=submitted["gate"], phase=submitted.get("phase"), revision=submitted["revision"],
                     action=action, actor="human" if action == "approve" else "coordinator", evidence=path)
        if submitted["gate"] == "G9":
            candidate = json.loads((self.root / submitted["artifacts"]["release_candidate"]).read_bytes())
            auth = {"version": 1, "action": "deploy", "actor": "human", "revision": submitted["revision"],
                    "release": candidate, "attempt": self.deploy_attempt(), "observation": "Fixture authorization only"}
            event["deploy_authorization"] = f"approval/{submitted['revision']}-deploy.json"
            event["deploy_authorization_sha256"] = self.write(event["deploy_authorization"], auth)
        self.log["events"].append(event)
        return event

    def deploy_attempt(self):
        return 1 + sum(e["gate"] == "G10" and e["action"] == "submit" for e in self.log["events"])

    def execution(self, attempt):
        evidence = f"execution/item-{attempt}.md"
        code = self.write(evidence, "Synthetic completed checklist observation")
        reviews, items = {}, {}
        for micro in self.task["microtasks"]:
            if micro["phase"] != "stock":
                continue
            items[micro["id"]] = [{"status": "verified", "evidence": evidence, "sha256": code}
                                   for _ in micro["checklist"]]
            reviews[micro["id"]] = dict(role=micro["validator"], reviewer="independent-mt-qa", executor="backend",
                                        verdict="PASS", attempt=attempt, evidence=evidence, evidence_sha256=code,
                                        observation="Synthetic MT check")
        checkpoint = {"task_id": self.task["task_id"], "contract_revision": self.task["contract_revision"],
                      "phase": "stock", "attempt": attempt, "task_sha256": self.task_submission["sha256"]["task"],
                      "items": items, "rework": {}, "invalidated": {}}
        snapshot = {"task_id": self.task["task_id"], "contract_revision": self.task["contract_revision"],
                    "sector_receipts": {"backend": {"reviews": reviews}}}
        return checkpoint, snapshot

    def submit(self, gate, revision=None):
        stage = next(stage for stage in self.plan if stage[0] == gate)
        revision = revision or gate + "-r1"
        artifacts = {key: f"artifacts/{revision}-{key}.json" for key in stage[2]}
        values = {key: "Synthetic stage output" for key in stage[2]}
        if gate == "G7":
            attempt = 1 + sum(e["gate"] == "G7" and e["action"] == "submit" for e in self.log["events"])
            values["execution_checkpoint"], values["sector_receipts"] = self.execution(attempt)
            values["task_snapshot"] = (self.root / self.task_submission["artifacts"]["task"]).read_bytes()
        if gate == "G9":
            self.write("release/candidate.bin", "Synthetic immutable candidate")
            values["release_candidate"] = {"candidate": "release/candidate.bin",
                                           "candidate_sha256": self.sha("release/candidate.bin"), "target": "fixture-only"}
        if gate == "G10":
            approval = next(e for e in reversed(self.log["events"]) if e["gate"] == "G9" and e["action"] == "approve")
            auth = json.loads((self.root / approval["deploy_authorization"]).read_bytes())
            result = {"release": auth["release"], "attempt": self.deploy_attempt(),
                      "authorization": {"path": approval["deploy_authorization"], "sha256": approval["deploy_authorization_sha256"]},
                      "checks": [self.check]}
            values = {key: copy.deepcopy(result) for key in stage[2]}
        hashes = {key: self.write(path, values[key]) for key, path in artifacts.items()}
        event = dict(gate=gate, phase=stage[1], revision=revision, action="submit", actor="author-" + gate,
                     artifacts=artifacts, sha256=hashes)
        self.attach(event, event)
        self.log["events"].append(event)
        return event

    def advance(self, target="G10"):
        if self.log["events"][-1]["gate"] == "G6":
            self.terminal(self.task_submission)
        for gate in ("G7", "G8-review", "G8", "G9", "G10"):
            event = self.submit(gate)
            if gate == target:
                return event
            for role in next(s[3] for s in self.plan if s[0] == gate):
                self.review(event, role)
            self.terminal(event)

    def test_gate_matrix_and_legacy_default(self):
        actual = {gate: reviews for gate, _, _, reviews in self.plan}
        for gate in ("G0", "G1", "G4", "G5", "G6", "G8-review"):
            self.assertEqual(actual[gate], ("qa_spec",))
        self.assertEqual(actual["G0.5"], ("qa_backend",))
        self.assertEqual(actual["G8"], ("qa_spec", "qa_ui"))
        self.assertEqual(actual["G9"], ("qa_backend", "security"))
        self.assertEqual(actual["G10"], ("qa_backend", "security", "qa_ui"))
        self.assertEqual(stages(self.log["phases"])[-1][0], "G8")

    def test_full_new_mode_requires_qa_then_authorized_terminal_completion(self):
        deployment = self.advance()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        for role in ("qa_backend", "security", "qa_ui"):
            self.review(deployment, role)
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")
        self.terminal(deployment, "complete")
        self.assertEqual(evaluate(self.log, self.root), {"status": "COMPLETE"})

    def test_new_stages_cannot_skip_independent_qa_or_receipts(self):
        self.advance()
        original = copy.deepcopy(self.log)
        for event in original["events"]:
            if event["action"] not in {"submit", "review"}:
                continue
            self.log = copy.deepcopy(original)
            index = original["events"].index(event)
            self.log["events"][index].pop("stage_receipt")
            with self.subTest(gate=event["gate"], action=event["action"]):
                with self.assertRaisesRegex(ValueError, "evidence|stage"):
                    evaluate(self.log, self.root)
        self.log = copy.deepcopy(original)
        review = next(e for e in self.log["events"] if e["gate"] == "G0.5" and e["action"] == "review")
        self.log["events"].remove(review)
        with self.assertRaisesRegex(ValueError, "current QA"):
            evaluate(self.log, self.root)

    def test_receipt_rejects_actor_revision_artifact_source_and_exit_tampering(self):
        event = self.log["events"][0]
        original = self.receipt(event)
        for field, value in (("actor", "someone-else"), ("revision", "old"), ("artifacts", {}), ("checks", [])):
            data = copy.deepcopy(original)
            data[field] = value
            self.replace_receipt(event, data)
            with self.subTest(field=field), self.assertRaises(ValueError):
                evaluate(self.log, self.root)
        data = copy.deepcopy(original)
        data["checks"][0].update(exit=1, result="FAIL")
        self.replace_receipt(event, data)
        with self.assertRaisesRegex(ValueError, "unresolved"):
            evaluate(self.log, self.root)
        self.replace_receipt(event, original)
        self.write("canonical.md", "Changed source")
        with self.assertRaisesRegex(ValueError, "canonical source changed"):
            evaluate(self.log, self.root)

    def test_fallback_reuse_and_bundle_sources_require_bound_evidence(self):
        knowledge = self.knowledge()
        navigation = knowledge["navigation"]
        navigation.update(method="lexical", status="INDEX_STALE")
        navigation["sha256"] = self.write("navigation.json", {"status": "INDEX_STALE"})
        with self.assertRaisesRegex(ValueError, "fallback"):
            require_knowledge(knowledge, self.root, require_file)
        navigation["reason"] = "Bundle index fingerprint differs; canonical lexical sources opened"
        require_knowledge(knowledge, self.root, require_file)
        navigation.update(method="reuse", status="VERIFIED", revision="fixture-r1", applicability="Same scope and source revision",
                          original_navigation="navigation-original.json")
        navigation["original_navigation_sha256"] = self.write("navigation-original.json", {"status": "GRAPHIFY"})
        navigation["sha256"] = self.write("navigation.json", {"status": "VERIFIED"})
        require_knowledge(knowledge, self.root, require_file)
        source_path = "skills/TFD-backend/SKILL.md"
        source = knowledge["sources"][0]
        source.update(kind="bundle", path=source_path, sha256=hashlib.sha256((Path(__file__).resolve().parents[1] / source_path).read_bytes()).hexdigest())
        require_knowledge(knowledge, self.root, require_file)
        navigation["original_navigation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "original navigation changed"):
            require_knowledge(knowledge, self.root, require_file)

    def test_graphify_uses_actual_adapter_status_and_remote_sources_bind_local_observation(self):
        from tests import test_graphify_retrieval
        graph_fixture = test_graphify_retrieval.GraphifyRetrievalTests()
        graph_fixture.setUp()
        self.addCleanup(graph_fixture.doCleanups)
        graph_fixture.cached()
        with patch.object(test_graphify_retrieval.graph, "worker", return_value="Fixture graph context"):
            observed = graph_fixture.query(python=Path(sys.executable))
        self.assertEqual(observed["status"], "GRAPHIFY")
        knowledge = self.knowledge()
        navigation = knowledge["navigation"]
        navigation["sha256"] = self.write("navigation.json", observed)
        require_knowledge(knowledge, self.root, require_file)
        navigation["status"] = "OK"
        navigation["sha256"] = self.write("navigation.json", {"status": "OK"})
        with self.assertRaisesRegex(ValueError, "actual Graphify status"):
            require_knowledge(knowledge, self.root, require_file)
        navigation.update(method="lexical", status="GRAPHIFY_UNAVAILABLE", reason="Graph engine unavailable; canonical sources opened")
        navigation["sha256"] = self.write("navigation.json", {"status": "GRAPHIFY_UNAVAILABLE"})
        source = knowledge["sources"][0]
        source.update(kind="remote", origin="https://docs.python.org/3/library/hashlib.html")
        require_knowledge(knowledge, self.root, require_file)
        source["origin"] = "http://docs.python.org/3/library/hashlib.html"
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            require_knowledge(knowledge, self.root, require_file)

    def test_empty_phase_plan_cannot_finish_new_workflow(self):
        index = next(i for i, event in enumerate(self.log["events"]) if event["gate"] == "G5")
        self.log["events"] = self.log["events"][:index+1]
        self.log["phases"] = []
        with self.assertRaisesRegex(ValueError, "at least one planned phase"):
            evaluate(self.log, self.root)

    def test_author_failure_records_rework_and_cannot_be_passed(self):
        submit = self.log["events"][0]
        self.log["events"] = self.log["events"][:1]
        data = self.receipt(submit)
        data["checks"][0].update(exit=1, result="FAIL", observation="Observed self-check failure")
        self.replace_receipt(submit, data)
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        review = self.review(submit, "qa_spec")
        with self.assertRaisesRegex(ValueError, "unresolved author"):
            evaluate(self.log, self.root)
        self.log["events"].remove(review)
        review = self.review(submit, "qa_spec", "REWORK")
        data = self.receipt(review)
        data["checks"][0].update(exit=1, result="FAIL", observation="Independently reproduced failure")
        self.replace_receipt(review, data)
        self.assertEqual(evaluate(self.log, self.root)["status"], "REWORK")

    def test_g10_requires_all_qa_and_preserves_authorization_before_completion(self):
        deployment = self.advance()
        self.review(deployment, "qa_backend")
        completion = self.terminal(deployment, "complete")
        with self.assertRaisesRegex(ValueError, "current QA"):
            evaluate(self.log, self.root)
        self.log["events"].remove(completion)
        self.review(deployment, "security")
        self.review(deployment, "qa_ui")
        self.terminal(deployment, "complete")
        self.assertEqual(evaluate(self.log, self.root)["status"], "COMPLETE")
        auth = next(e for e in self.log["events"] if e["gate"] == "G9" and e["action"] == "approve")
        self.write(auth["deploy_authorization"], {"action": "changed"})
        with self.assertRaisesRegex(ValueError, "authorization"):
            evaluate(self.log, self.root)

    def test_g2_handoff_binds_bundle_and_cannot_approve_or_self_handoff(self):
        handoff = next(e for e in self.log["events"] if e["gate"] == "G2" and e["action"] == "handoff")
        original = copy.deepcopy(handoff)
        for action in ("approve", "complete"):
            handoff["action"] = action
            with self.assertRaisesRegex(ValueError, "internal handoff"):
                evaluate(self.log, self.root)
        handoff.update(original)
        handoff["sha256"] = {}
        with self.assertRaisesRegex(ValueError, "exact Discovery"):
            evaluate(self.log, self.root)
        handoff.update(original, actor="discovery")
        with self.assertRaisesRegex(ValueError, "own work"):
            evaluate(self.log, self.root)

    def test_old_consultation_remains_required_at_g3_and_g6(self):
        for gate in ("G3", "G6"):
            event = next(e for e in self.log["events"] if e["gate"] == gate and e["action"] == "review")
            value = event.pop("consultation")
            with self.subTest(gate=gate), self.assertRaisesRegex(ValueError, "consultation"):
                evaluate(self.log, self.root)
            event["consultation"] = value

    def test_historical_g6_receipts_survive_active_task_update_in_place(self):
        from render_task import render_task
        review = self.log["events"][-1]
        review["verdict"] = "REWORK"
        self.write(review["evidence"], {"artifact": "spec.md", "revision": review["revision"], "verdict": "REWORK",
                                      "findings": [{"id": "F-01", "severity": "major", "dimension": "Source verification",
                                                    "evidence": "Missing source", "recommendation": "Consult source"}]})
        self.fixture.attach()
        self.attach(review, self.task_submission, "qa_spec")
        author_receipt = self.receipt(self.task_submission)
        author_receipt["knowledge"]["sources"].append({"kind": "project", "path": "task.json",
            "sha256": self.sha("task.json"), "revision": "contract-1", "locator": "requirements",
            "observation": "Checked submitted Task", "status": "VERIFIED"})
        self.replace_receipt(self.task_submission, author_receipt)
        self.assertEqual(evaluate(self.log, self.root)["status"], "REWORK")
        self.task["contract_revision"] += 1
        self.write("task.json", self.task)
        self.write("task.md", render_task(self.task))
        submitted = copy.deepcopy(self.task_submission)
        submitted.update(revision="task-r2", contract_revision=self.task["contract_revision"],
                         sha256={key: self.sha(path) for key, path in submitted["artifacts"].items()})
        self.attach(submitted, submitted)
        self.log["events"].append(submitted)
        review = self.review(submitted, "qa_spec")
        self.write(review["evidence"], {"artifact": "spec.md", "revision": "task-r2", "verdict": "PASS", "findings": []})
        self.fixture.attach()
        self.attach(review, submitted, "qa_spec")
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_APPROVAL")

    def test_g7_requires_current_verified_checkpoint_and_mt_pass(self):
        submit = self.advance("G7")
        for key, mutate in (
                ("execution_checkpoint", lambda data: data["items"]["MT-01"].clear()),
                ("sector_receipts", lambda data: data["sector_receipts"]["backend"]["reviews"]["MT-01"].update(attempt=2)),
                ("sector_receipts", lambda data: data["sector_receipts"]["backend"]["reviews"]["MT-01"].update(verdict="REWORK"))):
            path = submit["artifacts"][key]
            original = json.loads((self.root / path).read_bytes())
            changed = copy.deepcopy(original)
            mutate(changed)
            submit["sha256"][key] = self.write(path, changed)
            self.attach(submit, submit)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "stage loop"):
                evaluate(self.log, self.root)
            submit["sha256"][key] = self.write(path, original)
            self.attach(submit, submit)
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")

    def test_g7_invalidated_dependency_pass_is_rejected(self):
        submit = self.advance("G7")
        snapshot = json.loads((self.root / submit["artifacts"]["sector_receipts"]).read_bytes())
        review = snapshot["sector_receipts"]["backend"]["reviews"]["MT-02"]
        fingerprint = hashlib.sha256(json.dumps(review, sort_keys=True).encode() + (self.root / review["evidence"]).read_bytes()).hexdigest()
        path = submit["artifacts"]["execution_checkpoint"]
        data = json.loads((self.root / path).read_bytes())
        data["invalidated"]["MT-02"] = fingerprint
        submit["sha256"]["execution_checkpoint"] = self.write(path, data)
        self.attach(submit, submit)
        with self.assertRaisesRegex(ValueError, "invalidated"):
            evaluate(self.log, self.root)

    def historical_execution(self):
        from render_task import render_task
        self.log["phases"].append({"id": "second", "backend": True, "ui": True, "security": True})
        self.plan = stages(self.log["phases"], stage_loop=True)
        self.task["phases"].append({"id": "second", "title": "Second phase"})
        self.task["microtasks"][1]["phase"] = "second"
        self.write("task.json", self.task)
        self.write("task.md", render_task(self.task))
        planning = next(e for e in self.log["events"] if e["gate"] == "G5" and e["action"] == "submit")
        planning["sha256"]["phase_plan"] = self.write(planning["artifacts"]["phase_plan"], self.log["phases"])
        for event in self.log["events"]:
            if event["gate"] == "G5" and event["action"] in {"submit", "review"}:
                self.attach(event, planning, event.get("reviewer", "author"))
        first = self.task_submission
        first["sha256"] = {key: self.sha(path) for key, path in first["artifacts"].items()}
        self.fixture.attach()
        self.attach(first, first)
        self.attach(self.log["events"][-1], first, "qa_spec")
        execution = self.advance("G7")
        for role in ("qa_backend", "qa_ui", "security"):
            self.review(execution, role)
        self.terminal(execution)
        self.task["contract_revision"] += 1
        self.task["microtasks"][0]["checklist"].append("Later revision has another check")
        self.write("task.json", self.task)
        self.write("task.md", render_task(self.task))
        second = copy.deepcopy(first)
        second.update(phase="second", revision="task-second-r2", contract_revision=self.task["contract_revision"],
                      sha256={key: self.sha(path) for key, path in first["artifacts"].items()})
        self.attach(second, second)
        self.log["events"].append(second)
        return execution

    def rebind_execution(self, execution):
        for event in self.log["events"]:
            if event["gate"] == "G7" and event.get("phase") == "stock" and event["action"] in {"submit", "review"}:
                self.attach(event, execution, event.get("reviewer", "author"))

    def test_every_historical_g7_uses_its_approved_task_snapshot(self):
        execution = self.historical_execution()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        # Matching declared hashes cannot hide a structurally invalid old checkpoint.
        execution["sha256"]["execution_checkpoint"] = self.write(execution["artifacts"]["execution_checkpoint"], {})
        self.rebind_execution(execution)
        with self.assertRaisesRegex(ValueError, "checkpoint does not match"):
            evaluate(self.log, self.root)

    def test_historical_g6_review_inventory_matches_its_frozen_phase_task(self):
        self.historical_execution()
        self.assert_historical_review_inventory()

    def legacy_historical_execution(self):
        execution = self.historical_execution()
        self.log.pop("stage_loop_version")
        self.log["events"] = [event for event in self.log["events"] if not (
            event["action"] == "review" and event["gate"] in {"G0", "G0.5", "G1", "G5"})]
        for event in self.log["events"]:
            if event["action"] == "handoff":
                event["action"] = "approve"
        return execution

    def test_review_version_without_stage_loop_binds_historical_inventory(self):
        self.legacy_historical_execution()
        self.assert_historical_review_inventory()

    def test_review_version_rejects_missing_authentic_historical_task(self):
        execution = self.legacy_historical_execution()
        execution["artifacts"].pop("task_snapshot")
        execution["sha256"].pop("task_snapshot")
        with self.assertRaisesRegex(ValueError, "authentic historical Task"):
            evaluate(self.log, self.root)

    def test_review_version_binds_available_historical_task_without_snapshot(self):
        from render_task import render_task
        execution = self.legacy_historical_execution()
        contents = (self.root / execution["artifacts"].pop("task_snapshot")).read_bytes()
        execution["sha256"].pop("task_snapshot")
        task = json.loads(contents)
        self.write("task.json", contents)
        self.write("task.md", render_task(task))
        current = self.log["events"][-1]
        current["contract_revision"] = task["contract_revision"]
        current["sha256"] = {key: self.sha(path) for key, path in current["artifacts"].items()}
        self.assert_historical_review_inventory()

    def test_workflow_without_review_version_keeps_legacy_snapshot_optional(self):
        execution = self.legacy_historical_execution()
        self.log.pop("review_version")
        execution["artifacts"].pop("task_snapshot")
        execution["sha256"].pop("task_snapshot")
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")

    def test_review_version_accepts_unchanged_task_without_snapshot(self):
        self.terminal(self.task_submission)
        execution = self.submit("G7")
        self.log.pop("stage_loop_version")
        self.log["events"] = [event for event in self.log["events"] if not (
            event["action"] == "review" and event["gate"] in {"G0", "G0.5", "G1", "G5"})]
        for event in self.log["events"]:
            if event["action"] == "handoff":
                event["action"] = "approve"
        execution["artifacts"].pop("task_snapshot")
        execution["sha256"].pop("task_snapshot")
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")

    def assert_historical_review_inventory(self):
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        review = next(e for e in self.log["events"] if e["gate"] == "G6" and e["action"] == "review")
        original = json.loads((self.root / review["consultation"]).read_bytes())
        for field, values in (("requirement_ids", ["REQ-01"]),
                              ("requirement_ids", ["REQ-01", "REQ-02", "REQ-03"]),
                              ("business_rule_ids", []),
                              ("business_rule_ids", ["RULE-01", "RULE-02"])):
            with self.subTest(field=field, values=values):
                data = copy.deepcopy(original)
                data["approved_inventory"][field] = values
                # Keep the declaration internally valid so only the task binding detects the drift.
                claims = data["approved_inventory"]["business_rule_ids"] or ["REQ-01"]
                for check in data["checks"]:
                    check["claim_ids"] = claims
                review["consultation_sha256"] = self.write(review["consultation"], data)
                with self.assertRaisesRegex(ValueError, "approved inventory"):
                    evaluate(self.log, self.root)
        review["consultation_sha256"] = self.write(review["consultation"], original)
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")

    def test_historical_task_snapshot_cannot_be_replaced_with_active_contract(self):
        execution = self.historical_execution()
        path = execution["artifacts"]["task_snapshot"]
        execution["sha256"]["task_snapshot"] = self.write(path, (self.root / "task.json").read_bytes())
        self.rebind_execution(execution)
        with self.assertRaisesRegex(ValueError, "approved G6 task hash"):
            evaluate(self.log, self.root)

    def replace_historical_contract(self, execution, task):
        submitted = next(e for e in self.log["events"] if e["gate"] == "G6" and e.get("phase") == "stock" and e["action"] == "submit")
        task_hash = self.write(execution["artifacts"]["task_snapshot"], task)
        submitted["sha256"]["task"] = execution["sha256"]["task_snapshot"] = task_hash
        path = execution["artifacts"]["execution_checkpoint"]
        checkpoint = json.loads((self.root / path).read_bytes())
        checkpoint["task_sha256"] = task_hash
        execution["sha256"]["execution_checkpoint"] = self.write(path, checkpoint)
        for event in self.log["events"]:
            if event["gate"] == "G6" and event.get("phase") == "stock" and event["action"] in {"submit", "review"}:
                if event["action"] == "review":
                    consultation = json.loads((self.root / event["consultation"]).read_bytes())
                    for reference in consultation["references"]:
                        if reference["kind"] == "task":
                            reference["sha256"] = task_hash
                    event["consultation_sha256"] = self.write(event["consultation"], consultation)
                self.attach(event, submitted, event.get("reviewer", "author"))
        self.rebind_execution(execution)

    def test_historical_task_spec_must_match_its_g6_submission(self):
        execution = self.historical_execution()
        self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
        task = json.loads((self.root / execution["artifacts"]["task_snapshot"]).read_bytes())
        task["spec"] = "different-spec.md"
        self.replace_historical_contract(execution, task)
        with self.assertRaisesRegex(ValueError, "task.spec must match"):
            evaluate(self.log, self.root)

    def test_historical_requirement_inventory_must_match_reviewed_discovery(self):
        execution = self.historical_execution()
        task = json.loads((self.root / execution["artifacts"]["task_snapshot"]).read_bytes())
        requirement = {**task["requirements"][0], "id": "REQ-03"}
        task["requirements"].append(requirement)
        task["acceptance_criteria"][0]["requirement_ids"].append("REQ-03")
        self.replace_historical_contract(execution, task)
        with self.assertRaisesRegex(ValueError, "requirements must match reviewed"):
            evaluate(self.log, self.root)

    def test_historical_rule_inventory_must_match_reviewed_discovery(self):
        execution = self.historical_execution()
        task = json.loads((self.root / execution["artifacts"]["task_snapshot"]).read_bytes())
        task["business_rules"].append({**task["business_rules"][0], "id": "RULE-02"})
        task["acceptance_criteria"][0]["rule_ids"].append("RULE-02")
        task["technical_coverage"]["business"]["rule_ids"].append("RULE-02")
        self.replace_historical_contract(execution, task)
        with self.assertRaisesRegex(ValueError, "business_rules must match reviewed"):
            evaluate(self.log, self.root)

    def test_shared_g6_context_rejects_area_phase_order_and_discovery_drift(self):
        submitted = self.task_submission
        research = next(e for e in self.log["events"] if e["gate"] == "G3" and e["action"] == "submit")
        coverage = self.fixture.case.coverage
        context = (research["artifacts"], research["sha256"])
        def check(task, artifacts=submitted["artifacts"], hashes=submitted["sha256"], phases=None, reviewed=None):
            require_task_context(task, artifacts, hashes, phases or self.log["phases"],
                                 reviewed or coverage, context, require_spec=True, coverage_required=True)
        check(self.task)
        changed = copy.deepcopy(coverage)
        changed["areas"]["backend"]["status"] = "N/A"
        with self.assertRaisesRegex(ValueError, "backend requires reviewed Discovery"):
            check(self.task, reviewed=changed)
        with self.assertRaisesRegex(ValueError, "G5 plan order"):
            check(self.task, phases=[{"id": "later"}, {"id": "stock"}])
        hashes = {**submitted["sha256"], "discovery": "0" * 64}
        with self.assertRaisesRegex(ValueError, "G3 reviewed coverage"):
            check(self.task, hashes=hashes)

    def test_g9_requires_specific_human_candidate_target_authorization(self):
        submit = self.advance("G9")
        for role in ("qa_backend", "security"):
            self.review(submit, role)
        approval = self.terminal(submit)
        auth = json.loads((self.root / approval["deploy_authorization"]).read_bytes())
        auth["release"]["target"] = "different-target"
        approval["deploy_authorization_sha256"] = self.write(approval["deploy_authorization"], auth)
        with self.assertRaisesRegex(ValueError, "explicit deploy authorization"):
            evaluate(self.log, self.root)

    def test_malformed_deploy_authorization_actor_is_controlled_cli_error(self):
        submit = self.advance("G9")
        for role in ("qa_backend", "security"):
            self.review(submit, role)
        approval = self.terminal(submit)
        path = approval["deploy_authorization"]
        auth = json.loads((self.root / path).read_bytes())
        auth["actor"] = ["invalid actor"]
        approval["deploy_authorization_sha256"] = self.write(path, auth)
        workflow = self.root / "workflow.json"
        self.write("workflow.json", self.log)
        script = Path(__file__).resolve().parents[1] / "scripts/pipeline.py"
        result = subprocess.run([sys.executable, "-B", str(script), str(workflow), "--project-root", str(self.root)],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("explicit deploy authorization", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_g10_rejects_retargeting_and_failed_checks_cannot_pass_qa(self):
        submit = self.advance()
        path = submit["artifacts"]["post_deploy_checks"]
        original = json.loads((self.root / path).read_bytes())
        for mutation in ("target", "checks"):
            value = copy.deepcopy(original)
            if mutation == "target":
                value["release"]["target"] = "different-target"
            else:
                value["checks"][0].update(exit=1, result="FAIL")
            submit["sha256"]["post_deploy_checks"] = self.write(path, value)
            self.attach(submit, submit)
            if mutation == "target":
                with self.assertRaisesRegex(ValueError, "stage loop"):
                    evaluate(self.log, self.root)
            else:
                self.assertEqual(evaluate(self.log, self.root)["status"], "AWAITING_QA")
                review = self.review(submit, "qa_backend")
                with self.assertRaisesRegex(ValueError, "verified PASS"):
                    evaluate(self.log, self.root)
                self.log["events"].remove(review)
                self.review(submit, "qa_backend", "REWORK")
                self.assertEqual(evaluate(self.log, self.root)["gate"], "G9")

    def test_g10_rework_requires_fresh_g9_and_has_bounded_retry(self):
        deployment = self.advance()
        for attempt in range(1, 5):
            self.review(deployment, "qa_backend", "REWORK")
            state = evaluate(self.log, self.root)
            if attempt == 4:
                self.assertEqual(state["status"], "BLOCKED")
                break
            self.assertEqual((state["gate"], state["status"]), ("G9", "AWAITING_SUBMISSION"))
            release = self.submit("G9", f"release-r{attempt+1}")
            for role in ("qa_backend", "security"):
                self.review(release, role)
            self.terminal(release)
            deployment = self.submit("G10", f"deployment-r{attempt+1}")

    def test_versions_must_be_explicit_and_compatible(self):
        for value in (True, "1", 2, None):
            self.log["stage_loop_version"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "stage_loop_version"):
                evaluate(self.log, self.root)
        self.log["stage_loop_version"] = 1
        self.log.pop("review_version")
        with self.assertRaisesRegex(ValueError, "requires"):
            evaluate(self.log, self.root)


if __name__ == "__main__":
    unittest.main()
