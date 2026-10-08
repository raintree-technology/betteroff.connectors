import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from package_chatgpt import build, SOURCE, TRANSFER_TOOLS

class ChatgptPackageTest(unittest.TestCase):
    def test_restricted_package_preserves_shared_source(self):
        before = (SOURCE / 'plugin.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            with ZipFile(build(Path(directory) / 'chatgpt.zip')) as archive:
                self.assertIn('https://api.betteroff.finance/mcp/chatgpt', archive.read('mcp.json').decode())
                for entry in archive.namelist():
                    if entry.startswith('skills/'):
                        self.assertNotIn('request USDC transfers', archive.read(entry).decode())
                manifest = json.loads(archive.read('plugin.json'))
                listing = manifest['extensions']['com.openai']
                self.assertNotIn('With separate transfer permission', listing['interface']['longDescription'])
                for case in listing['review']['test_cases']['negative']:
                    self.assertNotIn('Transfer tools cover only USDC', case['description'])
                skill = archive.read('skills/household-review/SKILL.md').decode()
                self.assertIn('individualized investment, tax, or legal advice', skill)
                for name in TRANSFER_TOOLS:
                    self.assertNotIn(name, skill)
                self.assertNotIn('transfers:prepare', skill)
        self.assertEqual(before, (SOURCE / 'plugin.json').read_bytes())

if __name__ == '__main__':
    unittest.main()
