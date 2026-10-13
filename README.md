# <picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="48" height="48" align="absmiddle"></picture> BetterOff connectors

Connect your AI client to BetterOff to review household finances, find recurring charges, and prepare corrections for your approval.

**25 tools · 8 skills · 11 client setup guides**

[Choose your client](#install-the-connector) · [What you can do](#what-the-connector-can-do) · [Compatibility](COMPATIBILITY.md) · [Connector guide](plugins/betteroff/README.md)

## Before you start

- **Account:** You need a BetterOff household owner account and a client listed below. Connect a supported account or wallet in BetterOff to ask questions about your finances.
- **Consent:** All household members must consent to AI processing, and you must accept the applicable BetterOff Terms. Data returned by a tool is shared with your connected client.
- **Plan:** Reading data is free. Preparing corrections and transfer requests requires BetterOff Core.
- **Approval:** The connector prepares corrections for your review. With separate permission, it can request USDC transfers between your own wallets. You review each request in BetterOff. Corrections require your approval; transfers require your approval and wallet signature. The connector cannot apply a correction, move bank funds, or place a trade.

## Install the connector

Choose your client to jump to its setup instructions. MCP stands for Model Context Protocol. It lets your AI client call BetterOff tools.

| Client | Setup route | Client | Setup route |
| --- | --- | --- | --- |
| <a href="#codex"><img src="assets/clients/codex.png" alt="" width="24" height="24" align="absmiddle">&nbsp; Codex</a> | Plugin | <a href="#claude-code"><img src="assets/clients/claude-code.png" alt="" width="24" height="24" align="absmiddle">&nbsp; Claude Code</a> | Plugin |
| <a href="#github-copilot"><img src="assets/clients/github-copilot.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; GitHub Copilot</a> | Plugin | <a href="#cursor"><img src="assets/clients/cursor.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; Cursor</a> | Plugin or MCP |
| <a href="#gemini-cli"><img src="assets/clients/gemini-cli.png" alt="" width="24" height="24" align="absmiddle">&nbsp; Gemini CLI</a> | Extension | <a href="#devin"><img src="assets/clients/devin.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; Devin</a> | Personal plugin |
| <a href="#hermes-agent"><img src="assets/clients/hermes-agent.png" alt="" width="24" height="24" align="absmiddle">&nbsp; Hermes Agent</a> | MCP + skills | <a href="#muse-code"><img src="assets/clients/muse-code.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; Muse Code</a> | MCP + skills |
| <a href="#openclaw"><img src="assets/clients/openclaw.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; OpenClaw</a> | MCP + skills | <a href="#pi"><img src="assets/clients/pi.svg" alt="" width="24" height="24" align="absmiddle">&nbsp; Pi</a> | MCP + skills |
| <a href="#grok"><img src="assets/clients/grok.png" alt="" width="24" height="24" align="absmiddle">&nbsp; Grok</a> | Plugin or MCP |  |  |

These are documented configuration routes. Several clients still need live verification; read the [compatibility review](COMPATIBILITY.md) for the evidence and limits.

### Sign in and ask your first question

1. Follow your client's setup instructions below. Run shell commands in a terminal; run slash commands inside the client.
2. When prompted, sign in to BetterOff. Review the household and requested permissions before selecting **Allow access**.
3. Ask: “Show my household overview and flag missing or out-of-date data.”

Results can be incomplete when a source is not connected or is out of date. Check available dates and warnings before relying on a result.

### Codex

```sh
codex plugin marketplace add raintree-technology/betteroff.connectors
codex plugin add betteroff@betteroff
```

### Claude Code

```sh
claude plugin marketplace add raintree-technology/betteroff.connectors
claude plugin install betteroff@betteroff
```

### GitHub Copilot

In VS Code:

1. Run **Chat: Install Plugin From Source** from the Command Palette.
2. Enter `https://github.com/raintree-technology/betteroff.connectors`.
3. Confirm the marketplace trust prompt.
4. Select **Install** for **betteroff**.

In Copilot CLI:

```sh
copilot plugin marketplace add raintree-technology/betteroff.connectors
copilot plugin install betteroff@betteroff
```

In the GitHub Copilot app:

1. Open **Customize** > **Plugins**.
2. Select the gear icon.
3. Add `raintree-technology/betteroff.connectors`.
4. Install **betteroff**.

With default approval settings, VS Code can run tools marked read-only without asking and asks before proposal tools. Copilot CLI normally asks before tool calls; policies and allowlists can change this behavior. To sign in again from Copilot CLI, run `/mcp auth betteroff`.

### Cursor

Copy `plugins/betteroff` from a clone of this repository to `~/.cursor/plugins/local/betteroff`, then reload Cursor. The plugin adds the BetterOff MCP server and the BetterOff skills.

To add only the MCP server, add it to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "betteroff": {
      "url": "https://api.betteroff.finance/mcp"
    }
  }
}
```

Cursor asks before it runs each BetterOff tool unless you add the tool to your allowlist.

### Gemini CLI

Run Gemini CLI on a machine with a browser. Sign-in opens the browser and returns to Gemini CLI through a `localhost` callback.

```sh
gemini extensions install https://github.com/raintree-technology/betteroff.connectors
```

Restart Gemini CLI after installation. If sign-in does not start on first use, run `/mcp auth betteroff`.

The extension includes the BetterOff skills. Tool approvals depend on Gemini CLI policy and trusted-tool settings.

### Devin

> **Warning:** Connect BetterOff with **Personal** access only. With **Organization** access, every member's sessions share one BetterOff sign-in and can read your household finances. Devin notes that other members can still interact with your sessions, so use BetterOff only in an organization whose members you trust with this data.

In the Devin web app:

1. Open **Customize** > **Plugins** and select the **Personal** scope.
2. Choose **Add plugin** > **From repository**. Enter `raintree-technology/betteroff.connectors` and the subdirectory `plugins/betteroff`.
3. After indexing finishes, open **Customize** > **MCPs**, select **betteroff**, and choose **Connect**.
4. Start a new session and mention `/betteroff:household-review` or a workflow skill such as `/betteroff:monthly-review` to load it.

In the Devin CLI:

```sh
devin plugins install raintree-technology/betteroff.connectors#plugins/betteroff
devin mcp login betteroff
```

The Devin CLI asks before each BetterOff tool call unless you allow it.

### Hermes Agent

Add the server to `~/.hermes/config.yaml` with the settings below. `trust: untrusted` makes Hermes ask before running tools that are not marked read-only. This includes correction proposal and transfer request tools:

```yaml
mcp_servers:
  betteroff:
    url: "https://api.betteroff.finance/mcp"
    auth: oauth
    trust: untrusted
    sampling:
      enabled: false
