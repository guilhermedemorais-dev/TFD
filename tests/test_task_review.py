import hashlib
import html
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from tests import test_pipeline, test_schemas

from pipeline import stages
from render_task import render_task
from render_task_review import render_review_body, render_review_html
from resume_task import resume


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/render_task_review.py"
EMPTY = ({}, {}, [])


def cli(task, output, *arguments):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), str(task), str(output), *map(str, arguments)],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)


class TestTaskReview(unittest.TestCase):
    def test_legacy_review_keeps_full_contract_and_copies_same_markdown(self):
        task = test_schemas.load_example()
        task["microtasks"][0]["checklist"][0] = "Escapar <script>, @nome e [referência]"
        task["goal"] += "\r\nSegunda linha do objetivo."
        task["references"][0]["path"] = "https://example.org/spec?left=1&right=2"
        markdown = render_review_body(task, "digest", EMPTY, markdown=True)
        page = render_review_html(task, "digest", EMPTY)
        embedded = re.search(r'<textarea[^>]*>(.*?)</textarea>', page, re.S)[1]
        self.assertEqual(html.unescape(embedded), markdown)
        self.assertNotIn("\r", markdown)
        self.assertLess(page.index("Copiar Markdown"), page.index(task["title"]))
        self.assertIn('role="status"', page)
        self.assertIn('source.select()', page)
        self.assertIn('<figure class="flow">', page)
        self.assertIn("```mermaid", markdown)
        self.assertNotIn("<script", markdown)
        self.assertIn("&lt;script&gt;", markdown)
        self.assertIn("&#64;nome", markdown)
        self.assertIn('href="https://example.org/spec?left=1&amp;right=2"', markdown)
        self.assertEqual(markdown.count("- [ ] Aprovado"), 2)
        self.assertEqual(markdown.count("- [ ] Reprovado"), 2)
        for text in ("Checklist para aprovar a Task", "Regras de negócio", "Caminhos protegidos",
                     "Critérios de aceite", "Condições de parada", "Sem registro nesta visão",
                     "Sem parecer de execução", "TEST-01", "REQ-01", "src/cadastro/normalize.py"):
            self.assertIn(text, markdown)

    def test_invalid_or_canonical_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task = root / "task.json"
            task.write_bytes(test_schemas.EXAMPLE.read_bytes())
            sibling = task.with_suffix(".md")
            sibling.write_text("canonical view", encoding="utf-8")
            self.assertEqual(cli(task, sibling).returncode, 1)
            self.assertEqual(sibling.read_text(encoding="utf-8"), "canonical view")
            output = root / "review.html"
            task.write_text("{}", encoding="utf-8")
            self.assertEqual(cli(task, output).returncode, 1)
            self.assertFalse(output.exists())


