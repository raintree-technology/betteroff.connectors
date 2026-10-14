"""Copy canonical plugin skills to Gemini; --check reports drift without writing."""
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def inventory(directory):
    if directory.is_symlink():
        raise ValueError(f"Refusing symlink: {directory}")
    files = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f"Refusing symlink: {path}")
        if path.is_file():
            files[path.relative_to(directory)] = path.read_bytes()
    return files


def sync(root, check=False):
    source = root / 'plugins/betteroff/skills'
    target = root / 'skills'
    expected, actual = inventory(source), inventory(target)
    if not expected:
        raise ValueError('Canonical plugin skills are missing or empty')
    extra = actual.keys() - expected.keys()
    if extra:
        raise ValueError('Review unexpected Gemini files before syncing: ' +
                         ', '.join(str(path) for path in sorted(extra)))
    changed = [path for path in expected if actual.get(path) != expected[path]]
    if check:
        for path in changed:
            print(f'Skill drift: skills/{path}')
        return not changed
    for path in changed:
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(expected[path])
        print(f'Updated skills/{path}')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        success = sync(ROOT, args.check)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
    parser.exit(0 if success else 1)
