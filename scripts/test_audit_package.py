"""Check inline OpenAI metadata, Gemini skill drift, and client manifest metadata drift independently."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class PackageAuditTests(unittest.TestCase):
    def test_inline_metadata_and_native_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory)
            for name in ('plugins', 'skills', '.agents', '.claude-plugin', '.cursor-plugin'):
                shutil.copytree(ROOT / name, target / name)
            for name in ('README.md', 'COMPATIBILITY.md', 'gemini-extension.json'):
                shutil.copyfile(ROOT / name, target / name)
            def audit():
                return subprocess.run(['python3', str(ROOT / 'scripts/audit_package.py'), directory], capture_output=True, text=True)
            self.assertEqual(audit().returncode, 0)
            manifest = target / 'plugins/betteroff/plugin.json'
            original = manifest.read_text()
            data = json.loads(original)
            data['extensions']['com.openai']['review']['test_cases']['positive'][0]['unsupported'] = True
            manifest.write_text(json.dumps(data))
            result = audit()
            self.assertEqual(result.returncode, 1)
            self.assertIn('positive_fields', result.stdout)
            manifest.write_text(original)
            (target / 'skills/household-review/SKILL.md').write_text('stale')
            result = audit()
            self.assertEqual(result.returncode, 1)
            self.assertIn('gemini_skill_drift', result.stdout)
            shutil.copyfile(ROOT / 'skills/household-review/SKILL.md', target / 'skills/household-review/SKILL.md')
            cursor = target / '.cursor-plugin/marketplace.json'
            data = json.loads(cursor.read_text())
            data['owner']['name'] = 'Someone Else'
            data['plugins'][0]['source'] = './plugins/missing'
            cursor.write_text(json.dumps(data))
            result = audit()
            self.assertEqual(result.returncode, 1)
            self.assertIn('developer_name_drift', result.stdout)
            self.assertIn('cursor_marketplace_source_path', result.stdout)

    def test_client_metadata_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory)
            for name in ('plugins', 'skills', '.agents', '.claude-plugin', '.cursor-plugin'):
                shutil.copytree(ROOT / name, target / name)
            for name in ('README.md', 'COMPATIBILITY.md', 'gemini-extension.json'):
                shutil.copyfile(ROOT / name, target / name)
            manifest = target / 'plugins/betteroff/.cursor-plugin/plugin.json'
            data = json.loads(manifest.read_text())
            data['author'] = {'name': 'Someone Else'}
            manifest.write_text(json.dumps(data))
            result = subprocess.run(['python3', str(ROOT / 'scripts/audit_package.py'), directory], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('metadata_drift: plugins/betteroff/.cursor-plugin/plugin.json: author', result.stdout)

if __name__ == '__main__':
    unittest.main()
