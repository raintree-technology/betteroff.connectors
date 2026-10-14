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
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers']['betteroff']['url'], 'https://api.betteroff.finance/mcp')
                for entry in archive.namelist():
                    if entry.startswith('skills/'):
                        self.assertNotIn('<!-- transfers', archive.read(entry).decode())
                        self.assertNotIn('prepare wallet transfers', archive.read(entry).decode())
                        for name in TRANSFER_TOOLS:
                            self.assertNotIn(name, archive.read(entry).decode())
                        self.assertNotIn('transfers:bank', archive.read(entry).decode())
                        self.assertNotIn('transfers:vault', archive.read(entry).decode())
                manifest = json.loads(archive.read('plugin.json'))
                listing = manifest['extensions']['com.openai']
                self.assertEqual(len(listing['review']['test_cases']['positive']), 5)
                self.assertEqual(len(listing['review']['test_cases']['negative']), 3)
                self.assertNotIn('With separate transfer permission', listing['interface']['longDescription'])
                for case in listing['review']['test_cases']['negative']:
                    self.assertNotIn('Transfer tools cover only USDC', case['description'])
                skill = archive.read('skills/household-review/SKILL.md').decode()
                self.assertIn('individualized investment, tax, or legal advice', skill)
                self.assertIn('description: Reads BetterOff household finances and prepares corrections for '
                              'authenticated user review in BetterOff. Use for accounts', skill)
                self.assertIn('financial findings, and permitted financial activity.', skill)
                for name in TRANSFER_TOOLS:
                    self.assertNotIn(name, skill)
                self.assertNotIn('transfers:prepare', skill)
        self.assertEqual(before, (SOURCE / 'plugin.json').read_bytes())

if __name__ == '__main__':
    unittest.main()