```

Then sign in and install the skills:

```sh
hermes mcp login betteroff
for skill in household-review monthly-review subscription-audit categorize-transactions debt-plan portfolio-check connect-and-setup financial-checkup; do
  hermes skills install "raintree-technology/betteroff.connectors/plugins/betteroff/skills/$skill"
done
```

### Muse Code

Add the server to `~/.config/muse/settings.json`. Keep `"schema_version": 1` and merge the `mcp_servers` block into any existing settings:

```json
{
  "schema_version": 1,
  "mcp_servers": {
    "betteroff": {
      "transport": "streamable_http",
      "url": "https://api.betteroff.finance/mcp",
      "mode": "optional"
    }
  }
}
```

OAuth works through user settings. Muse Code plugin servers and project-only servers do not provide this sign-in route.

Then sign in and install the skills from a clone of this repository:

```sh
muse mcp login betteroff
for skill in plugins/betteroff/skills/*/; do muse skills install "$skill" --scope user; done
```

Do not choose **Always allow** for the proposal tools. Each proposal should get its own approval.

### OpenClaw

Use OpenClaw only in a direct chat with the household owner. By default, OpenClaw shares one BetterOff sign-in with everyone who can message the agent, so anyone in a group chat could read your household finances.

OpenClaw can instead give each sender a separate sign-in: set `oauth.identity` to `"per-requester"` on the server and set `gateway.publicOrigin`, as described in [OpenClaw's MCP transport documentation](https://github.com/openclaw/openclaw/blob/main/docs/cli/mcp/transports.md). This route has not been tested with BetterOff.

```sh
openclaw mcp add betteroff --url https://api.betteroff.finance/mcp --transport streamable-http --auth oauth
openclaw mcp configure betteroff --approval prompt
openclaw mcp login betteroff
openclaw mcp doctor betteroff --probe
```

Then install the skills from a clone of this repository:

```sh
for skill in plugins/betteroff/skills/*/; do openclaw skills install "./$skill" --global; done
```

Sign-in returns to `http://127.0.0.1:8989/oauth/callback`. If the Gateway runs on another machine, finish with `openclaw mcp login betteroff --code <code>`. `--approval prompt` applies only to Gateway-hosted Codex runs; other agent harnesses use their own approval settings. Verify their behavior before sharing access. Nothing changes until you approve the proposal in BetterOff.

### Pi

Requires Pi 0.99.0 or later.

```sh
pi mcp add betteroff --url https://api.betteroff.finance/mcp --exposure direct
pi mcp login betteroff
pi mcp list
```

Then copy the skills from a clone of this repository:

