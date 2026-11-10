# Contexto TFD · 447 palavras · 1150 tokens (o200k_base)

"""Behavioral checks for explicit MT responsibility, boundaries and results."""

import copy
import unittest

from tests import test_schemas as fixtures
from render_task import render_task, sector_context, read_sector_receipts


class TestMicrotaskHandoff(unittest.TestCase):
    def routed(self):
        return fixtures.TestTaskContract().routed_task()

    def test_header_identifies_main_coordinator_and_implementation_qa_loop(self):
        for task in (self.routed(), fixtures.load_example()):
            with self.subTest(sectors="sectors" in task):
                header = render_task(task).split("## ", 1)[0]
                for expected in ("agente principal", "TFD-harness", "tfd_harness",
                                 "consulta/status", "QA independente", "aprovação humana"):
                    self.assertIn(expected, header)
                self.assertIn("Loop de implementação", header)

    def test_harness_display_first_preserves_execution_dependencies(self):
        task = self.routed()
        task["sectors"].pop("harness", None)
        task["sectors"]["harness"] = dict(label="harness", owner="TFD-harness", applicability="REQUIRED")
        task["microtasks"][1].update(sector="harness", owner="TFD-harness")
        original = copy.deepcopy(task)
        view = render_task(task)
        self.assertLess(view.index("| [harness](#harness)"), view.index("| [backend](#backend)"))
        self.assertLess(view.index('<a id="harness">'), view.index('<a id="backend">'))
        self.assertEqual(task, original)
        self.assertEqual(task["microtasks"][1]["depends_on"], ["MT-01"])

    def test_every_mt_has_its_own_handoff_in_sector_and_legacy_views(self):
        for task in (self.routed(), fixtures.load_example()):
            for index, micro in enumerate(task["microtasks"]):
                micro["owner"] = f"custom-agent-{index}"
                micro["validator"] = f"custom-reviewer-{index}"
                micro["deliverables"] = [f"unique-output-{index}.md"]
                micro["completion_condition"] = f"Unique acceptance {index} has observed evidence."
            view = render_task(task)
            for micro in task["microtasks"]:
                with self.subTest(sectors="sectors" in task, microtask=micro["id"]):
                    section = view.split(f"- **{micro['id']}", 1)[1].split("- **MT-", 1)[0]
                    for value in ("@" + micro["owner"], "@" + micro["validator"],
                                  micro["completion_condition"], *micro["allowed_paths"],
                                  *micro["deliverables"], *micro["checklist"]):
                        self.assertIn(value, section)
                    for label in ("Pode:", "Não pode:", "Resultado esperado:", "Concluído quando:"):
                        self.assertIn(label, section)
                    self.assertIn("(#limites-globais)", section)

    def test_global_exclusions_are_once_and_links_have_one_target(self):
        task = self.routed()
        task["out_of_scope"] = ["UNIQUE-GLOBAL-EXCLUSION"]
        task["protected_paths"] = ["UNIQUE-PROTECTED/**"]
        view = render_task(task)
        self.assertEqual(view.count("UNIQUE-GLOBAL-EXCLUSION"), 1)
        self.assertEqual(view.count("UNIQUE-PROTECTED/**"), 1)
        self.assertEqual(view.count('id="limites-globais"'), 1)
        self.assertEqual(view.count("(#limites-globais)"), len(task["microtasks"]))
        self.assertIn("caminhos protegidos", view)
        self.assertIn("contornar gates", view)

    def test_rendering_does_not_mutate_task_or_routed_execution_context(self):
        task = self.routed()
        original = copy.deepcopy(task)
        before = [sector_context(task, "backend", m["id"]) for m in task["microtasks"]]
        render_task(task)
        self.assertEqual(task, original)
        self.assertEqual(before, [sector_context(task, "backend", m["id"]) for m in task["microtasks"]])

    def test_independent_receipt_verdicts_survive_detailed_view(self):
        task = self.routed()
        micro = task["microtasks"][0]
        for verdict, marks in (("PASS", "☑ Aprovado · ☐ Reprovado"),
                               ("REWORK", "☐ Aprovado · ☑ Reprovado"),
                               ("BLOCKED", "☐ Aprovado · ☐ Reprovado")):
            with self.subTest(verdict=verdict):
                review = dict(role=micro["validator"], reviewer="reviewer", executor="executor",
                              verdict=verdict, evidence="observed.md", observation="Observed current result")
                log = dict(task_id=task["task_id"], contract_revision=task["contract_revision"],
                           sector_receipts={"backend": {"reviews": {micro["id"]: review}}})
                view = render_task(task, receipts=read_sector_receipts(task, log))
                section = view.split(f"- **{micro['id']}", 1)[1].split("- **MT-", 1)[0]
                self.assertIn(marks, section)
                self.assertIn("@" + micro["owner"], section)
                if verdict == "BLOCKED":
                    self.assertIn("Bloqueado", section)
