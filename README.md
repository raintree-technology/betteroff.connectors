# <picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="48" height="48" align="absmiddle"></picture> BetterOff connectors

Ask Codex, Claude Code, GitHub Copilot, Cursor, Gemini CLI, Devin, Hermes Agent, Muse Code, OpenClaw, or Pi about the financial records you connect to BetterOff. The connector can read approved household data and prepare corrections for your review. It cannot apply a correction, move money, or place a trade.

Installation instructions below describe supported configuration routes. Full lifecycle evidence is recorded in [the compatibility review](COMPATIBILITY.md); several clients still need live verification.

## Before you start

You need a BetterOff household owner account with paid access and one of those clients. All household members must consent to AI processing, and you must accept the applicable BetterOff Terms. Connect at least one supported account or wallet in BetterOff to ask questions about your finances.

## Install the connector

Run the commands for your client in a terminal.

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

In VS Code, run **Chat: Install Plugin From Source** from the Command Palette, enter `https://github.com/raintree-technology/betteroff.connectors`, confirm the marketplace trust prompt, and select **Install** for **betteroff**.

In Copilot CLI:

```sh
copilot plugin marketplace add raintree-technology/betteroff.connectors
copilot plugin install betteroff@betteroff
```

In the GitHub Copilot app, open **Customize** > **Plugins**, select the gear icon, add `raintree-technology/betteroff.connectors`, and install **betteroff**.

With default approval settings, VS Code can run tools marked read-only without asking and asks before proposal tools. Copilot CLI normally asks before tool calls; policies and allowlists can change this behavior. To sign in again from Copilot CLI, run `/mcp auth betteroff`.

### Cursor

Copy `plugins/betteroff` from a clone of this repository to `~/.cursor/plugins/local/betteroff`, then reload Cursor. The plugin adds the BetterOff MCP server and the `household-review` skill.

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

```sh
gemini extensions install https://github.com/raintree-technology/betteroff.connectors
```

Restart Gemini CLI. On first use, it opens your browser to sign in to BetterOff and receives the result on a `localhost` callback, so run it on a machine with a browser. If sign-in does not start, run `/mcp auth betteroff`. Gemini CLI approval behavior depends on its policy and trusted-tool settings. The extension includes the native `household-review` skill.

### Devin

> **Warning:** Connect BetterOff with **Personal** access only. With **Organization** access, every member's sessions share one BetterOff sign-in and can read your household finances. Devin notes that other members can still interact with your sessions, so use BetterOff only in an organization whose members you trust with this data.

In the Devin web app:

1. Open **Customize** > **Plugins** and select the **Personal** scope.
2. Choose **Add plugin** > **From repository**. Enter `raintree-technology/betteroff.connectors` and the subdirectory `plugins/betteroff`.
3. After indexing finishes, open **Customize** > **MCPs**, select **betteroff**, and choose **Connect**.
4. Start a new session and mention `/betteroff:household-review` to load the skill.

In the Devin CLI:

```sh
devin plugins install raintree-technology/betteroff.connectors#plugins/betteroff
devin mcp login betteroff
```

The Devin CLI asks before each BetterOff tool call unless you allow it.

### Hermes Agent

Add the server to `~/.hermes/config.yaml`. With `trust: untrusted`, Hermes asks you before any tool that is not marked read-only, including the three proposal tools, runs:

```yaml
mcp_servers:
  betteroff:
    url: "https://api.betteroff.finance/mcp"
    auth: oauth
    trust: untrusted
    sampling:
      enabled: false
```

Then sign in and install the skill:

```sh
hermes mcp login betteroff
hermes skills install raintree-technology/betteroff.connectors/plugins/betteroff/skills/household-review
```

### Muse Code

Add the server to `~/.config/muse/settings.json`. Keep `"schema_version": 1` and merge the `mcpServers` block into any existing settings:

```json
{
  "schema_version": 1,
  "mcpServers": {
    "betteroff": {
      "type": "streamable-http",
      "url": "https://api.betteroff.finance/mcp",
      "required": false
    }
  }
}
```

OAuth works through user settings. Muse Code plugin servers and project-only servers do not provide this sign-in route.

Then sign in and install the skill from a clone of this repository:

```sh
muse mcp login betteroff
muse skills install ./plugins/betteroff/skills/household-review --scope user
```

Do not choose **Always allow** for the proposal tools. Each proposal should get its own approval.

### OpenClaw

Use OpenClaw only in a direct chat with the household owner. By default, OpenClaw shares one BetterOff sign-in with everyone who can message the agent, so anyone in a group chat could read your household finances.

```sh
openclaw mcp add betteroff --url https://api.betteroff.finance/mcp --transport streamable-http --auth oauth
openclaw mcp configure betteroff --approval prompt
openclaw mcp login betteroff
openclaw mcp doctor betteroff --probe
```

Then install the skill from a clone of this repository:

```sh
openclaw skills install ./plugins/betteroff/skills/household-review --global
```

Sign-in returns to `http://127.0.0.1:8989/oauth/callback`. If the Gateway runs on another machine, finish with `openclaw mcp login betteroff --code <code>`. Approval prompts depend on the Gateway and agent harness. Verify their behavior before sharing access. Nothing changes until you approve the proposal in BetterOff.

### Pi

Requires Pi 0.99.0 or later.

```sh
pi mcp add betteroff --url https://api.betteroff.finance/mcp --exposure direct
pi mcp login betteroff
pi mcp list
```

Then copy the skill from a clone of this repository:

```sh
cp -R plugins/betteroff/skills/household-review ~/.agents/skills/
```

Run `/reload` in an open Pi session to pick up the server. Pi's built-in tools can run without prompts; permission extensions can change this behavior. The proposal tools only prepare a correction, and nothing changes until you approve it in BetterOff.

When your client prompts you, sign in to BetterOff. Review the household and requested permissions before selecting **Allow access**. The data returned by a tool is shared with the client you connected.

Try asking:

- “Show my household overview and flag missing or out-of-date data.”
- “Compare my spending by category this month with the same days last month.”
- “List my debts and tell me which terms are missing.”

Results can be incomplete when a source is not connected or is out of date. Check available dates and warnings before relying on a result.

## What the connector can do

Version 0.3.0 provides 20 tools:

- **17 reads and analyses** cover setup status, accounts, net worth, cash flow, recurring items, holdings, transactions, spending, debts, observations, and financial activity.
- **Three correction proposals** cover payment categories, recurring items, and debt classifications.

## Approval and disconnection

Preparing a proposal changes no financial record. Open its authenticated BetterOff review page to choose the scope and approve any change. The connector cannot approve or apply it for you.

Only an eligible household owner can grant access. Access lasts up to 30 days. You can disconnect sooner in [BetterOff Agent connections](https://app.betteroff.finance/settings/agents).

For the MCP endpoint, data boundaries, and correction flow, read the [connector guide](plugins/betteroff/README.md). For help, [contact BetterOff](https://betteroff.finance/contact).
