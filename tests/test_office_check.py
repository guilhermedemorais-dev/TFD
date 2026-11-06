import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import office


class TestOfficeCheck(unittest.TestCase):
    def test_git_status_failure_blocks_pass_even_with_green_tests(self):
        task = str(ROOT / "examples" / "task.example.json")
        git_failure = subprocess.CompletedProcess(
            ["git", "status", "--porcelain"], 128, "", "not a git repository"
        )
        with tempfile.TemporaryDirectory() as temp:
            delivery = Path(temp) / "delivery"
            stderr = io.StringIO()
            with (
                patch.object(office, "DELIVERY", delivery),
                patch.object(office.subprocess, "run", return_value=git_failure),
                patch.object(office, "_run", side_effect=lambda command, timeout: {
                    "command": command, "exit": 0,
                }),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                self.assertEqual(office.main(["check", task]), 1)
                self.assertEqual(office.main(["report", task]), 0)

            self.assertIn("[ESCOPO] NÃO VERIFICADO", stderr.getvalue())
            receipt = json.loads((delivery / "receipts" / "DEMO-001.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["result"], "FAILED")
            self.assertIn("exit 128", receipt["scope"]["error"])
            self.assertEqual([test["exit"] for test in receipt["tests"]], [0, 0])
            report = (delivery / "ENTREGA-DEMO-001.md").read_text(encoding="utf-8")
            self.assertIn("Escopo não verificado", report)
