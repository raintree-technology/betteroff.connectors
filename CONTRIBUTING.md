<picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# Contributing to BetterOff connectors

[All clients](README.md#install-the-connector) · [Connector reference](docs/connector.md)

Use this guide to find the source for each kind of documentation and run repository checks.

## Documentation map

| Reader or task | Canonical document |
| --- | --- |
| Install a client and choose a workflow | [Installation guide](README.md) |
| Check client verification and its limits | [Client guides](README.md#install-the-connector) |
| Understand permissions, data, and approval boundaries | [Connector reference](docs/connector.md) |
| Change an agent workflow | `plugins/betteroff/skills/<name>/SKILL.md` |
| Prepare directory submissions and inspect recorded evidence | [Directory guide](integrations/directories/README.md) |
| Build and validate the Zapier integration | [Zapier private preview guide](integrations/zapier/README.md) |
| Investigate Glama's OAuth callback | [Reproduction and relay experiment](integrations/directories/README.md#glama-oauth-callback-handoff-reproduction) |
| Check client artwork attribution | [Logo sources](README.md#client-logo-sources) |

Edit the document that owns the information:

- Use the root README to help readers choose a client or workflow.
- Keep each client’s setup, sign-in, troubleshooting, and test limits in `docs/clients/<client>.md`. Group related apps and command-line tools in that guide.
- Keep shared capabilities, permissions, approval rules, and data limits in `docs/connector.md`.
- Keep submission fields and publication status in the directory guide.
- Link to these documents from the packaged README instead of copying their contents.

Apply the [functional writing standard](https://github.com/raintree-technology/raintree.standards/blob/main/writing/functional.md) when editing documentation. Put prerequisites before numbered steps and state how readers can check the result. Preserve exact commands, permissions, and qualifications.

Use relative links between repository documents and local assets. Link to a section when readers need a specific procedure. Keep absolute GitHub links in the packaged plugin README because installed copies do not include the repository’s documentation. Keep logos outside headings so heading anchors remain stable, and use empty image alternatives when nearby text names the client.

Show each client’s verification limits before setup steps and in the root README. Distinguish private tests, unsubmitted drafts, approval status, and published metadata. Do not upgrade a status without dated evidence for that destination.

Date official-source reviews separately from BetterOff tests. A documentation review does not verify a working connection. Preserve earlier test dates and limits when adding new evidence.

`todo-mcp.txt` and `.private/` are ignored local operational material. Keep credentials and private reviewer material out of public documentation.

## Agent workflow sources

The plugin's `skills/` directory is the editing source. Root `skills/` mirrors it for Gemini CLI. Both distributions need complete, standalone workflows, including their core interpretation and approval rules.

1. Edit `plugins/betteroff/skills/<name>/SKILL.md` and its `agents/openai.yaml` when applicable.
2. Run `python3 scripts/sync_skills.py` to update the Gemini distribution. Root `skills/` is generated; do not edit it directly.
3. Run `python3 scripts/sync_skills.py --check` and the package audit below. CI checks every distributed file, including agent metadata. Unexpected files require manual review; the sync command never deletes them.

Keep both copies as regular files. Do not replace a workflow with a link to another skill: clients can install each workflow independently.

## Contribution checks

Changes reach `main` only through pull requests. Branch protection applies to administrators, every commit must be signed, and the `package` check must pass before a pull request can merge.

The **Audit** workflow in `.github/workflows/audit.yml` runs two jobs:

- **`package`** runs on pull requests, pushes to `main`, and manual runs. It tests and runs the public-content and package audits, scans the full Git history with gitleaks, and validates the marketplace and the plugin with `claude plugin validate --strict`.
- **`server`** runs daily and on manual runs. It checks the live MCP endpoint's OAuth discovery, token rejection, HTTPS redirect, HSTS, and CORS behavior. It does not run on pull requests, so a server outage cannot block a merge.

To run the same checks before you open a pull request, run these commands from the repository root. The server check needs `curl` and `jq`.

```sh
python3 scripts/test_audit_public.py && python3 scripts/audit_public.py
python3 scripts/test_audit_package.py && python3 scripts/audit_package.py
python3 scripts/test_package_chatgpt.py
python3 scripts/test_sync_skills.py && python3 scripts/sync_skills.py --check
gitleaks git --redact --no-banner .
claude plugin validate --strict . && claude plugin validate --strict plugins/betteroff
scripts/audit_server.sh
```

Dependabot proposes GitHub Actions updates weekly and waits seven days after each release. Update the other two pinned tools by hand in `audit.yml`:

- **gitleaks:** change `GITLEAKS_VERSION` and `GITLEAKS_SHA256` together. Take the hash from the `linux_x64` line of the release's `checksums.txt`.
- **Claude Code:** `--strict` validation needs version 2.1.281 or later. Bump it deliberately and confirm that validation still passes.

## ChatGPT submission package

**Submission preparation only — public approval and listing unverified in this repository.** A generated ZIP is not an approved directory integration.

Generate the ChatGPT ZIP separately from the shared client plugin:

```sh
python3 scripts/package_chatgpt.py /tmp/betteroff-chatgpt.zip
```

The generator uses `https://api.betteroff.finance/mcp`, the URL fixed at OpenAI registration. It removes transfer tools and transfer instructions from the ZIP. The generator documents a server restriction for the verified ChatGPT client; verify that restriction through an authenticated ChatGPT test before uploading for review. Package filtering alone does not establish server enforcement.

## Client verification

Earlier HTTP checks with synthetic data covered the tool catalog, permission enforcement, correction review and undo, token rotation, and denied access after disconnection. These server checks do not verify each client’s behavior.

Full client verification must cover installation, skill loading, consent,
permitted tool discovery, populated reads, missing-data responses, correction
preparation, token renewal, and denial after disconnection. Record the client
version, package revision, and test date when publishing results.

Check the [directory guide](integrations/directories/README.md) for publication status and directory acceptance tests. Installing this repository does not mean BetterOff is available in the ChatGPT or Claude connector directories.

### Instinct

An Instinct connection is not yet verified. On October 6, 2026, [Instinct's public site](https://instinct.com/) provided no custom MCP setup instructions, and its account app required phone sign-in before settings could be inspected. Instinct's ability to operate applications does not establish support for this connector.

Before documenting an installation route:

1. Confirm a custom MCP connection option in Instinct account settings or obtain official integration instructions.
2. Connect the endpoint using OAuth and approve the intended household and permissions in BetterOff.
3. Discover the permitted tools and run `betteroff_get_setup_status`, then `betteroff_get_overview`, against a synthetic household.
4. Verify token renewal and denied access after disconnecting in BetterOff.

Do not claim Instinct support until those checks pass. Do not paste BetterOff credentials or access tokens into an Instinct conversation.
