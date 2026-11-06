"""Testes do contrato de task do TFD. Rode: python -m unittest discover -s tests -v"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_task as vt  # noqa: E402
from validate_estimate import validate_estimate
from render_task import read_sector_receipts, render_task, sector_context

EXAMPLE = ROOT / "examples" / "task.example.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


class TestTaskContract(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual(vt.validate_task(load_example()), [])

    def routed_task(self):
        task = load_example()
        task["phases"] = [{"id": "A", "title": "Entrega"}, {"id": "B", "title": "Validação"}]
        task["sectors"] = {sector: {"label": sector, "owner": f"TFD-{sector}",
                                   "applicability": "N/A", "reason": "Fora do recorte"}
                           for sector in sorted(vt.OFFICE_SECTORS)}
        task["sectors"]["backend"]["applicability"] = "REQUIRED"
        for phase, micro in zip(("A", "B"), task["microtasks"]):
            micro.update(phase=phase, sector="backend", reference_ids=[task["references"][0]["id"]])
        return task

    def test_sector_matrix_and_phase_dependencies(self):
        task = self.routed_task()
        self.assertEqual(vt.validate_task(task), [])
        context = sector_context(task, "backend", "MT-02")
        self.assertEqual([entry["id"] for entry in context["microtasks"]], ["MT-02"])
        self.assertEqual(context["microtasks"][0]["depends_on"], ["MT-01"])
        del task["sectors"]["database"]
        task["phases"].reverse()
        errors = vt.validate_task(task)
        self.assertIn("missing sector: database", errors)
        self.assertIn("MT-02: dependency MT-01 is in a later phase", errors)

    def test_visual_verdict_requires_current_independent_evidence(self):
        task = self.routed_task()
        review = dict(role="TFD-qa_backend", reviewer="qa", executor="dev", verdict="REWORK",
                      evidence="evidence.md", observation="Teste falhou")
        workflow = dict(task_id=task["task_id"], contract_revision=task["contract_revision"],
                        sector_receipts={"backend": {"reviews": {"MT-02": review},
                                                     "total_tokens": 17, "token_receipt": "tokens.json"}})
        view = render_task(task, receipts=read_sector_receipts(task, workflow))
        self.assertIn("☐ Aprovado · ☑ Reprovado · Teste falhou", view)
        self.assertIn("Tokens reais: 17", view)
        review["verdict"] = "PASS"
        view = render_task(task, receipts=read_sector_receipts(task, workflow))
        self.assertIn("☑ Aprovado · ☐ Reprovado", view)
        review["reviewer"] = "DEV"
        with self.assertRaisesRegex(ValueError, "independente"):
            read_sector_receipts(task, workflow)
        workflow["contract_revision"] += 1
        with self.assertRaisesRegex(ValueError, "revisão"):
            read_sector_receipts(task, workflow)

    def test_missing_gates_is_rejected(self):
        task = load_example()
        del task["gates"]
        self.assertIn("$: campo obrigatório ausente: gates", vt.validate_task(task))

    def test_microtask_owner_cannot_be_its_validator(self):
        task = load_example()
        microtask = task["microtasks"][0]
        microtask["validator"] = microtask["owner"]
        self.assertIn(f"{microtask['id']}: validator deve ser diferente de owner",
                      vt.validate_task(task))

    def test_microtask_cannot_depend_on_itself(self):
        task = load_example()
        task["microtasks"][0]["depends_on"] = ["MT-01"]
        self.assertIn("depends_on: ciclo de dependências: MT-01 -> MT-01",
                      vt.validate_task(task))

    def test_microtask_dependency_cycle_is_rejected(self):
        task = load_example()
        task["microtasks"][0]["depends_on"] = ["MT-02"]
        self.assertIn("depends_on: ciclo de dependências: MT-01 -> MT-02 -> MT-01",
                      vt.validate_task(task))

    def test_missing_acceptance_is_rejected(self):
        task = load_example()
        del task["acceptance_criteria"]
        errors = vt.validate_task(task)
        self.assertTrue(any("acceptance_criteria" in e for e in errors))

    def test_bad_complexity_is_rejected(self):
        task = load_example()
        task["complexity"] = "urgente"
        errors = vt.validate_task(task)
        self.assertTrue(any("complexity" in e for e in errors))

    def test_ac_pointing_to_missing_test_is_rejected(self):
        task = load_example()
        task["acceptance_criteria"][0]["validation"] = "TEST-99"
        errors = vt.validate_task(task)
        self.assertTrue(any("TEST-99" in e for e in errors))

    def test_acceptance_requires_nonempty_link_lists(self):
        for field in ("requirement_ids", "microtask_ids"):
            with self.subTest(field=field):
                task = load_example()
                acceptance = task["acceptance_criteria"][0]
                del acceptance[field]
                self.assertTrue(any(field in error for error in vt.validate_task(task)))
                acceptance[field] = []
                self.assertTrue(any(field in error for error in vt.validate_task(task)))

    def test_acceptance_rejects_unknown_link_ids(self):
        task = load_example()
        acceptance = task["acceptance_criteria"][0]
        acceptance["requirement_ids"].append("REQ-99")
        acceptance["microtask_ids"].append("MT-99")
        errors = vt.validate_task(task)
        self.assertIn("AC-01: requirement_ids contém ID inexistente: REQ-99", errors)
        self.assertIn("AC-01: microtask_ids contém ID inexistente: MT-99", errors)

    def test_requirements_and_microtasks_must_have_acceptance_coverage(self):
        task = load_example()
        for acceptance in task["acceptance_criteria"]:
            acceptance["requirement_ids"] = ["REQ-01"]
            acceptance["microtask_ids"] = ["MT-01"]
        errors = vt.validate_task(task)
        self.assertIn("REQ-02: sem critério de aceite", errors)
        self.assertIn("MT-02: sem critério de aceite", errors)

    def test_microtask_path_outside_scope_is_rejected(self):
        task = load_example()
        task["microtasks"][0]["allowed_paths"] = ["src/outro/**"]
        errors = vt.validate_task(task)
        self.assertTrue(any("fora de allowed_paths" in e for e in errors))

    def test_estimate_order_is_enforced(self):
        task = load_example()
        task["estimate"] = {"optimistic_h": 9, "likely_h": 4, "pessimistic_h": 8,
                            "confidence": "low", "basis": "teste inválido de ordem"}
        errors = vt.validate_task(task)
        self.assertTrue(any("optimistic_h" in e for e in errors))

    def test_duplicate_ids_are_rejected(self):
        task = load_example()
        task["requirements"].append(copy.deepcopy(task["requirements"][0]))
        errors = vt.validate_task(task)
        self.assertTrue(any("duplicado" in e for e in errors))

    def test_complex_requires_spec(self):
        task = load_example()
        task["complexity"] = "complex"
        errors = vt.validate_task(task)
        self.assertTrue(any("spec" in e for e in errors))

    def test_unknown_field_is_rejected(self):
        task = load_example()
        task["campo_inventado"] = True
        errors = vt.validate_task(task)
        self.assertTrue(any("não permitido" in e for e in errors))


class TestEstimateSchema(unittest.TestCase):
    def setUp(self):
        self.estimate = {
            "task_id": "DEMO-001",
            "phase": "fase-1",
            "optimistic_h": 2,
            "likely_h": 4,
            "pessimistic_h": 8,
            "confidence": "low",
            "basis": "sem histórico; analogia com módulo similar",
            "updated_at": "2026-11-05",
        }

    def test_estimate_example_validates(self):
        self.assertEqual(validate_estimate(self.estimate), [])

    def test_estimate_rejects_out_of_order_values(self):
        for hours in ((9, 4, 8), (2, 9, 8)):
            with self.subTest(hours=hours):
                estimate = dict(zip(("optimistic_h", "likely_h", "pessimistic_h"), hours))
                errors = validate_estimate({**self.estimate, **estimate})
                self.assertTrue(any("optimistic_h" in error for error in errors))

    def test_estimate_rejects_invalid_dates(self):
        for updated_at in ("2026-02-29", "2026-11-05lixo", "2026-11-05\n"):
            with self.subTest(updated_at=updated_at):
                errors = validate_estimate({**self.estimate, "updated_at": updated_at})
                self.assertTrue(any("updated_at" in error for error in errors))

    def test_estimate_accepts_leap_day_and_equal_hours(self):
        self.estimate.update(updated_at="2024-02-29", optimistic_h=4, pessimistic_h=4)
        self.assertEqual(validate_estimate(self.estimate), [])


if __name__ == "__main__":
    unittest.main()
