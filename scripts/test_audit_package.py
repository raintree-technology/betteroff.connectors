"""Check inline OpenAI metadata and generated Gemini skill drift independently."""
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
            for name in ('plugins', 'skills', '.agents', '.claude-plugin'):
                shutil.copytree(ROOT / name, target / name)
            for name in ('README.md', 'gemini-extension.json'):
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

if __name__ == '__main__':
    unittest.main()