class TestTaskReviewWorkflow(unittest.TestCase):
    def setUp(self):
        self.fixture = test_pipeline.TestPipeline()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.project = self.fixture.project.resolve()
        self.workflow = self.project / "workflow.json"
        self.output = self.project / "task-review.md"
        self.task_file = self.project / "task.json"
        task = test_schemas.TestTaskContract().routed_task()
        self.fixture.log["phases"] = [{"id": phase["id"], "backend": True, "ui": False, "security": False}
                                      for phase in task["phases"]]
        self.fixture.plan = stages(self.fixture.log["phases"])
        implementation_index = next(i for i, stage in enumerate(self.fixture.plan) if stage[0] == "G7")
        self.implementation = self.fixture.plan[implementation_index]
        self.fixture.complete_prefix(implementation_index)
        submitted = next(event for event in self.fixture.log["events"] if event["gate"] == "G6"
                         and event["action"] == "submit")
        submitted["artifacts"]["task_view"] = "canonical-view.md"
        self.view = self.project / "canonical-view.md"
        for artifact, content in {"task": json.dumps(task), "task_view": render_task(task)}.items():
            data = content.encode("utf-8")
            (self.project / submitted["artifacts"][artifact]).write_bytes(data)
            submitted["sha256"][artifact] = hashlib.sha256(data).hexdigest()
        for event in self.fixture.log["events"]:
            if event.get("phase") is None:
                event.pop("phase", None)
        self.fixture.log.update(task_id=task["task_id"], contract_revision=task["contract_revision"])
        self.save_workflow()

    def save_workflow(self):
        self.workflow.write_text(json.dumps(self.fixture.log), encoding="utf-8")

    def run_review(self, output=None):
        return cli(self.task_file, output or self.output, "--workflow", self.workflow, "--project-root", self.project)

    def record_execution_and_review(self):
        evidence = "execution.md"
        (self.project / evidence).write_text("Observed result", encoding="utf-8")
        for status in ("started", "verified"):
            resume(self.workflow, self.project, SimpleNamespace(git_base=None, record=status,
                   microtask="MT-01", item=1, evidence=evidence))
        review = dict(role="TFD-qa_backend", reviewer="qa", executor="dev", verdict="PASS",
                      evidence="review.md", observation="Observed backend QA", attempt=1)
        self.fixture.log["sector_receipts"] = {"backend": {"reviews": {"MT-01": review}}}
        self.fixture.submit(self.implementation, "implementation-1")
        self.fixture.review(self.implementation, "implementation-1", "qa_backend")
        self.save_workflow()
        return review

    def test_approved_review_preserves_verified_checkpoint_and_unchecked_human_marks(self):
        self.record_execution_and_review()
        run = self.run_review()
        self.assertEqual(run.returncode, 0, run.stderr)
        markdown = self.output.read_text(encoding="utf-8")
        self.assertIn("Item 1 · verificado · execution.md", markdown)
        self.assertIn("PASS · TFD-qa_backend · tentativa 1 · Observed backend QA", markdown)
        self.assertIn("G6 · A", markdown)
        self.assertIn("G7 · A", markdown)
        self.assertIn("- [ ] Aprovado", markdown)
        self.assertNotIn("- [x] Aprovado", markdown)
        self.assertLess(markdown.index("A · Entrega"), markdown.index("B · Validação"))
        self.assertLess(markdown.index("MT-01 · Implementar"), markdown.index("MT-02 · Cobrir"))

    def test_invalid_checkpoint_or_review_attempt_fails_closed(self):
        review = self.record_execution_and_review()
        review["attempt"] = 2
        self.save_workflow()
        run = self.run_review()
        self.assertEqual(run.returncode, 1)
        self.assertFalse(self.output.exists())
        review["attempt"] = 1
        self.save_workflow()
        (self.project / "execution.md").write_text("Changed result", encoding="utf-8")
        run = self.run_review()
        self.assertEqual(run.returncode, 1)
        self.assertIn("item evidence changed", run.stderr)
        self.assertFalse(self.output.exists())

    def test_sector_receipts_must_be_an_object(self):
        self.fixture.log["sector_receipts"] = []
        self.save_workflow()
        run = self.run_review()
        self.assertEqual(run.returncode, 1)
        self.assertFalse(self.output.exists())

    def test_alternate_canonical_view_and_evidence_cannot_be_overwritten(self):
        for file in (self.view, self.project / "review.md"):
            with self.subTest(file=file.name):
                before = file.read_bytes()
                run = self.run_review(file)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(file.read_bytes(), before)

    def test_different_task_bytes_with_same_identity_are_rejected(self):
        other = self.project / "other.json"
        other.write_bytes(self.task_file.read_bytes() + b"\n")
        run = cli(other, self.output, "--workflow", self.workflow, "--project-root", self.project)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(self.output.exists())

    def test_preparation_authorization_cannot_be_overwritten(self):
        authorization = self.project / "preparation.md"
        authorization.write_text("Explicit preparation authorization", encoding="utf-8")
        self.fixture.log["events"] = []
        self.fixture.log["preparation"] = {"mode": "reviewed_task", "authorization": authorization.name}
        self.save_workflow()
        run = self.run_review(authorization)
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(authorization.read_text(encoding="utf-8"), "Explicit preparation authorization")
