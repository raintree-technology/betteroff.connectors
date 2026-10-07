"""Verify publication boundaries without printing private file contents."""
import unittest
import contextlib
import io
import pathlib
import subprocess
import tempfile
from audit_public import audit, violations


class PublicAuditTests(unittest.TestCase):
    def test_private_files_are_rejected_even_when_force_added(self):
        for path in ('.private/review.md', 'todo-mcp.txt', '.env', '.env.production',
                     'credentials.pem', 'oauth.key', 'scripts/__pycache__/audit.pyc'):
            with self.subTest(path=path):
                self.assertEqual(violations(path, b''), ['private_file'])

    def test_workstation_paths_are_rejected(self):
        for prefix in ('Users', 'home'):
            text = f'/{prefix}/reviewer/private/report.md'.encode()
            self.assertEqual(violations('COMPATIBILITY.md', text), ['workstation_path'])

    def test_public_contract_and_examples_are_allowed(self):
        text = b'https://api.betteroff.finance/mcp; synthetic USD 100; ~/.config/client'
        self.assertEqual(violations('README.md', text), [])
        self.assertEqual(violations('.env.example', b'API_KEY='), [])

    def test_credentials_are_rejected_in_images_and_text(self):
        token = ('gh' + 'p_' + 'a' * 36).encode()
        for path in ('README.md', 'assets/icon.png'):
            self.assertEqual(violations(path, token), ['credential_like_content'])

    def test_staged_secret_is_rejected_after_working_file_is_cleaned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(['git', 'init', '-q', directory], check=True)
            file = root / 'README.md'
            token = 'gh' + 'p_' + 'a' * 36
            file.write_text(token)
            subprocess.run(['git', 'add', 'README.md'], cwd=root, check=True)
            file.write_text('Public documentation')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(audit(root), 1)
            self.assertIn('(index)', output.getvalue())
            self.assertNotIn(token, output.getvalue())

    def test_force_added_private_file_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(['git', 'init', '-q', directory], check=True)
            (root / '.gitignore').write_text('.private/\n')
            (root / '.private').mkdir()
            (root / '.private' / 'report.txt').write_text('Private report')
            (root / 'public-link').symlink_to('.private/report.txt')
            subprocess.run(['git', 'add', '-f', '.private/report.txt', 'public-link'],
                           cwd=root, check=True)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(audit(root), 1)
            self.assertIn('private_file:', output.getvalue())
            self.assertIn('symlink:', output.getvalue())


if __name__ == '__main__':
    unittest.main()
