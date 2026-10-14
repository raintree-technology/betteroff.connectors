"""Verify distribution drift checks and preservation of unexpected files."""
from pathlib import Path
import tempfile
import unittest

from sync_skills import sync


class SkillSyncTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / 'plugins/betteroff/skills/review'
        self.source.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('Canonical workflow\n')
        (self.source / 'agents').mkdir()
        (self.source / 'agents/openai.yaml').write_text('interface: {}\n')

    def test_missing_and_stale_files_check_without_writing(self):
        self.assertFalse(sync(self.root, check=True))
        self.assertFalse((self.root / 'skills').exists())
        self.assertTrue(sync(self.root))
        self.assertTrue(sync(self.root, check=True))
        metadata = self.root / 'skills/review/agents/openai.yaml'
        metadata.write_text('stale\n')
        self.assertFalse(sync(self.root, check=True))
        self.assertEqual(metadata.read_text(), 'stale\n')
        self.assertTrue(sync(self.root))
        self.assertEqual(metadata.read_bytes(), (self.source / 'agents/openai.yaml').read_bytes())

    def test_unexpected_file_blocks_all_writes(self):
        target = self.root / 'skills'
        target.mkdir()
        extra = target / 'local-notes.md'
        extra.write_text('Preserve me\n')
        for check in (False, True):
            with self.assertRaisesRegex(ValueError, 'unexpected'):
                sync(self.root, check=check)
        self.assertEqual(extra.read_text(), 'Preserve me\n')
        self.assertFalse((target / 'review').exists())

    def test_symlink_is_rejected_without_touching_destination(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.root / 'skills').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            sync(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_core_rules_come_from_one_source(self):
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/core_rules.md').write_text('- Shared rule.\n')
        skill = self.source / 'SKILL.md'
        skill.write_text('# Review\n\n## Core rules\n\n- Edited copy.\n\n## Read\n\nSteps\n')
        self.assertTrue(sync(self.root))
        self.assertTrue(sync(self.root, check=True))
        expected = '# Review\n\n## Core rules\n\n- Shared rule.\n\n## Read\n\nSteps\n'
        self.assertEqual(skill.read_text(), expected)
        self.assertEqual((self.root / 'skills/review/SKILL.md').read_text(), expected)
        skill.write_text(expected.replace('Shared rule', 'Local edit'))
        self.assertFalse(sync(self.root, check=True))
        self.assertIn('Local edit', skill.read_text())

    def test_empty_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaisesRegex(ValueError, 'missing or empty'):
                sync(Path(empty))


if __name__ == '__main__':
    unittest.main()
