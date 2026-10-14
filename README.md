<picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff connectors

Connect your AI client to BetterOff to review household finances, find recurring charges, and prepare corrections for your approval.

**29 tools · eight skills · 11 client setup guides**

[Choose your client](#install-the-connector) · [Preview integrations](#preview-integrations) · [Connector reference](docs/connector.md) · [Contributing](CONTRIBUTING.md)

## Before you start

- **Account:** You need a BetterOff household owner account and a client listed below. Connect a supported account or wallet in BetterOff to ask questions about your finances.
- **Consent:** All household members must consent to AI processing, and you must accept the applicable BetterOff Terms. Data returned by a tool is shared with your connected client.
- **Plan:** Most reads are free. Recurring items, checklist progress, observations, correction proposals, and transfer requests require BetterOff Core.
- **Approval:** The connector prepares corrections for your review. With separate permissions, it can request wallet transfers, bank transfers between your own linked accounts, and vault deposits. You review each request in BetterOff. Wallet transfers and deposits require your signature; bank transfers require passkey confirmation. The connector cannot approve or execute these requests or apply a correction.

## Install the connector

Choose your client and check its recorded verification status below. No client has a fully verified connection lifecycle in the October 6, 2026 test record. The October 13 documentation review did not rerun those tests. Repository installation does not establish vendor marketplace approval or a public directory listing.

| Client guide | App or interface | Recorded verification |
| --- | --- | --- |
| [<img src="assets/clients/codex.png" alt="" width="24" height="24" align="absmiddle"> Codex](docs/clients/codex.md) | [App and CLI](docs/clients/codex.md#install-and-sign-in) | **Partially verified:** authenticated checks passed; fresh install, renewal, and revocation unverified. |
| [<img src="assets/clients/claude-code.png" alt="" width="24" height="24" align="absmiddle"> Claude Code](docs/clients/claude-code.md) | Claude Code | **Partially verified:** interactive authenticated checks passed; automated sessions and full lifecycle unverified. |
| [<img src="assets/clients/github-copilot.svg" alt="" width="24" height="24" align="absmiddle"> GitHub Copilot](docs/clients/github-copilot.md) | [VS Code](docs/clients/github-copilot.md#install-in-vs-code), [CLI](docs/clients/github-copilot.md#install-in-copilot-cli), and [app](docs/clients/github-copilot.md#github-copilot-app) | **Installation only:** CLI installed; authentication, reads, VS Code, and app installation unverified. |
| [<img src="assets/clients/cursor.svg" alt="" width="24" height="24" align="absmiddle"> Cursor](docs/clients/cursor.md) | Cursor | **Unverified connection:** plugin and MCP-only routes. |
| [<img src="assets/clients/gemini-cli.png" alt="" width="24" height="24" align="absmiddle"> Gemini CLI](docs/clients/gemini-cli.md) | Gemini CLI | **Installation only:** extension and skills loaded; authentication and reads unverified. |
| [<img src="assets/clients/devin.svg" alt="" width="24" height="24" align="absmiddle"> Devin](docs/clients/devin.md) | [Web app](docs/clients/devin.md#connect-in-the-web-app) and [CLI](docs/clients/devin.md#connect-in-the-cli) | **Unverified connection:** web app and CLI. |
| [<img src="assets/clients/hermes-agent.png" alt="" width="24" height="24" align="absmiddle"> Hermes Agent](docs/clients/hermes-agent.md) | Hermes Agent | **Partially verified:** authenticated checks passed; full lifecycle unverified. |
| [<img src="assets/clients/muse-code.svg" alt="" width="24" height="16" align="absmiddle"> Muse Code](docs/clients/muse-code.md) | Muse Code | **Unverified connection:** user, plugin, and project routes. |
| [<img src="assets/clients/openclaw.svg" alt="" width="24" height="24" align="absmiddle"> OpenClaw](docs/clients/openclaw.md) | OpenClaw | **Unverified connection:** shared and per-sender sign-in. |
| [<img src="assets/clients/pi.svg" alt="" width="24" height="24" align="absmiddle"> Pi](docs/clients/pi.md) | Pi | **Unverified connection.** |
| [<img src="assets/clients/grok.png" alt="" width="24" height="24" align="absmiddle"> Grok](docs/clients/grok.md) | [Build](docs/clients/grok.md#connect-in-grok-build), [grok.com](docs/clients/grok.md#connect-on-grokcom), and [Bot](docs/clients/grok.md#connect-in-grok-bot) | **Unverified connection:** Build, grok.com, and Bot. |

Instinct has no verified connection route. See the [verification prerequisites](CONTRIBUTING.md#instinct) before claiming support.

## Workflows and integrations

Use the [workflow picker](docs/connector.md#choose-a-workflow) for household reviews, subscriptions, categories, debt, investments, setup, and financial checkups. Read the [connector reference](docs/connector.md) for tool permissions, approval boundaries, troubleshooting, and disconnection.

Maintainers can find publication procedures and evidence in the [directory guide](integrations/directories/README.md), and repository checks in [CONTRIBUTING.md](CONTRIBUTING.md).

## Preview integrations

[<img src="assets/clients/zapier.ico" alt="" width="24" height="24" align="absmiddle"> Zapier private preview](integrations/zapier/README.md) — **Private; not yet approved for public listing.** The guide covers MCP and API-token setup, account-access requirements, and historical test evidence. Successful tests do not establish public approval.

The following directory routes also remain unavailable or unverified in the recorded evidence. These statuses concern publication and destination-specific tests, not the shared server's availability.

| Destination | Recorded status | Guide |
| --- | --- | --- |
| Smithery | **Private testing only; unpublished.** Limited synthetic reads passed; renewal and a successful valuation comparison remain unverified. | [Smithery status](integrations/directories/README.md#smithery) |
| Glama | **Unsubmitted; connection blocked.** OAuth callback handoff failed; no authenticated tool call completed. | [Glama status](integrations/directories/README.md#glama) |
| PulseMCP | **Listing unverified.** Manual submissions were paused; Registry ingestion was not verified. | [PulseMCP status](integrations/directories/README.md#pulsemcp) |
| ChatGPT directory | **Public approval and listing unverified in this repository.** Preparing a submission ZIP does not establish availability. | [ChatGPT package status](CONTRIBUTING.md#chatgpt-submission-package) |
| Claude connector directory | **Public approval and listing unverified in this repository.** Claude Code plugin tests do not verify this separate destination. | [Directory status](integrations/directories/README.md#chatgpt-and-claude-connector-directories) |

The [official MCP Registry entry](integrations/directories/README.md#official-mcp-registry) was recorded as **published and active** on October 13, 2026. It publishes metadata; it does not certify client compatibility or approval by another directory.

## License and brand assets

This is a public connector distribution, not an open-source license grant. See [LICENSE](LICENSE); the manifests declare `UNLICENSED`. See [Terms of Service, Section 10: Intellectual Property](https://betteroff.finance/legal/terms#intellectual-property) for the terms covering BetterOff names and artwork. For usage questions, [contact BetterOff](https://betteroff.finance/contact).

Client logos identify the documented integrations and remain the property of their respective owners. See [logo sources](#client-logo-sources) for attribution. Their inclusion does not imply endorsement.

### Client logo sources

The repository stores these client assets for attribution. They were retrieved from the official sources below on October 13, 2026. Their inclusion grants no trademark rights. Decorative logos appear beside the client’s written name; they do not replace link text.

Codex uses the OpenAI documentation favicon. Muse Code uses the Meta symbol from its documentation. The other assets use the client mark or site icon.

| Client | Local asset | Official source |
| --- | --- | --- |
| Codex | [codex.png](assets/clients/codex.png) | [Codex source asset](https://developers.openai.com/favicon.png) |
| Claude Code | [claude-code.png](assets/clients/claude-code.png) | [Claude Code source asset](https://assets.claude.com/95a868946ac8a31e5ff832e2899f294aa368b836.png?w=128&h=128) |
| GitHub Copilot | [github-copilot.svg](assets/clients/github-copilot.svg) | [GitHub Copilot source asset](https://raw.githubusercontent.com/primer/octicons/main/icons/copilot-24.svg) |
| Cursor | [cursor.svg](assets/clients/cursor.svg) | [Cursor source asset](https://cursor.com/marketing-static/favicon-light.svg) |
| Gemini CLI | [gemini-cli.png](assets/clients/gemini-cli.png) | [Gemini CLI source asset](https://geminicli.com/icon.png) |
| Devin | [devin.svg](assets/clients/devin.svg) | [Devin source asset](https://devin.ai/favicon.svg) |
| Hermes Agent | [hermes-agent.png](assets/clients/hermes-agent.png) | [Hermes Agent source asset](https://hermes-agent.nousresearch.com/marketing-static/assets/hermes-agent/icon.png) |
| OpenClaw | [openclaw.svg](assets/clients/openclaw.svg) | [OpenClaw source asset](https://openclaw.ai/favicon.svg) |
| Pi | [pi.svg](assets/clients/pi.svg) | [Pi source asset](https://pi.dev/favicon.svg) |
| Muse Code | [muse-code.svg](assets/clients/muse-code.svg) | [Muse Code source asset](https://dev.meta.ai/docs/muse-code) |
| Grok | [grok.png](assets/clients/grok.png) | [Grok icon](https://grok.com/images/android-chrome-192x192.png) |
| Zapier | [zapier.ico](assets/clients/zapier.ico) | [Zapier favicon](https://zapier.com/favicon.ico) |

The GitHub Copilot and Devin SVGs add a theme-aware fill for contrast on light and dark backgrounds. The Meta symbol is extracted from the documentation page with an SVG namespace added for standalone rendering. Other assets are stored as downloaded.

GitHub Copilot uses the [Primer Octicons](https://github.com/primer/octicons) mark, distributed under the [MIT license](https://github.com/primer/octicons/blob/main/LICENSE). See the accompanying [license copy](assets/clients/octicons-LICENSE).
