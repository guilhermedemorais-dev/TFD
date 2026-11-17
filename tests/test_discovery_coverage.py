import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/TFD-discovery/scripts/check_evidence.py"
spec = importlib.util.spec_from_file_location("discovery_evidence", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def fixture():
    sources = [{"id": "SRC-01", "location": "docs/contracts.md", "revision": "r2", "status": "verified"}]
    evidence = [{
        "id": "EV-01", "claim": "O contrato exige autorização para alterar pedidos",
        "class": "OBSERVED", "limits": "Contrato aprovado; runtime ainda não testado",
        "source_id": "SRC-01", "locator": "Regra 1",
    }]
    coverage = {
        "version": 1, "requirement_ids": ["REQ-01"], "business_rule_ids": ["RULE-01"],
        "areas": {area: {"status": "COVERED", "summary": f"Contrato de {area}", "evidence_ids": ["EV-01"]}
                  for area in checker.AREAS},
        "flows": [{"id": "FLOW-01", "summary": "Alterar pedido com autorização",
                   "requirement_ids": ["REQ-01"], "business_rule_ids": ["RULE-01"], "evidence_ids": ["EV-01"]}],
    }
    return sources, evidence, coverage


class TestDiscoveryCoverage(unittest.TestCase):
    def test_full_coverage_both_entry_points(self):
        sources, evidence, coverage = fixture()
        self.assertEqual(checker.validate_coverage(coverage, sources, evidence), ([], []))
        self.assertEqual(checker.validate(sources, evidence, coverage), ([], []))

    def test_shallow_ui_observation_is_not_complete_coverage(self):
        sources, evidence, coverage = fixture()
        evidence[0].update(claim="A tela mostra um pedido", limits="Só a tela", locator="Captura 1")
        self.assertEqual(checker.validate(sources, evidence), ([], []))
        coverage["areas"] = {"ui_ux": coverage["areas"]["ui_ux"]}
        coverage["flows"][0]["business_rule_ids"] = []
        errors, _ = checker.validate_coverage(coverage, sources, evidence)
        self.assertTrue(any("areas.backend" in error for error in errors))
        self.assertTrue(any("regra sem fluxo" in error for error in errors))

    def test_na_requires_reason_and_no_evidence(self):
        sources, evidence, coverage = fixture()
        area = coverage["areas"]["operations"]
        area.update(status="N/A", summary="Sem alteração operacional", reason="Fluxo exclusivamente documental", evidence_ids=[])
        self.assertEqual(checker.validate_coverage(coverage, sources, evidence), ([], []))
        for update in ({"reason": " "}, {"evidence_ids": ["EV-01"]}):
            changed = copy.deepcopy(coverage)
            changed["areas"]["operations"].update(update)
            self.assertTrue(checker.validate_coverage(changed, sources, evidence)[0])

    def test_business_rules_cannot_be_declared_not_applicable(self):
        sources, evidence, coverage = fixture()
        coverage["areas"]["business"].update(status="N/A", reason="Não investigado", evidence_ids=[])
        self.assertTrue(any("regras de negócio" in error
                            for error in checker.validate_coverage(coverage, sources, evidence)[0]))

    def test_unknown_area_blocks_even_with_demoted_unknown_evidence(self):
        sources, evidence, coverage = fixture()
        evidence.append({"id": "EV-02", "claim": "Como registrar a métrica?", "class": "UNKNOWN",
                         "limits": "Fornecedor indisponível", "essential": False,
                         "rationale": "Métrica opcional fora do aceite", "affected_decision": "Observabilidade futura"})
        coverage["areas"]["operations"].update(status="UNKNOWN", reason="Investigar métrica", evidence_ids=["EV-02"])
        self.assertEqual(checker.validate_coverage(coverage, sources, evidence), ([], ["coverage.areas.operations"]))
        for field in ("rationale", "affected_decision"):
            changed = copy.deepcopy(evidence)
            del changed[-1][field]
            self.assertTrue(any(field in error for error in checker.validate_coverage(coverage, sources, changed)[0]))
        evidence[-1]["essential"] = True
        self.assertIn("EV-02", checker.validate_coverage(coverage, sources, evidence)[1])

    def test_unknown_stale_missing_or_malformed_evidence_cannot_cover(self):
        for mutation in ("unknown", "stale", "missing", "locator", "claim", "revision"):
            sources, evidence, coverage = fixture()
            if mutation == "unknown":
                evidence[0].update({"class": "UNKNOWN", "essential": False,
                                    "rationale": "Fora do aceite", "affected_decision": "Futuro"})
            elif mutation == "stale":
                sources[0]["status"] = "stale"
            elif mutation == "missing":
                evidence[0]["source_id"] = "SRC-404"
            elif mutation == "revision":
                sources[0]["revision"] = ""
            else:
                evidence[0][mutation] = ""
            with self.subTest(mutation=mutation):
                errors, _ = checker.validate_coverage(coverage, sources, evidence)
                self.assertTrue(any("COVERED requer" in error for error in errors))
                self.assertTrue(any("requisito sem fluxo" in error for error in errors))

    def test_bad_links_duplicate_ids_and_uncovered_inventory(self):
        mutations = (
            lambda c: c["requirement_ids"].append("REQ-01"),
            lambda c: c["business_rule_ids"].append("RULE-02"),
            lambda c: c["requirement_ids"].append("REQ-02"),
            lambda c: c["flows"].append(copy.deepcopy(c["flows"][0])),
            lambda c: c["flows"][0]["requirement_ids"].append("REQ-404"),
            lambda c: c["flows"][0]["business_rule_ids"].append("RULE-404"),
            lambda c: c["flows"][0]["evidence_ids"].append("EV-404"),
            lambda c: c["areas"]["backend"]["evidence_ids"].append("EV-404"),
            lambda c: c["flows"][0]["evidence_ids"].append("EV-01"),
            lambda c: c["flows"][0].update(id="not-a-flow"),
            lambda c: c["areas"].update(unrecognized={}),
        )
        for index, mutate in enumerate(mutations):
            sources, evidence, coverage = fixture()
            mutate(coverage)
            with self.subTest(mutation=index):
                self.assertTrue(checker.validate_coverage(coverage, sources, evidence)[0])

    def test_references_can_be_shared_across_distinct_flows(self):
        sources, evidence, coverage = fixture()
        coverage["flows"].append({**coverage["flows"][0], "id": "FLOW-02"})
        self.assertEqual(checker.validate_coverage(coverage, sources, evidence), ([], []))

    def test_malformed_coverage_reports_errors_without_crashing(self):
        for value in (None, [], {}, {"version": True, "areas": [], "flows": [None]},
                      {"version": 1, "requirement_ids": [{}], "business_rule_ids": False,
                       "areas": {"business": {"status": [], "evidence_ids": [{}]}}, "flows": [{}]}):
            sources, evidence, _ = fixture()
            with self.subTest(value=value):
                self.assertTrue(checker.validate_coverage(value, sources, evidence)[0])

    def test_cli_coverage_optional_required_invalid_and_blocked(self):
        sources, evidence, coverage = fixture()
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / name for name in ("sources.json", "evidence.json", "coverage.json")]
            for path, content in zip(paths, (sources, evidence, coverage)):
                path.write_text(json.dumps(content), encoding="utf-8")
            command = [sys.executable, "-B", str(SCRIPT), str(paths[0]), str(paths[1])]
            cases = (([], 0), (["--require-coverage"], 1),
                     (["--coverage", str(paths[2])], 0),
                     (["--coverage", str(paths[2]), "--require-coverage"], 0))
            for flags, code in cases:
                with self.subTest(flags=flags):
                    result = subprocess.run(command + flags, capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, code, result.stdout + result.stderr)
            coverage["areas"]["operations"].update(status="UNKNOWN", reason="Pergunta pendente", evidence_ids=[])
            paths[2].write_text(json.dumps(coverage), encoding="utf-8")
            result = subprocess.run(command + ["--coverage", str(paths[2])], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("BLOCKED: coverage.areas.operations", result.stdout)
            for invalid in ("null", "{", "{}"):
                paths[2].write_text(invalid, encoding="utf-8")
                result = subprocess.run(command + ["--coverage", str(paths[2])], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
