# Contexto TFD · 467 palavras · 1119 tokens (o200k_base)

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import install_tfd


class TestInstallTfd(unittest.TestCase):
    def test_routing_contract_names_two_installation_requests_and_one_delivery_request(self):
        skill = (ROOT / "skills/tfd-install/SKILL.md").read_text(encoding="utf-8")
        cases = (
            ("Instala o TFD neste computador.", "`install`"),
            ("Confere se saiu atualização do TFD.", "`check`"),
            ("Abre o módulo de cadastro no TFD.", "harness"),
        )
        for message, action in cases:
            with self.subTest(message=message):
                self.assertIn(f"“{message}” → {action}", skill)

    def test_check_of_unmanaged_profile_does_not_write_or_install(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory) / "profile"
            with patch.dict("os.environ", {"CODEX_HOME": str(profile)}), patch.object(
                install_tfd, "remote_revision", return_value="b" * 40,
            ), patch.object(sys, "argv", ["install_tfd.py", "check"]), patch("builtins.print") as output:
                self.assertEqual(install_tfd.main(), 0)
                self.assertEqual(json.loads(output.call_args.args[0])["status"], "INSTALL_REQUIRED")
            self.assertFalse(profile.exists())

    def test_update_required_for_old_revision_or_missing_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory)
            cache = profile / "cache"
            manifest = cache / install_tfd.MANIFEST
            manifest.parent.mkdir(parents=True)
            manifest.write_text("{}", encoding="utf-8")
            receipt = profile / "receipt.json"
            receipt.write_text(
                json.dumps({"installed_revision": "a" * 40, "installed_path": str(cache)}), encoding="utf-8",
            )
            self.assertEqual(install_tfd.inspect_installation(receipt, "a" * 40)["status"], "UP_TO_DATE")
            self.assertEqual(install_tfd.inspect_installation(receipt, "b" * 40)["status"], "UPDATE_AVAILABLE")
            manifest.unlink()
            self.assertEqual(install_tfd.inspect_installation(receipt, "a" * 40)["status"], "INSTALL_REQUIRED")

    def test_updates_only_managed_instruction_section_in_active_override(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory)
            default = profile / "AGENTS.md"
            override = profile / "AGENTS.override.md"
            default.write_bytes(b"# Default rules\r\n")
            override.write_bytes(b"# Existing rules\r\n")
            install_tfd.configure_instructions(profile, "## Tradutor TFD\n\nFirst.")
            with override.open("ab") as stream:
                stream.write(b"\r\n## Keep this heading\r\n")
            install_tfd.configure_instructions(profile, "## Tradutor TFD\n\nSecond.")
            body = override.read_bytes()
            self.assertIn(b"# Existing rules\r\n", body)
            self.assertIn(b"\r\nSecond.\r\n", body)
            self.assertTrue(body.endswith(b"\r\n## Keep this heading\r\n"))
            self.assertEqual(body.count(install_tfd.START.encode()), 1)
            self.assertEqual(default.read_bytes(), b"# Default rules\r\n")

    def test_preserves_unmanaged_tfd_instruction_section(self):
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory)
            instructions = profile / "AGENTS.md"
            original = b"# Existing rules\r\n\r\n## Tradutor TFD\r\n\r\nMy changes.\r\n"
            instructions.write_bytes(original)
            self.assertEqual(install_tfd.configure_instructions(profile, "Another version"), "existing-section")
            self.assertEqual(instructions.read_bytes(), original)

    def test_rejects_marketplace_revision_that_does_not_match_main(self):
        with patch.object(install_tfd, "codex", side_effect=[
            {"marketplaces": []}, {"installedRoot": "/test/marketplace"},
        ]), patch.object(install_tfd, "run", return_value="a" * 40):
            with self.assertRaisesRegex(ValueError, "expected"):
                install_tfd.setup_source("b" * 40)

    def test_marketplace_status_allows_only_the_codex_install_receipt(self):
        revision = "a" * 40
        receipt = "?? .codex-marketplace-install.json"
        for changes, accepted in ((receipt, True), (f"{receipt}\n?? other.py", False)):
            with self.subTest(changes=changes), patch.object(install_tfd, "codex", side_effect=[
                {"marketplaces": []}, {"installedRoot": "/test/marketplace"},
            ]), patch.object(install_tfd, "run", side_effect=[revision, changes]):
                if accepted:
                    self.assertEqual(install_tfd.setup_source(revision), Path("/test/marketplace"))
                else:
                    with self.assertRaisesRegex(ValueError, "local changes"):
                        install_tfd.setup_source(revision)
