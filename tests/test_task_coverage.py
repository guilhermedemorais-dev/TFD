"""Versioned technical coverage, human acceptance and safe route projections."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests import test_schemas
from render_task import render_task, sector_context
from render_task_review import render_review_body, render_review_html
from validate_task import COVERAGE_AREAS, validate_task


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/task-coverage.example.json"


def load_coverage():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


class TestTaskCoverage(unittest.TestCase):
    def test_legacy_is_accepted_but_new_authoring_requires_coverage(self):
        task = test_schemas.load_example()
        self.assertEqual(validate_task(task), [])
        self.assertTrue(validate_task(task, require_coverage=True))
        self.assertNotIn("Cobertura técnica", render_task(task))

    def test_generic_example_and_implicit_version_are_valid(self):
        task = load_coverage()
        self.assertEqual(validate_task(task, require_coverage=True), [])
        task.pop("coverage_version")
        self.assertEqual(validate_task(task), [])
        self.assertTrue(validate_task(task, require_coverage=True))

    def test_version_requires_coverage_and_spec(self):
        task = test_schemas.load_example()
        task["coverage_version"] = 1
        errors = validate_task(task)
        self.assertTrue(any("technical_coverage" in error for error in errors))
        task = load_coverage()
        task.pop("spec")
        self.assertTrue(any("spec" in error for error in validate_task(task)))
        for version in (2, True, "1"):
            task["coverage_version"] = version
            self.assertTrue(any("coverage_version" in error for error in validate_task(task)))

    def test_new_authoring_requires_phase_and_sector_routes(self):
        task = load_coverage()
        task.pop("phases")
        task.pop("sectors")
        self.assertEqual(validate_task(task), [])
        self.assertTrue(any("phases e sectors" in error for error in validate_task(task, require_coverage=True)))

    def test_all_eight_areas_are_required_and_no_other_key_is_allowed(self):
        for area in COVERAGE_AREAS:
            task = load_coverage()
            del task["technical_coverage"][area]
            self.assertTrue(any(area in error for error in validate_task(task)))
        task = load_coverage()
        task["technical_coverage"]["extra"] = copy.deepcopy(task["technical_coverage"]["backend"])
        self.assertTrue(any("extra" in error for error in validate_task(task)))

    def test_covered_requires_summary_and_real_ref_mt_ac_links(self):
        for field in ("summary", "reference_ids", "microtask_ids", "acceptance_ids"):
            task = load_coverage()
            task["technical_coverage"]["backend"][field] = "   " if field == "summary" else []
            self.assertTrue(any(field in error for error in validate_task(task)), field)
        for field, bad_id in (("reference_ids", "REF-99"), ("microtask_ids", "MT-99"), ("acceptance_ids", "AC-99")):
            task = load_coverage()
            task["technical_coverage"]["backend"][field] = [bad_id]
            self.assertTrue(any(bad_id in error for error in validate_task(task)), field)

    def test_na_requires_specific_reason_and_no_links(self):
        for reason in (None, "", "   ", "não se aplica", "fora do escopo"):
            task = load_coverage()
            cell = task["technical_coverage"]["frontend"]
            cell.pop("reason")
            if reason is not None:
                cell["reason"] = reason
            self.assertTrue(any("frontend" in error for error in validate_task(task)))
        for field, link in (("reference_ids", "REF-01"), ("microtask_ids", "MT-01"), ("acceptance_ids", "AC-01")):
            task = load_coverage()
            task["technical_coverage"]["frontend"][field] = [link]
            self.assertTrue(any("N/A não permite links" in error for error in validate_task(task)))

    def test_unknown_acceptance_rule_and_missing_rule_acceptance_are_rejected(self):
        task = load_coverage()
        task["acceptance_criteria"][0]["rule_ids"] = ["RULE-99"]
        errors = validate_task(task)
        self.assertTrue(any("RULE-99" in error for error in errors))
        self.assertTrue(any("RULE-01 sem critério" in error for error in errors))
        task = load_coverage()
        task["technical_coverage"]["business"]["rule_ids"] = []
        self.assertTrue(any("regra sem cobertura: RULE-01" in error for error in validate_task(task)))

    def test_cell_acceptance_must_link_a_listed_mt(self):
        task = load_coverage()
        task["acceptance_criteria"][0]["microtask_ids"] = ["MT-01"]
        task["technical_coverage"]["backend"]["microtask_ids"] = ["MT-02"]
        task["technical_coverage"]["backend"]["acceptance_ids"] = ["AC-01"]
        self.assertTrue(any("AC-01 sem vínculo" in error for error in validate_task(task)))

    def test_each_listed_microtask_has_acceptance_in_its_area(self):
        task = load_coverage()
        task["acceptance_criteria"][0]["microtask_ids"] = ["MT-01"]
        task["acceptance_criteria"][1]["microtask_ids"] = ["MT-02"]
        task["technical_coverage"]["backend"]["acceptance_ids"] = ["AC-01"]
        errors = validate_task(task, require_coverage=True)
        self.assertTrue(any("technical_coverage.backend" in error and "MT-02" in error
                            for error in errors), errors)
        task["technical_coverage"]["backend"]["acceptance_ids"].append("AC-02")
        self.assertEqual(validate_task(task, require_coverage=True), [])
        sliced = sector_context(task, "backend", "MT-02")
        self.assertEqual(sliced["technical_coverage"]["backend"]["acceptance_ids"], ["AC-02"])

    def test_requirement_and_mt_cannot_hide_outside_covered_acceptance(self):
        task = load_coverage()
        # Existing acceptance still covers both REQs/MTs, but area evidence omits REQ-02/MT-02.
        task["acceptance_criteria"][0]["microtask_ids"] = ["MT-01"]
        for cell in task["technical_coverage"].values():
            if cell["status"] == "COVERED":
                cell["acceptance_ids"] = ["AC-01"]
        errors = validate_task(task)
        self.assertTrue(any("requirement sem cobertura: REQ-02" in error for error in errors))
        self.assertTrue(any("microtask sem cobertura: MT-02" in error for error in errors))

    def routed(self):
        task = load_coverage()
        route = test_schemas.TestTaskContract().routed_task()
        task["phases"], task["sectors"] = route["phases"], route["sectors"]
        for micro, routed in zip(task["microtasks"], route["microtasks"]):
            micro.update(phase=routed["phase"], sector=routed["sector"])
        return task

    def test_required_sector_cannot_use_na_area(self):
        for sector, area in (("backend", "backend"), ("database", "data"), ("qa", "quality"),
                             ("frontend", "frontend"), ("ui_ux", "ui_ux"), ("security", "security"),
                             ("devops", "operations"), ("observability", "operations")):
            task = self.routed()
            task["sectors"][sector]["applicability"] = "REQUIRED"
            micro = task["microtasks"][0]
            micro.update(sector=sector, owner=task["sectors"][sector]["owner"])
            task["technical_coverage"][area] = copy.deepcopy(task["technical_coverage"]["frontend"])
            self.assertTrue(any(f"setor {sector} REQUIRED" in error for error in validate_task(task)), sector)

    def test_slice_preserves_mandatory_references_applicable_coverage_and_global_rules(self):
        task = self.routed()
        original = copy.deepcopy(task)
        self.assertEqual(validate_task(task), [])
        for mt in (None, "MT-01", "MT-02"):
            context = sector_context(task, "backend", mt)
            self.assertEqual(context["references"], task["references"])
            self.assertEqual(context["business_rules"], task["business_rules"])
            self.assertEqual(context["protected_paths"], task["protected_paths"])
            self.assertEqual(context["coverage_version"], 1)
            self.assertEqual(context["spec"], task["spec"])
            for area in ("backend", "business", "quality"):
                cell = context["technical_coverage"][area]
                self.assertEqual(cell["reference_ids"], ["REF-01", "REF-02"])
                self.assertEqual(cell["microtask_ids"], [mt] if mt else ["MT-01", "MT-02"])
                self.assertEqual(cell["acceptance_ids"], ["AC-01", "AC-02"])
        self.assertEqual(task, original)

    def test_slice_omits_references_from_unrelated_coverage_and_filters_rule_links(self):
        task = self.routed()
        task["references"].append({"id": "REF-03", "path": "docs/other-area.md",
                                   "purpose": "Reference needed only for the second microtask."})
        task["acceptance_criteria"][0]["microtask_ids"] = ["MT-01"]
        task["acceptance_criteria"][1]["microtask_ids"] = ["MT-02"]
        task["technical_coverage"]["data"] = {
            "status": "COVERED", "summary": "Preservar os valores de entrada nos casos de borda.",
            "reference_ids": ["REF-03"], "microtask_ids": ["MT-02"], "acceptance_ids": ["AC-02"]}
        self.assertEqual(validate_task(task), [])
        first = sector_context(task, "backend", "MT-01")
        self.assertEqual({ref["id"] for ref in first["references"]}, {"REF-01", "REF-02"})
        self.assertNotIn("data", first["technical_coverage"])
        self.assertEqual(first["business_rules"], task["business_rules"])
        second = sector_context(task, "backend", "MT-02")
        self.assertEqual({ref["id"] for ref in second["references"]}, {"REF-01", "REF-02", "REF-03"})
        self.assertIn("data", second["technical_coverage"])
        self.assertEqual(second["business_rules"], [])
        self.assertEqual(second["technical_coverage"]["business"]["rule_ids"], [])
        self.assertEqual(second["technical_coverage"]["business"]["acceptance_ids"], ["AC-02"])

    def test_markdown_and_review_show_summary_evidence_and_human_acceptance_per_mt(self):
        task = load_coverage()
        task["technical_coverage"]["backend"]["summary"] = "Preservar <script> e | texto"
        original = copy.deepcopy(task)
        markdown = render_task(task)
        review = render_review_body(task, "digest", ({}, {}, []), markdown=True)
        page = render_review_html(task, "digest", ({}, {}, []))
        self.assertIn("| Backend | COVERED |", markdown)
        self.assertIn("\\| texto", markdown)
        for rendered in (markdown, review, page):
            for field in ("REF-02", "RULE-01", "AC-01", task["technical_coverage"]["frontend"]["reason"]):
                self.assertIn(field, rendered)
            self.assertIn("Nome vazio retorna erro", rendered)
        self.assertIn("<summary>Cobertura técnica por área</summary>", review)
        self.assertIn("&lt;script&gt;", review)
        self.assertNotIn("<script>", review)
        for micro in task["microtasks"]:
            section = markdown.split(f"- **{micro['id']}", 1)[1].split("- **MT-", 1)[0]
            self.assertIn("Aceite AC-01:", section)
            self.assertIn("Aceite AC-02:", section)
            self.assertIn("TEST-02", section)
        self.assertEqual(task, original)

    def test_cli_require_coverage_is_explicit_and_legacy_still_works(self):
        for file, required_exit in ((test_schemas.EXAMPLE, 1), (EXAMPLE, 0)):
            run = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_task.py"), str(file),
                                  "--require-coverage"], capture_output=True, timeout=30)
            self.assertEqual(run.returncode, required_exit, run.stderr)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task = root / "task.json"
            task.write_bytes(EXAMPLE.read_bytes())
            for script, args in (("render_task.py", []), ("render_task_review.py", [root / "review.html"])):
                run = subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / script), str(task),
                                      *map(str, args), "--require-coverage"], capture_output=True, timeout=30)
                self.assertEqual(run.returncode, 0, run.stderr)


if __name__ == "__main__":
    unittest.main()
