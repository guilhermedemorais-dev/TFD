# Contexto TFD · 665 palavras · 1660 tokens (o200k_base)

"""Testes da skill TFD-qa_spec e do validador de findings.

Rode: python -m unittest tests.test_qa_spec_skill -v
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "TFD-qa_spec" / "SKILL.md"
CHECKLIST = ROOT / "skills" / "TFD-qa_spec" / "references" / "review-checklist.md"
CHECKER = ROOT / "skills" / "TFD-qa_spec" / "scripts" / "check_findings.py"
AGENT = ROOT / "agents" / "TFD-qa_spec" / "agent.json"

ACTIVATES = [
    "revisar a spec antes de implementar",
    "revisar o PRD e o discovery antes do código",
]
NAO_ATIVA = "implementar endpoint de pedido"

VALID_FINDINGS = {
    "artifact": "docs/specs/pedido/spec.md",
    "revision": "r3",
    "verdict": "REWORK",
    "findings": [
        {
            "id": "F-01",
            "severity": "blocker",
            "dimension": "rastreabilidade",
            "evidence": "AC-03 não aponta para nenhum TEST",
            "recommendation": "Vincular AC-03 a um TEST que falhe sem a mudança.",
        },
        {
            "id": "F-02",
            "severity": "minor",
            "dimension": "ambiguidade",
            "evidence": "o retorno deve ser rápido",
            "recommendation": "Declarar o limite em milissegundos.",
        },
    ],
}


def skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError("SKILL.md sem frontmatter ---")
    end = lines.index("---", 1)
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    rest = text[start + len(heading):]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def run_checker(payload: dict) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "findings.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=False,
        )


class TestSkillFile(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(skill_text())
        self.assertEqual(fm["name"], "TFD-qa_spec")
        self.assertEqual(fm["version"], "1.5.0")
        self.assertEqual(fm["owner"], "qa_spec")
        self.assertIn("description", fm)
        words = re.findall(r"\S+", fm["description"])
        self.assertLessEqual(len(words), 60, f"description com {len(words)} palavras")

    def test_body_size(self):
        lines = skill_text().splitlines()
        self.assertLessEqual(len(lines), 150)

    def test_routing_has_two_activations(self):
        ativar = section(skill_text(), "## Activate")
        for pedido in ACTIVATES:
            self.assertIn(pedido, ativar)

    def test_routing_has_one_non_activation(self):
        nao_ativar = section(skill_text(), "## Route elsewhere")
        self.assertIn(NAO_ATIVA, nao_ativar)

    def test_checklist_covers_eight_dimensions(self):
        text = CHECKLIST.read_text(encoding="utf-8").lower()
        dimensoes = [
            "ambiguity",
            "contradictions",
            "gaps",
            "testability",
            "traceability",
            "scope",
            "unstated assumptions",
            "security and data",
        ]
        for dimensao in dimensoes:
            self.assertIn(dimensao, text)

    def test_agent_contract(self):
        agent = json.loads(AGENT.read_text(encoding="utf-8"))
        self.assertEqual(agent["name"], "TFD-qa_spec")
        self.assertEqual(agent["sector"], "qa_spec")
        self.assertEqual(agent["outputs"], ["findings.json"])
        self.assertEqual(agent["gate"], "G3/G6")
        self.assertEqual(agent["validator"], "harness")
        self.assertEqual(agent["skills"], ["TFD-qa_spec"])
        self.assertGreaterEqual(len(agent["activates_on"]), 2)


class TestCheckFindings(unittest.TestCase):
    def test_valid_findings_exit_zero(self):
        result = run_checker(VALID_FINDINGS)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)

    def test_blocker_with_pass_is_rejected(self):
        payload = copy.deepcopy(VALID_FINDINGS)
        payload["verdict"] = "PASS"
        result = run_checker(payload)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_pass_with_only_minor_is_valid(self):
        payload = copy.deepcopy(VALID_FINDINGS)
        payload["verdict"] = "PASS"
        payload["findings"] = [payload["findings"][1]]
        result = run_checker(payload)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_verdict_and_severity_fail_without_crashing(self):
        for value in (None, [], {}):
            with self.subTest(value=value):
                payload = copy.deepcopy(VALID_FINDINGS)
                payload["verdict"] = value
                payload["findings"][0]["severity"] = value
                result = run_checker(payload)
                self.assertEqual(result.returncode, 1)
                self.assertIn("verdict: esperado", result.stdout)
                self.assertIn(".severity: esperado", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_duplicate_id_is_rejected(self):
        payload = copy.deepcopy(VALID_FINDINGS)
        payload["findings"].append(copy.deepcopy(payload["findings"][0]))
        result = run_checker(payload)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicado", result.stdout)

    def test_empty_evidence_is_rejected(self):
        payload = copy.deepcopy(VALID_FINDINGS)
        payload["findings"][0]["evidence"] = "   "
        result = run_checker(payload)
        self.assertEqual(result.returncode, 1)
        self.assertIn("evidence", result.stdout)

    def test_wrong_usage_exit_two(self):
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            check=False,
        )
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
