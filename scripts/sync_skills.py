"""Write scripts/core_rules.md into each plugin skill's Core rules section, then copy the plugin
skills to Gemini; --check reports drift without writing."""
import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# The section ends at the next heading or, when it is the last section, at the end of the file.
CORE_RULES = re.compile(r'(^## Core rules\n\n).*?(?=^## |\Z)', re.M | re.S)


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


def apply_core_rules(root, check):
    """Return skills whose Core rules section differs from the shared source; fix them unless checking."""
    rules = root / 'scripts/core_rules.md'
    if not rules.is_file():
        return []
    rules_text = rules.read_text()
    changed = []
    for skill in sorted((root / 'plugins/betteroff/skills').glob('*/SKILL.md')):
        text = skill.read_text()
        updated = CORE_RULES.sub(
            lambda match: match.group(1) + rules_text + ('' if match.end() == len(text) else '\n'), text)
        if updated != text:
            changed.append(skill.relative_to(root))
            if not check:
                skill.write_text(updated)
    return changed


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
    stale_rules = apply_core_rules(root, check)
    if stale_rules and not check:
        expected = inventory(source)
    changed = [path for path in expected if actual.get(path) != expected[path]]
    if check:
        for path in stale_rules:
            print(f'Core rules drift: {path}')
        for path in changed:
            print(f'Skill drift: skills/{path}')
        return not changed and not stale_rules
    for path in stale_rules:
        print(f'Updated core rules in {path}')
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
