# Contexto TFD · 969 palavras · 2275 tokens (o200k_base)

"""Sector contract integration and simulated receipts, not live model discovery."""

import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pipeline import require_file, stages
from stage_loop import require_stage_receipt


ROLES = "product devops discovery architecture frontend backend database documentation qa_spec qa_backend qa_ui security ui_ux".split()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestStageSectorContracts(unittest.TestCase):
    def test_all_tool_using_skills_resolve_the_same_conditional_contract(self):
        shared = ROOT / "skills/TFD-harness/references/stage-loop.md"
        for role in [*ROLES, "harness"]:
            with self.subTest(role=role):
                skill = ROOT / "skills" / ("TFD-" + role) / "SKILL.md"
                text = skill.read_text(encoding="utf-8")
                links = re.findall(r"\[[^\]]+\]\(([^)]+stage-loop\.md)\)", text)
                self.assertEqual(len(links), 1)
                self.assertEqual((skill.parent / links[0]).resolve(), shared.resolve())
                self.assertIn("stage_loop_version: 1", text)
                self.assertLessEqual(len(text.splitlines()), 150)
                description = next(line for line in text.splitlines() if line.startswith("description:"))
                self.assertLessEqual(len(description.split()) - 1, 60)

    def test_two_declared_positive_routes_and_one_foreign_route_per_sector(self):
        # These are static discovery surfaces, not a claim about host model routing.
        agents = {role: json.loads((ROOT / "agents" / ("TFD-" + role) / "agent.json").read_text(encoding="utf-8")) for role in ROLES}
        for role, agent in agents.items():
            with self.subTest(role=role):
                first, second = agent["activates_on"][:2]
                self.assertNotEqual(first, second)
                self.assertTrue(first.strip() and second.strip())
                foreign = agents["product" if role != "product" else "backend"]["activates_on"][0]
                self.assertNotIn(foreign, agent["activates_on"])
                for name in agent["skills"]:
                    self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())

    def test_runtime_gate_reviewers_have_matching_agent_contracts(self):
        phases = [{"id": "module", "backend": True, "ui": True, "security": True}]
        plan = stages(phases, stage_loop=True)
        for gate, _, _, reviewers in plan:
            for reviewer in reviewers:
                with self.subTest(gate=gate, reviewer=reviewer):
                    agent = json.loads((ROOT / "agents" / ("TFD-" + reviewer) / "agent.json").read_text(encoding="utf-8"))
                    self.assertIn(gate, agent["gate"].split("/"))
        by_gate = {gate: reviewers for gate, _, _, reviewers in plan}
        self.assertEqual(by_gate["G0.5"], ("qa_backend",))
        self.assertEqual(by_gate["G1"], ("qa_spec",))
        self.assertEqual(by_gate["G8"], ("qa_spec", "qa_ui"))
        self.assertNotIn("qa_spec", by_gate["G7"])
        for role, validator in (("devops", "TFD-qa_backend"), ("documentation", "TFD-qa_spec")):
            agent = json.loads((ROOT / "agents" / ("TFD-" + role) / "agent.json").read_text(encoding="utf-8"))
            self.assertEqual(agent["validator"], validator)

    def test_every_new_g7_requires_approved_task_snapshot_and_legacy_stays_unchanged(self):
        phases = [{"id": phase, "backend": True, "ui": False, "security": False} for phase in ("first", "second")]
        current = [stage for stage in stages(phases, stage_loop=True) if stage[0] == "G7"]
        legacy = [stage for stage in stages(phases) if stage[0] == "G7"]
        self.assertEqual([stage[1] for stage in current], ["first", "second"])
        for _, phase, artifacts, reviewers in current:
            with self.subTest(phase=phase):
                self.assertTrue({"task_snapshot", "execution_checkpoint", "sector_receipts"} <= set(artifacts))
                self.assertEqual(reviewers, ("qa_backend",))
        for _, _, artifacts, _ in legacy:
            self.assertEqual(artifacts, ("implementation", "self_tests"))


