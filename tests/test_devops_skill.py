"""Check the published DevOps routing metadata and its incident guide."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTOR = ROOT / "skills" / "TFD-devops"
AGENT = ROOT / "agents" / "TFD-devops" / "agent.json"


class DevOpsRoutingTests(unittest.TestCase):
    def test_github_access_and_ci_failures_route_to_devops(self):
        agent = json.loads(AGENT.read_text(encoding="utf-8"))
        for request in ("diagnosticar falha de acesso ao GitHub", "corrigir permissões do CI no GitHub Actions"):
            with self.subTest(request=request):
                self.assertIn(request, agent["activates_on"])
        self.assertNotIn("corrigir regra de cálculo no backend", agent["activates_on"])

    def test_incident_guide_is_reachable_from_skill(self):
        skill = (SECTOR / "SKILL.md").read_text(encoding="utf-8")
        guide = "references/github-access-recovery.md"
        self.assertIn(f"]({guide})", skill)
        self.assertTrue((SECTOR / guide).is_file())
