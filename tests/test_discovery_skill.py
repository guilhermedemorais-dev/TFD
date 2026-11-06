import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "TFD-discovery"
SOURCE = {
    "id": "SRC-01", "location": "docs/reference.md",
    "revision": "r1", "status": "verified",
}
OBSERVED = {
    "id": "EV-01", "claim": "A tela mostra o saldo", "class": "OBSERVED",
    "limits": "Só o fluxo visível", "source_id": "SRC-01", "locator": "Tela de estoque",
}


class TestDiscovery(unittest.TestCase):
    def test_resource_index_resolves_to_verified_files_inside_plugin(self):
        library = ROOT / "library"
        index = json.loads((library / "indexes/resources.json").read_text(encoding="utf-8"))
        self.assertTrue(index["resources"])
        for resource in index["resources"]:
            with self.subTest(resource=resource["id"]):
                path = (library / resource["path"]).resolve()
                self.assertTrue(path.is_relative_to(library.resolve()))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), resource["sha256"])

    def test_skill_budget_and_static_routes(self):
        lines = (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines()
        description = next(line.split(":", 1)[1] for line in lines if line.startswith("description:"))
        self.assertLessEqual(len(lines), 150)
        self.assertLessEqual(len(description.split()), 60)
        agent = json.loads((ROOT / "agents/TFD-discovery/agent.json").read_text(encoding="utf-8"))
        for trigger in ("fazer discovery do módulo", "investigar uma lacuna apontada pelo QA de spec"):
            self.assertIn(trigger, agent["activates_on"])
        self.assertNotIn("implementar endpoint de pedido", agent["activates_on"])

    def test_evidence_cli_distinguishes_valid_invalid_and_blocked(self):
        unknown = {
            "id": "EV-02", "claim": "Como o saldo é persistido?", "class": "UNKNOWN",
            "limits": "Sem acesso ao servidor",
        }
        cases = (
            ([SOURCE], [OBSERVED], 0, "OK"),
            ([], [], 1, "registre pelo menos um achado"),
            ([SOURCE, SOURCE], [OBSERVED], 1, "duplicado"),
            ([SOURCE], [{**OBSERVED, "class": "CONFIRMED"}], 1, "classe"),
            ([], [OBSERVED], 1, "fonte verificada"),
            ([{**SOURCE, "status": "stale"}], [OBSERVED], 1, "fonte verificada"),
            ([], [{**unknown, "essential": False}], 0, "OK"),
            ([], [{**unknown, "essential": True}], 2, "BLOCKED: EV-02"),
        )
        with tempfile.TemporaryDirectory() as temp:
            sources_path = Path(temp) / "sources.json"
            evidence_path = Path(temp) / "evidence.json"
            for sources, evidence, code, message in cases:
                with self.subTest(sources=sources, evidence=evidence):
                    sources_path.write_text(json.dumps(sources), encoding="utf-8")
                    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, "-B", str(SKILL / "scripts/check_evidence.py"),
                         str(sources_path), str(evidence_path)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                    self.assertIn(message, result.stdout)
