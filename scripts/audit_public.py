#!/usr/bin/env python3
"""Reject private files and workstation paths in Git's publication inventory."""
import pathlib
import re
import subprocess
import sys

SECRET_PATTERNS = (
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?:postgres(?:ql)?|https?)://[^\s/:]+:[^\s/@]+@',
    r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b',
    r'\b(?:sk_live_|rk_live_)[A-Za-z0-9]{16,}\b',
    r'\bBearer\s+[A-Za-z0-9._-]{20,}',
)


def violations(path, data):
    parts = pathlib.PurePosixPath(path).parts
    name = parts[-1]
    if ('.private' in parts or '__pycache__' in parts or name == 'todo-mcp.txt'
            or name == '.env' or (name.startswith('.env.') and name != '.env.example')
            or name.endswith(('.pem', '.key', '.pyc', '.pyo'))):
        return ['private_file']
    text = data.decode('utf-8', errors='replace')
    found = []
    if re.search(r'/(?:Users|home)/[A-Za-z0-9_.-]+/', text):
        found.append('workstation_path')
    if any(re.search(pattern, text) for pattern in SECRET_PATTERNS):
        found.append('credential_like_content')
    return found


def audit(root):
    # Inspect the index independently: a clean working copy can conceal staged content.
    staged = subprocess.run(['git', 'ls-files', '--stage', '-z'], cwd=root,
                            capture_output=True, check=True)
    failed = False
    for raw in staged.stdout.split(b'\0'):
        if not raw:
            continue
        metadata, path = raw.decode('utf-8').split('\t', 1)
        mode, oid, _ = metadata.split()
        if mode == '120000':
            print(f'symlink: {path}')
            failed = True
            continue
        if mode == '160000':
            print(f'submodule: {path}')
            failed = True
            continue
        data = subprocess.run(['git', 'cat-file', 'blob', oid], cwd=root,
                              capture_output=True, check=True).stdout
        for code in violations(path, data):
            print(f'{code}: {path} (index)')
            failed = True
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root,
                            capture_output=True, check=True)
    for raw in result.stdout.split(b'\0'):
        if not raw:
            continue
        path = raw.decode('utf-8')
        file = root / path
        if file.is_symlink():
            print(f'symlink: {path}')
            failed = True
            continue
        if not file.exists():
            continue  # A deleted tracked file will not be published in the next commit.
        for code in violations(path, file.read_bytes()):
            print(f'{code}: {path}')
            failed = True
    if not failed:
        print('Public file inventory passed')
    return int(failed)


def main():
    return audit(pathlib.Path(__file__).resolve().parents[1])


if __name__ == '__main__':
    sys.exit(main())