```sh
cp -R plugins/betteroff/skills/* ~/.agents/skills/
```

Run `/reload` in an open Pi session to pick up the server. Pi's built-in tools can run without prompts; permission extensions can change this behavior. The proposal tools only prepare a correction, and nothing changes until you approve it in BetterOff.

### Grok

Grok connects to the same endpoint and signs in with OAuth. Do not add an `Authorization` header or an API key.

In Grok Build, load the plugin from a clone of this repository. It adds the BetterOff MCP server and the skills:

```sh
grok --plugin-dir ./plugins/betteroff
```

To add only the MCP server:

```sh
grok mcp add --transport http betteroff https://api.betteroff.finance/mcp
grok mcp doctor betteroff
```

Sign-in starts on first use. In an open session, run `/mcps` and press `i` to sign in again.

On [grok.com](https://grok.com/connectors):

1. Select **New Connector** > **Custom**.
2. Name the connector `BetterOff`.
3. Enter `https://api.betteroff.finance/mcp` as the server URL. Leave the headers empty.

In Grok Bot:

1. Send “Add a custom MCP server called betteroff at https://api.betteroff.finance/mcp”.
2. Check that the proposed URL matches `https://api.betteroff.finance/mcp`.
3. Select **Add it**.
4. Select **Authorize** on the card Grok Bot posts.

If Grok marks the connector as connected without opening a BetterOff sign-in page, remove it and add it again. Each proposal still needs your approval in BetterOff.

## What the connector can do

Version 0.4.0 provides 25 tools:

- **18 reads and analyses** cover setup status, accounts, net worth, cash flow, recurring items, holdings, transactions, spending, debts, checklist progress, observations, and financial activity.
- **Three correction proposals** cover payment categories, recurring items, and debt classifications.
- **Three transfer request tools** request, check, and cancel USDC transfers between wallets your household tracks on Solana or Base. They require separate, opt-in `transfers:prepare` and `transfers:read` permissions. A request never approves, signs, or sends; you approve and sign each one in BetterOff.
- **One feedback tool**, `betteroff_submit_feedback`, sends diagnostic reports you approve. It requires separate, opt-in `feedback:submit` permission. Reports must exclude financial records, conversation history, tool payloads, and credentials.

If you already connected BetterOff, reconnect to request a new permission.

### Choose a workflow

Skills give your AI client instructions for specific tasks. Each skill works on its own. Start with `household-review` for a broad review, or choose a focused workflow.

| Skill | Example request |
| --- | --- |
| [`household-review`](plugins/betteroff/skills/household-review/SKILL.md) | “Show my household overview and flag missing or out-of-date data.” |
| [`monthly-review`](plugins/betteroff/skills/monthly-review/SKILL.md) | “Review my spending and cash flow for the last complete month.” |
| [`subscription-audit`](plugins/betteroff/skills/subscription-audit/SKILL.md) | “Review my recurring charges and identify bills and subscriptions.” |
| [`categorize-transactions`](plugins/betteroff/skills/categorize-transactions/SKILL.md) | “Find payments that may be miscategorized and prepare corrections for review.” |
| [`debt-plan`](plugins/betteroff/skills/debt-plan/SKILL.md) | “Compare debt payoff strategies and flag missing terms.” |
| [`portfolio-check`](plugins/betteroff/skills/portfolio-check/SKILL.md) | “Summarize my investment allocation and concentration.” |
| [`connect-and-setup`](plugins/betteroff/skills/connect-and-setup/SKILL.md) | “Check my connections and show the remaining setup steps.” |
| [`financial-checkup`](plugins/betteroff/skills/financial-checkup/SKILL.md) | “Review my financial checklist and suggest the next items to complete.” |

## Approval and disconnection

Preparing a proposal changes no financial record. Open its authenticated BetterOff review page to choose the scope and approve any change. The connector cannot approve or apply it for you.

Only an eligible household owner can grant access. Access lasts up to 30 days. You can disconnect sooner in [BetterOff Agent connections](https://app.betteroff.finance/settings/agents).

For the MCP endpoint, data boundaries, and correction flow, read the [connector guide](plugins/betteroff/README.md). To change this repository, read the [contribution guide](CONTRIBUTING.md). For help, [contact BetterOff](https://betteroff.finance/contact).

## License and brand assets

This is a public connector distribution, not an open-source license grant. See [LICENSE](LICENSE); the manifests declare `UNLICENSED`. BetterOff names and artwork remain subject to the [brand usage terms](https://betteroff.finance/brand).

Client logos identify the documented integrations and remain the property of their respective owners. See [logo sources](assets/clients/README.md) for attribution. Their inclusion does not imply endorsement.
