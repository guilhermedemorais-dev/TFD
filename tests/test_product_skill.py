# Contexto TFD · 820 palavras · 1889 tokens (o200k_base)

"""Testes estáticos do setor `product` do TFD.

Rode na raiz do plugin:
    python -m unittest tests.test_product_skill -v
"""

from __future__ import annotations

import json
import re
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "TFD-product" / "SKILL.md"
AGENT = ROOT / "agents" / "TFD-product" / "agent.json"
TEMPLATE = ROOT / "skills" / "TFD-product" / "references" / "prd-template.md"

REQUIRED_AGENT_KEYS = {
    "name",
    "sector",
    "description",
    "activates_on",
    "inputs",
    "outputs",
    "gate",
    "validator",
    "skills",
}

REQUIRED_SECTIONS = [
    "problema",
    "objetivos",
    "usuarios",
    "escopo",
    "nao-escopo",
    "requisitos",
    "regras de negocio",
    "riscos",
    "metricas de sucesso",
    "referencias",
    "perguntas abertas",
]

POSITIVE_REQUESTS = [
    "preciso do PRD deste produto",
    "vamos fazer o briefing do novo produto",
]

NEGATIVE_REQUEST = "corrigir bug de SQL no backend"

FORBIDDEN_REFERENCES = [
    "the office v2",
    "global-core",
    "codex_home",
    "c:\\users",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize(text: str) -> str:
    """Minúsculas, sem acentos e com espaços colapsados."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict:
    """Lê o YAML simples do frontmatter: campos de primeiro nível e um nível aninhado."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}

    data: dict = {}
    parent = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        key, _, value = raw.strip().partition(":")
        if raw[0] in " \t":
            if parent is not None:
                data[parent][key.strip()] = _unquote(value)
            continue
        key = key.strip()
        if value.strip() == "":
            parent = key
            data[key] = {}
        else:
            parent = None
            data[key] = _unquote(value)
    return data


def headings(text: str) -> list[str]:
    return [
        normalize(line.lstrip("#").strip())
        for line in text.splitlines()
        if line.startswith("## ")
    ]


class TestSkillFrontmatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(SKILL)
        cls.frontmatter = parse_frontmatter(cls.text)
        cls.metadata = cls.frontmatter.get("metadata", {})

    def test_frontmatter_exists(self):
        self.assertTrue(self.frontmatter, "frontmatter ausente ou malformado")

    def test_name_is_tfd_product(self):
        self.assertEqual(self.frontmatter.get("name"), "TFD-product")

    def test_description_has_at_most_60_words(self):
        description = self.frontmatter.get("description", "")
        self.assertTrue(description, "description vazia")
        self.assertLessEqual(
            len(description.split()),
            60,
            f"description com {len(description.split())} palavras",
        )

    def test_metadata_version_is_1_4_0(self):
        self.assertIsInstance(self.metadata, dict)
        self.assertEqual(self.metadata.get("version"), "1.4.0")

    def test_metadata_owner_is_product(self):
        self.assertEqual(self.metadata.get("owner"), "product")


class TestSkillBody(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(SKILL)

    def test_skill_has_at_most_150_lines(self):
        total = len(self.text.splitlines())
        self.assertLessEqual(total, 150, f"SKILL.md com {total} linhas")

    def test_reference_software_is_optional(self):
        body = normalize(self.text)
        self.assertIn("if the user names reference software", body)
        self.assertIn("missing reference software does not block g1", body)

    def test_required_prd_sections_are_named(self):
        body = normalize(self.text)
        sections = ("problem", "objectives", "users", "scope", "out of scope",
                    "requirements", "business rules", "risks", "success metrics",
                    "references", "open questions")
        missing = [s for s in sections if s not in body]
        self.assertEqual(missing, [], f"seções ausentes no SKILL.md: {missing}")

    def test_forbidden_references_are_absent(self):
        body = normalize(self.text)
        found = [term for term in FORBIDDEN_REFERENCES if term in body]
        self.assertEqual(found, [], f"referências proibidas no SKILL.md: {found}")


class TestPrdTemplate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(TEMPLATE)

    def test_has_all_required_sections_as_headings(self):
        heads = headings(self.text)
        missing = [s for s in REQUIRED_SECTIONS if s not in heads]
        self.assertEqual(missing, [], f"seções ausentes no template: {missing}")

    def test_uses_requirement_and_rule_numbering(self):
        self.assertIn("REQ-01", self.text)
        self.assertIn("RULE-01", self.text)


class TestAgentJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = json.loads(read(AGENT))

    def test_has_exactly_the_required_keys(self):
        self.assertEqual(set(self.agent.keys()), REQUIRED_AGENT_KEYS)

    def test_identity_and_gate(self):
        self.assertEqual(self.agent["name"], "TFD-product")
        self.assertEqual(self.agent["sector"], "product")
        self.assertEqual(self.agent["gate"], "G1")
        self.assertEqual(self.agent["validator"], "TFD-qa_spec")
        self.assertIn("TFD-product", self.agent["skills"])

    def test_outputs_include_briefing_and_prd(self):
        outputs = self.agent["outputs"]
        self.assertIn("docs/prd/briefing.md", outputs)
        self.assertIn("docs/prd/prd.md", outputs)

    def test_activates_on_is_a_non_empty_string_list(self):
        triggers = self.agent["activates_on"]
        self.assertIsInstance(triggers, list)
        self.assertGreaterEqual(len(triggers), 2)
        for trigger in triggers:
            self.assertIsInstance(trigger, str)
            self.assertTrue(trigger.strip())

    def test_forbidden_references_are_absent(self):
        raw = normalize(read(AGENT))
        found = [term for term in FORBIDDEN_REFERENCES if term in raw]
        self.assertEqual(found, [], f"referências proibidas no agent.json: {found}")


class TestRouting(unittest.TestCase):
    """Teste estático de roteamento: cobre gatilhos e descrição, não semântica."""

    @classmethod
    def setUpClass(cls):
        agent = json.loads(read(AGENT))
        frontmatter = parse_frontmatter(read(SKILL))
        surface = [frontmatter.get("description", "")]
        surface.extend(str(item) for item in agent.get("activates_on", []))
        cls.surface = normalize(" ".join(surface))

    def test_positive_request_prd(self):
        self.assertIn(normalize(POSITIVE_REQUESTS[0]), self.surface)

    def test_positive_request_briefing(self):
        self.assertIn(normalize(POSITIVE_REQUESTS[1]), self.surface)

    def test_negative_request_does_not_route(self):
        negative = normalize(NEGATIVE_REQUEST)
        self.assertNotIn(negative, self.surface)
        for term in ("sql", "backend"):
            self.assertNotIn(term, self.surface)


if __name__ == "__main__":
    unittest.main()
