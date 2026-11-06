import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install_codex_agents import install, native_profiles


class TestCodexAdapter(unittest.TestCase):
    def test_registers_native_roles_without_overwriting_custom_profiles(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            custom = destination / "tfd_translator.toml"
            custom.write_text('name = "personal"\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "custom profile"):
                install(destination)
            self.assertEqual(list(destination.iterdir()), [custom])
            self.assertEqual(custom.read_text(encoding="utf-8"), 'name = "personal"\n')
            custom.unlink()
            self.assertEqual(install(destination), 15)
            first = custom.read_bytes()
            self.assertEqual(install(destination), 15)
            self.assertEqual(custom.read_bytes(), first)
            profiles = {name: instructions for name, _, instructions in native_profiles()}
            self.assertIn("Reply to the user in Brazilian Portuguese", profiles["tfd_translator"])
            self.assertIn("read-only operations", profiles["tfd_harness"])

    def test_marketplace_resolves_native_plugin_and_sector_skills(self):
        market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        entry, = market["plugins"]
        self.assertEqual(entry["source"]["source"], "local")
        package = (ROOT / entry["source"]["path"]).resolve()
        self.assertEqual(package, ROOT)
        manifest = json.loads((package / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], entry["name"])
        skills = package / manifest["skills"]
        self.assertTrue((skills / "TFD-harness/SKILL.md").is_file())
        agents = sorted(package.glob("agents/*/agent.json"))
        self.assertEqual(len(agents), 14)
        for agent_file in agents:
            agent = json.loads(agent_file.read_text(encoding="utf-8"))
            for name in agent["skills"]:
                with self.subTest(skill=name):
                    self.assertTrue((skills / name / "SKILL.md").is_file())

    def test_translator_is_routed_as_handoff_support(self):
        descriptor = ROOT / "agents/TFD-translator/agent.json"
        agent = json.loads(descriptor.read_text(encoding="utf-8"))
        positive = {"resume o que eu falei para o agente de frontend",
                    "compacta e traduz esse pedido para o setor de banco"}
        self.assertTrue(positive <= set(agent["activates_on"]))
        self.assertNotIn("corrige a migration de clientes", agent["activates_on"])
        self.assertEqual(agent["gate"], "handoff")
        self.assertEqual(agent["validator"], "TFD-harness")
        skill = ROOT / "skills/tfd-translator/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 150)
        self.assertLessEqual(len(text.splitlines()[2].split()), 61)
        harness = ROOT / "skills/TFD-harness/SKILL.md"
        self.assertIn("../tfd-translator/SKILL.md", harness.read_text(encoding="utf-8"))

    def test_metering_is_packaged_as_a_skill_using_the_existing_readers(self):
        harness = ROOT / "skills/TFD-harness/SKILL.md"
        skill = (harness.parent / "../tfd-token-usage/SKILL.md").resolve()
        text = skill.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 150)
        self.assertLessEqual(len(text.splitlines()[2].split()), 61)
        self.assertIn("../tfd-token-usage/SKILL.md", harness.read_text(encoding="utf-8"))
        for reader in ("scripts/token_usage.py", "scripts/context_budget.py"):
            self.assertIn(reader, text)
            self.assertTrue((ROOT / reader).is_file())
        self.assertFalse((ROOT / "hooks/hooks.json").exists())
