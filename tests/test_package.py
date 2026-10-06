"""Tests reproducibles del paquete y de los hooks con el contrato de Codex."""
from pathlib import Path
import ast
import json
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'alfred-dev-codex'


class PackageTests(unittest.TestCase):
    def test_catalog_resolves_to_matching_plugin(self):
        catalog = json.loads((ROOT/'.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        entry = catalog['plugins'][0]
        target = (ROOT/entry['source']['path']).resolve()
        self.assertEqual(target, PLUGIN.resolve())
        manifest = json.loads((target/'plugin.json').read_text(encoding='utf-8'))
        overlay = json.loads((target/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(catalog['name'], 'alfred-dev-codex')
        self.assertEqual(entry['name'], manifest['name'])
        self.assertEqual(manifest['name'], overlay['name'])
        interface = manifest['extensions']['com.openai']['interface']
        self.assertEqual(interface, overlay['interface'])
        self.assertLessEqual(len(interface['shortDescription']), 30)

    def test_python_syntax_and_no_runtime_data(self):
        for path in PLUGIN.rglob('*.py'):
            with self.subTest(path=path.relative_to(PLUGIN)):
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        self.assertFalse(list(PLUGIN.rglob('*.db')))
        self.assertEqual(len(list((PLUGIN/'skills').glob('*/SKILL.md'))), 29)
        self.assertEqual(len(list((PLUGIN/'agents').glob('*.md'))), 10)

    def test_hook_commands_and_references(self):
        hooks = json.loads((PLUGIN/'hooks/hooks.json').read_text(encoding='utf-8'))
        for event, groups in hooks['hooks'].items():
            for group in groups:
                for hook in group['hooks']:
                    with self.subTest(event=event, command=hook['command']):
                        self.assertNotIn('args', hook)
                        self.assertIn('${PLUGIN_ROOT}', hook['command'])
                        self.assertIn('$env:PLUGIN_ROOT', hook['commandWindows'])
                        relative = hook['command'].split('${PLUGIN_ROOT}/', 1)[1].rstrip('"')
                        self.assertTrue((PLUGIN/relative).is_file())

    def run_hook(self, name, payload):
        env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
        return subprocess.run([sys.executable, str(PLUGIN/'hooks'/name)],
                              input=json.dumps(payload), capture_output=True,
                              text=True, encoding='utf-8', env=env, timeout=10)

    def test_canonical_apply_patch_blocks_added_secret(self):
        # A synthetic AWS-looking key, not an actual credential.
        key = 'AKIA' + 'ABCDEFGHIJKLMNOP'
        patch = '*** Begin Patch\n*** Add File: example.py\n+key="' + key + '"\n*** End Patch'
        result = self.run_hook('secret-guard.py', {
            'tool_name': 'apply_patch', 'tool_input': {'command': patch}})
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_canonical_apply_patch_allows_normal_content(self):
        patch = '*** Begin Patch\n*** Add File: example.py\n+text="ordinary"\n*** End Patch'
        result = self.run_hook('secret-guard.py', {
            'tool_name': 'apply_patch', 'tool_input': {'command': patch}})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dangerous_command_is_blocked_without_executing_it(self):
        result = self.run_hook('dangerous-command-guard.py', {
            'tool_name': 'Bash', 'tool_input': {'command': 'rm -rf /'}})
        self.assertEqual(result.returncode, 2, result.stderr)


if __name__ == '__main__':
    unittest.main()
