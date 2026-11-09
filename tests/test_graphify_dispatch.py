# Contexto TFD · 573 palavras · 1396 tokens (o200k_base)

import importlib.util
import json
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import graphify


class GraphifyDispatchTests(unittest.TestCase):
    def test_host_output_preserves_unicode_even_with_ascii_console(self):
        buffer = io.BytesIO()
        console = io.TextIOWrapper(buffer, encoding='ascii', write_through=True)
        with patch.object(graphify, 'settings', return_value={}), patch.object(
                graphify, 'execute', return_value={'status': 'INDEX_MISSING', 'excerpt': '\u4f7f\u7528'}), \
                patch.object(sys, 'argv', ['graphify.py', 'query', 'gates']), patch.object(sys, 'stdout', console):
            self.assertEqual(graphify.main(), 0)
        self.assertEqual(json.loads(buffer.getvalue())['excerpt'], '\u4f7f\u7528')

    def test_final_ascii_json_respects_byte_cap_after_unicode_escaping(self):
        for context in (chr(0x4f7f) * 2000, chr(0x1f9ea) * 1500):
            result = {'status': 'GRAPHIFY', 'mandatory_reads_preserved': True,
                      'graph_context': context,
                      'sources': [{'excerpt': chr(0x4f7f) * 450} for _ in range(5)]}
            output = io.StringIO()
            with patch.object(graphify, 'settings', return_value={}), patch.object(
                    graphify, 'execute', return_value=result), \
                    patch.object(sys, 'argv', ['graphify.py', 'query', 'gates']), patch.object(sys, 'stdout', output):
                self.assertEqual(graphify.main(), 0)
            self.assertLessEqual(len(output.getvalue().encode('utf-8')), 16000)
            parsed = json.loads(output.getvalue())
            self.assertEqual(parsed['status'], 'GRAPHIFY')
            self.assertTrue(parsed['mandatory_reads_preserved'])
            self.assertTrue(parsed['graph_context'])
            self.assertTrue(parsed['output_truncated'])
            self.assertEqual(len(result['sources']), 5)

    def test_windows_paths_are_passed_as_arguments_without_a_shell(self):
        settings = {'python': '/opt/tfd/bin/python', 'wsl_distribution': 'kali-linux'}
        command = graphify.command(settings, 'query', Path('C:/TFD Bundle'),
                                   Path('C:/Private/index.json'), 'approval; echo injected')
        self.assertEqual(command[:5], ['wsl.exe', '-d', 'kali-linux', '--exec', '/opt/tfd/bin/python'])
        self.assertIn('/mnt/c/TFD Bundle/integrations/graphify/tfd_graph.py', command)
        self.assertEqual(command[-1], 'approval; echo injected')

    def test_native_runtime_does_not_use_wsl(self):
        settings = {'python': '/opt/tfd/bin/python'}
        command = graphify.command(settings, 'rebuild', Path('/repo/tfd'), Path('/cache/index.json'), None)
        self.assertEqual(command[:2], ['/opt/tfd/bin/python', '-B'])
        self.assertNotIn('wsl.exe', command)
        self.assertNotIn('--query', command)

    def test_native_query_override_keeps_explicit_rebuild_in_wsl(self):
        config = {'python': '/env/python', 'wsl_distribution': 'kali-linux',
                  'query_python': 'C:/env/Scripts/python.exe'}
        bundle, index = Path('C:/TFD'), Path('C:/Private/index.json')
        query = graphify.command(config, 'query', bundle, index, 'gates')
        self.assertEqual(query[0], config['query_python'])
        self.assertNotIn('wsl.exe', query)
        self.assertIn(str(bundle / 'integrations/graphify/tfd_graph.py'), query)
        self.assertEqual(graphify.command(config, 'rebuild', bundle, index, None)[0], 'wsl.exe')

    def test_missing_runtime_uses_fresh_lexical_fallback_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'agents').mkdir()
            (root / 'skills').mkdir()
            (root / 'README.md').write_text('# Approval\nApproval requires human evidence.\n')
            index = root.parent / (root.name + '-missing-index.json')
            result = graphify.execute({}, 'query', root, index, 'Approval')
            self.assertEqual(result['status'], 'INDEX_MISSING')
            self.assertTrue(result['sources'])
            self.assertTrue(result['mandatory_reads_preserved'])
            self.assertFalse(index.exists())

    def test_unavailable_wsl_falls_back_but_rebuild_never_claims_success(self):
        settings = {'python': '/env/python', 'wsl_distribution': 'kali-linux'}
        with patch.object(graphify.subprocess, 'run', side_effect=OSError('WSL missing')):
            with patch.object(graphify, 'fallback', return_value={'status': 'INDEX_MISSING'}) as fallback:
                result = graphify.execute(settings, 'query', ROOT, Path('C:/Private/index.json'), 'gates')
                self.assertEqual(result['runtime_status'], 'UNAVAILABLE')
                fallback.assert_called_once()
            with self.assertRaisesRegex(ValueError, 'runtime failed'):
                graphify.execute(settings, 'rebuild', ROOT, Path('C:/Private/index.json'), None)

    def test_invalid_config_is_rejected_instead_of_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.json'
            for settings in ({'python': 'relative/python'},
                             {'python': '/env/python', 'wsl_distribution': '--exec'}):
                path.write_text(json.dumps(settings))
                with self.assertRaises(ValueError):
                    graphify.settings(path)

    def test_all_tool_using_native_roles_receive_query_route_but_not_translator(self):
        from install_codex_agents import native_profiles
        profiles = {name: instructions for name, _, instructions in native_profiles()}
        for name, instructions in profiles.items():
            with self.subTest(role=name):
                if name == 'tfd_translator':
                    self.assertNotIn('scripts/graphify.py', instructions)
                else:
                    self.assertIn('scripts/graphify.py', instructions)
                    self.assertIn('mandatory', instructions)


if __name__ == '__main__':
    unittest.main()