class TestExecutedStageReceiptScenarios(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.project = Path(temp.name)
        self.artifact = self.project / "deliverable.json"
        self.artifact.write_text(json.dumps({"technical_role": "administrator", "tutorial_roles": ["administrator", "user"]}), encoding="utf-8")
        self.nav = self.project / "navigation.json"
        self.nav.write_text(json.dumps({"status": "INDEX_STALE", "scenario": "simulated navigation for receipt validation"}), encoding="utf-8")
        self.report = self.project / "review.txt"
        self.report.write_text("Observed access policy in the JSON deliverable; browser behavior untested.", encoding="utf-8")
        # Execute a real bounded check against the fixture; never pretend it is UI QA.
        command = [sys.executable, "-B", "-c",
                   "import json,sys; d=json.load(open(sys.argv[1])); assert d['technical_role']=='administrator'; assert set(d['tutorial_roles'])=={'administrator','user'}",
                   str(self.artifact)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.check = {"command": subprocess.list2cmdline(command), "exit": result.returncode,
                      "result": "PASS", "observation": "Fixture policy checked; no browser or network consultation claimed."}
        source = ROOT / "skills/TFD-harness/references/stage-loop.md"
        self.knowledge = {
            "navigation": {"method": "lexical", "query": "stage receipt bindings", "evidence": self.nav.name,
                           "sha256": sha(self.nav), "status": "INDEX_STALE", "reason": "Simulated stale index; canonical bundle source opened directly."},
            "sources": [{"kind": "bundle", "path": source.relative_to(ROOT).as_posix(), "sha256": sha(source),
                         "revision": "current-test-content", "locator": "Source-backed production stages",
                         "observation": "Defines independent current-revision evidence.", "status": "VERIFIED"}],
        }

    def event(self, gate, role):
        artifacts = {"deliverable": self.artifact.name}
        hashes = {"deliverable": sha(self.artifact)}
        event = {"gate": gate, "phase": None, "revision": "r1", "actor": "author" if role == "author" else "independent-reviewer",
                 "evidence": self.report.name, "verdict": "PASS"}
        receipt = {"version": 1, "gate": gate, "phase": None, "revision": "r1", "actor": event["actor"], "role": role,
                   "artifacts": {"deliverable": {"path": self.artifact.name, "sha256": hashes["deliverable"]}},
                   "knowledge": copy.deepcopy(self.knowledge), "checks": [self.check], "findings_sha256": sha(self.report)}
        path = self.project / "receipt.json"
        path.write_text(json.dumps(receipt), encoding="utf-8")
        event.update(stage_receipt=path.name, stage_receipt_sha256=sha(path))
        return event, artifacts, hashes, receipt

    def test_readiness_author_receipt_binds_executed_self_check(self):
        event, artifacts, hashes, _ = self.event("G0.5", "author")
        receipt = require_stage_receipt(event, artifacts, hashes, self.project, require_file)
        self.assertEqual(receipt["checks"][0]["exit"], 0)

    def test_documentation_reviewer_receipt_binds_own_source_and_report(self):
        event, artifacts, hashes, _ = self.event("G8", "qa_spec")
        receipt = require_stage_receipt(event, artifacts, hashes, self.project, require_file, role="qa_spec")
        self.assertEqual(receipt["findings_sha256"], sha(self.report))

    def test_author_receipt_cannot_be_replayed_as_independent_documentation_review(self):
        event, artifacts, hashes, _ = self.event("G8", "author")
        with self.assertRaisesRegex(ValueError, "role"):
            require_stage_receipt(event, artifacts, hashes, self.project, require_file, role="qa_spec")

    def test_changed_review_report_invalidates_current_pass(self):
        event, artifacts, hashes, _ = self.event("G8", "qa_spec")
        self.report.write_text("Changed report", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "findings hash"):
            require_stage_receipt(event, artifacts, hashes, self.project, require_file, role="qa_spec")

    def test_changed_canonical_source_invalidates_current_pass(self):
        event, artifacts, hashes, receipt = self.event("G8", "qa_spec")
        source = self.project / "accepted-policy.json"
        source.write_bytes(self.artifact.read_bytes())
        receipt["knowledge"]["sources"].append({
            "kind": "project", "path": source.name, "sha256": sha(source), "revision": "accepted-r1",
            "locator": "technical_role", "observation": "Accepted access policy checked directly.", "status": "VERIFIED"})
        path = self.project / event["stage_receipt"]
        path.write_text(json.dumps(receipt), encoding="utf-8")
        event["stage_receipt_sha256"] = sha(path)
        require_stage_receipt(event, artifacts, hashes, self.project, require_file, role="qa_spec")
        source.write_text('{"technical_role": "user"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "canonical source changed"):
            require_stage_receipt(event, artifacts, hashes, self.project, require_file, role="qa_spec")


if __name__ == "__main__":
    unittest.main()
