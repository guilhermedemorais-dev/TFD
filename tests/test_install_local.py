# Contexto TFD · 598 palavras · 1272 tokens (o200k_base)

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests import test_install_tfd as fixtures
import install_local as local


class TestLocalUpdate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.origin = self.root / "origin"
        self.profile = self.root / "profile"
        self.cache = self.profile / "plugins/cache/tfd-local/the-factory-developer/0.1.6"
        self.source.mkdir()
        (self.source / ".codex-plugin").mkdir()
        (self.source / ".codex-plugin/plugin.json").write_text(json.dumps(dict(name="the-factory-developer", version="0.1.6")))
        (self.source / "library/indexes").mkdir(parents=True)
        (self.source / "library/indexes/resources.json").write_text('{"resources": []}')
        (self.source / "README.md").write_text("first\nlast\n")
        for args in (("init", "-q"), ("add", "."), ("-c", "user.name=TFD-test", "-c", "user.email=tfd-test@invalid", "commit", "-qm", "baseline")):
            subprocess.run(["git", "-C", str(self.source), *args], check=True, capture_output=True)
        self.base = local.git(self.source, "rev-parse", "HEAD").decode().strip()
        for target in (self.origin, self.cache):
            shutil.copytree(self.source, target, ignore=shutil.ignore_patterns(".git"))
            (target / "README.md").write_text("first\ncustom\nlast\n")
            (target / "extra-knowledge.md").write_text("preserve me")
        (self.source / "README.md").write_text("first\nlast\nnew\n")
        self.profile.mkdir(exist_ok=True)
        (self.profile / "config.toml").write_text("personal = true")

    def codex(self, *args):
        return {"installed": [{"pluginId": "the-factory-developer@tfd-local", "version": "0.1.6", "source": {"source": "local", "path": str(self.origin)}}]}

    def test_plan_has_no_installation_side_effects(self):
        before = local.snapshot(self.cache)
        result = local.update_local(self.profile, self.source, self.base, self.codex, True)
        self.assertEqual(result["status"], "LOCAL_PLAN")
        self.assertEqual(before, local.snapshot(self.cache))
        self.assertFalse((self.profile / "tfd-installation.json").exists())
        self.assertFalse((self.profile / "tfd-local-backups").exists())

    def test_update_preserves_custom_content_config_and_paths(self):
        result = local.update_local(self.profile, self.source, self.base, self.codex)
        for target in (self.origin, self.cache):
            self.assertEqual((target / "README.md").read_text(), "first\ncustom\nlast\nnew\n")
            self.assertEqual((target / "extra-knowledge.md").read_text(), "preserve me")
        self.assertEqual((self.profile / "config.toml").read_text(), "personal = true")
        self.assertTrue((Path(result["backup_path"]) / "manifest.json").is_file())
        self.assertEqual(json.loads((self.profile / "tfd-installation.json").read_text())["local_base"], self.base)

    def test_conflict_leaves_both_packages_unchanged(self):
        (self.source / "README.md").write_text("replaced\n")
        before = [local.snapshot(target) for target in (self.origin, self.cache)]
        with self.assertRaises(ValueError):
            local.update_local(self.profile, self.source, self.base, self.codex)
        self.assertEqual(before, [local.snapshot(target) for target in (self.origin, self.cache)])

    def test_partial_failure_rolls_back_and_does_not_advance_receipt(self):
        before = [local.snapshot(target) for target in (self.origin, self.cache)]
        real = local.atomic_bytes
        calls = []
        def injected(path, data):
            calls.append(path)
            if len(calls) == 2:
                raise OSError("injected write failure")
            return real(path, data)
        with patch.object(local, "atomic_bytes", side_effect=injected):
            with self.assertRaises(OSError):
                local.update_local(self.profile, self.source, self.base, self.codex)
        self.assertEqual(before, [local.snapshot(target) for target in (self.origin, self.cache)])
        self.assertFalse((self.profile / "tfd-installation.json").exists())

    def test_patch_handles_line_indentation_crlf_and_header_insertions(self):
        old = b"        work()\r\n"
        current = b"        work()\n            work()\n"
        self.assertEqual(local.patch_bytes(old, b"        changed()\n", current), b"        changed()\n            work()\n")
        self.assertEqual(local.patch_bytes(b"title\n", b"header\ntitle\n", b"title\n"), b"header\ntitle\n")

    def test_repeated_update_is_idempotent_with_retained_extensions(self):
        local.update_local(self.profile, self.source, self.base, self.codex)
        first = [local.snapshot(target) for target in (self.origin, self.cache)]
        result = local.update_local(self.profile, self.source, self.base, self.codex)
        self.assertEqual(result["changed_files"], [])
        self.assertEqual(first, [local.snapshot(target) for target in (self.origin, self.cache)])

    def test_source_outside_package_is_not_installed(self):
        (self.source / "private.env").write_text("private")
        local.update_local(self.profile, self.source, self.base, self.codex)
        self.assertFalse((self.cache / "private.env").exists())
