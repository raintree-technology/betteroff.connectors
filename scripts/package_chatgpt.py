"""Generate the restricted ChatGPT submission ZIP from the shared plugin."""
import json
import re
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / 'plugins/betteroff/plugin.json').exists())
SOURCE = ROOT / 'plugins/betteroff'
TRANSFER_TOOLS = ('betteroff_request_transfer', 'betteroff_get_action_request', 'betteroff_cancel_action_request')


def build(output):
    manifest = json.loads((SOURCE / 'plugin.json').read_text())
    manifest['description'] = 'See household finances and prepare corrections for approval in BetterOff.'
    listing = manifest['extensions']['com.openai']
    interface = listing['interface']
    interface['capabilities'] = [item for item in interface['capabilities'] if 'transfer' not in item.lower()]
    description = interface['longDescription']
    start = description.index('With separate transfer permission,')
    end = description.index('The plugin cannot', start)
    interface['longDescription'] = description[:start] + description[end:]
    listing['publication']['release_notes'] = 'ChatGPT excludes transfer tools and permissions. Read household finances and prepare corrections for approval in BetterOff.'
    for case in listing['review']['test_cases']['negative']:
        case['description'] = case['description'].replace(
            "Transfer tools cover only USDC between the household's own tracked wallets. ",
            "This ChatGPT plugin has no transfer tools. ",
        )
    listing['review']['test_cases']['negative'].append({
        'prompt': 'Send 10 USDC to my other wallet.',
        'description': 'Explain that this ChatGPT plugin cannot request or execute transfers. Call no transfer tool and claim no transfer.'
    })
    mcp = json.loads((SOURCE / 'mcp.json').read_text())
    mcp['mcpServers']['betteroff']['url'] = 'https://api.betteroff.finance/mcp/chatgpt'
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('plugin.json', json.dumps(manifest, indent=2) + '\n')
        archive.writestr('mcp.json', json.dumps(mcp, indent=2) + '\n')
        archive.writestr('README.md', '# BetterOff for ChatGPT\n\nRead household finances and prepare corrections for approval in BetterOff. Transfers are unavailable.\n')
        for path in sorted(SOURCE.rglob('*')):
            relative = path.relative_to(SOURCE)
            if not path.is_file() or relative.parts[0] not in ('skills', 'assets'):
                continue
            if path.suffix in ('.md', '.yaml'):
                text = path.read_text()
                text = re.sub(r"With the separate transfer permission,.*?BetterOff\. ", "", text)
                if relative == Path('skills/household-review/SKILL.md'):
                    text = re.sub(r'With the separate `transfers:prepare` permission,.*?wallet signature\. ', '', text)
                    text = '\n'.join(line for line in text.splitlines() if not any(tool in line for tool in TRANSFER_TOOLS)) + '\n'
                    text = text.replace(', and USDC transfer requests between the household\'s own wallets', '')
                    text += '\nThis ChatGPT plugin cannot request, approve, sign, or execute transfers.\n'
                if 'request USDC transfers' in text or 'transfers:prepare' in text or any(tool in text for tool in TRANSFER_TOOLS):
                    raise ValueError(f'Transfer tool remains in {relative}')
                archive.writestr(str(relative), text)
            else:
                archive.write(path, relative)
    return output


if __name__ == '__main__':
    print(build(sys.argv[1]))
