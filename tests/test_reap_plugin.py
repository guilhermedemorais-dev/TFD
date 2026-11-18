"""Exercise standalone packaging; synthetic source trees stay in temporary folders."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import reap_plugin


class TestReapPlugin(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)
        self.source = self.parent / "source"
        self.source.mkdir()
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Fixture")
        self.run_git("config", "user.email", "fixture@example.invalid")
        self.original = {}
        for index in range(26):
            name = f"reap-{index:02}"
            content = f"---\nname: {name}\ndescription: REA prompt pack: section {index}\n---\n\n# Full body {index}\nKeep all instructions.\n".encode()
            path = f"Skills/{name}/SKILL.md"
            reap_plugin.write(self.source / path, content)
            self.original[path] = content
        for name, content in {"LICENSE": b"MIT fixture\n", "README.md": b"Whole source\n", "setup.sh": b"do-not-run-fixture\n"}.items():
            reap_plugin.write(self.source / name, content)
            self.original[name] = content
        self.run_git("add", ".")
        self.run_git("-c", "core.hooksPath=NUL", "commit", "-qm", "fixture")
        self.revision = self.run_git("rev-parse", "HEAD").strip()
        self.metadata = {"revision": self.revision, "repository": "https://example.invalid/reap.git",
                         "license": "MIT", "upstream_skills_path": "Skills", "upstream_skill_count": 26,
                         "plugin": "reap-prompts", "marketplace": "reap-local"}
        self.manifest = {"name": "reap-prompts", "skills": "./skills/"}
        self.output = self.parent / "marketplace"

    def run_git(self, *args):
        result = subprocess.run(["git", "-C", str(self.source), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def build(self):
        return reap_plugin.build(self.source, self.output, self.metadata, self.manifest)

    def test_all_original_files_and_complete_skill_bodies_are_preserved(self):
        result = self.build()
        self.assertEqual((result["upstream_files"], result["active_skills"]), (29, 26))
        plugin = self.output / "plugin"
        provenance = json.loads((plugin / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(set(provenance["upstream_files"]), set(self.original))
        for name, original in self.original.items():
            self.assertEqual((plugin / "upstream" / name).read_bytes(), original)
            self.assertEqual(provenance["upstream_files"][name], hashlib.sha256(original).hexdigest())
            if name.startswith("Skills/"):
                relative = name[len("Skills/"):]
                normalized = (plugin / "skills" / relative).read_bytes()
                original_header, original_body = original.split(b"---\n", 2)[1:]
                active_header, active_body = normalized.split(b"---\n", 2)[1:]
                self.assertEqual(original_body, active_body)
                original_lines = original_header.splitlines()
                active_lines = active_header.splitlines()
                self.assertEqual(original_lines[0], active_lines[0])
                description = active_lines[1].decode().split(":", 1)[1].strip()
                self.assertEqual(json.loads(description), original_lines[1].decode().split(":", 1)[1].strip())
                self.assertEqual(provenance["active_skills"][relative]["body_sha256"], hashlib.sha256(original_body).hexdigest())
        marketplace = json.loads((self.output / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugin")
        self.assertFalse((plugin / ".mcp.json").exists())

    def test_existing_output_is_never_replaced(self):
        self.output.mkdir()
        marker = self.output / "knowledge.txt"
        marker.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.build()
        self.assertEqual(marker.read_text(), "preserve")

    def test_wrong_revision_does_not_create_output(self):
        self.metadata["revision"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "HEAD differs"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_output_inside_tfd_bundle_is_rejected_without_writes(self):
        tfd = self.parent / "tfd-bundle"
        tfd.mkdir()
        output = tfd / "external-plugin"
        with patch.object(reap_plugin, "ROOT", tfd):
            with self.assertRaisesRegex(ValueError, "outside the TFD bundle"):
                reap_plugin.build(self.source, output, self.metadata, self.manifest)
        self.assertFalse(output.exists())
        self.assertEqual(list(tfd.iterdir()), [])

    def test_missing_pack_or_special_file_fails_before_output(self):
        self.metadata["upstream_skill_count"] = 27
        with self.assertRaisesRegex(ValueError, "count"):
            self.build()
        self.assertFalse(self.output.exists())
        tree = b"120000 blob " + b"1" * 40 + b"\tSkills/link\0"
        with patch.object(reap_plugin, "git", side_effect=[(self.revision + "\n").encode(), tree]):
            with self.assertRaisesRegex(ValueError, "special file"):
                reap_plugin.read_files(self.source, self.revision)

    def test_unsafe_upstream_paths_are_rejected(self):
        for name in ("../outside", "/absolute", "a/../b", "a\\b", "C:/secret", "a/NUL.txt", "a/trailing.", "a//b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                reap_plugin.safe_parts(name)

    def test_case_collisions_and_execution_fields_are_rejected(self):
        tree = b"100644 blob " + b"1" * 40 + b"\tREADME.md\0" + b"100644 blob " + b"2" * 40 + b"\treadme.md\0"
        with patch.object(reap_plugin, "git", side_effect=[(self.revision + "\n").encode(), tree, b"one"]):
            with self.assertRaisesRegex(ValueError, "Case-colliding"):
                reap_plugin.read_files(self.source, self.revision)
        self.manifest["hooks"] = "./unreviewed.json"
        with self.assertRaisesRegex(ValueError, "execution"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_invalid_skill_header_fails_before_any_output(self):
        for content in (b"no header", b"---\nname: other\ndescription: text\n---\nbody", b"---\nname: reap-x\ndescription: |\n  lines\n---\nbody"):
            with self.subTest(content=content), self.assertRaises(ValueError):
                reap_plugin.normalize_skill(content, "reap-x")


if __name__ == "__main__":
    unittest.main()
