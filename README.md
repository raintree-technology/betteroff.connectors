# <picture><source media="(prefers-color-scheme: dark)" srcset="assets/betteroff-mark-white.svg"><img src="assets/betteroff-mark-graphite.svg" alt="" width="48" height="48" align="absmiddle"></picture> BetterOff connectors

Ask Codex, Claude Code, GitHub Copilot, Cursor, Gemini CLI, Devin, Hermes Agent, Muse Code, OpenClaw, or Pi about the financial records you connect to BetterOff. The connector can read approved household data and prepare corrections for your review. With separate permission, it can request USDC transfers between your own wallets, which you approve and sign in BetterOff. It cannot apply a correction, move bank funds, or place a trade.

Installation instructions below describe supported configuration routes. Full lifecycle evidence is recorded in [the compatibility review](COMPATIBILITY.md); several clients still need live verification.

This is a public connector distribution, not an open-source license grant. See [LICENSE](LICENSE); the manifests declare `UNLICENSED`. BetterOff names and artwork remain subject to the [brand usage terms](https://betteroff.finance/brand).

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

```sh
gemini extensions install https://github.com/raintree-technology/betteroff.connectors
```

Restart Gemini CLI. On first use, it opens your browser to sign in to BetterOff and receives the result on a `localhost` callback, so run it on a machine with a browser. If sign-in does not start, run `/mcp auth betteroff`. Gemini CLI approval behavior depends on its policy and trusted-tool settings. The extension includes the BetterOff skills.

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

Add the server to `~/.hermes/config.yaml`. With `trust: untrusted`, Hermes asks you before any tool that is not marked read-only, including the proposal and transfer request tools, runs:

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

When your client prompts you, sign in to BetterOff. Review the household and requested permissions before selecting **Allow access**. The data returned by a tool is shared with the client you connected.

Try asking:

- “Show my household overview and flag missing or out-of-date data.”
- “Compare my spending by category this month with the same days last month.”
- “List my debts and tell me which terms are missing.”

Results can be incomplete when a source is not connected or is out of date. Check available dates and warnings before relying on a result.

## What the connector can do

Version 0.4.0 provides 25 tools:

- **18 reads and analyses** cover setup status, accounts, net worth, cash flow, recurring items, holdings, transactions, spending, debts, checklist progress, observations, and financial activity.
- **Three correction proposals** cover payment categories, recurring items, and debt classifications.
- **Three transfer request tools** request, check, and cancel USDC transfers between wallets your household tracks on Solana or Base. They require separate, opt-in `transfers:prepare` and `transfers:read` permissions. A request never approves, signs, or sends; you approve and sign each one in BetterOff.
- **One feedback tool**, `betteroff_submit_feedback`, sends diagnostic reports you approve. It requires separate, opt-in `feedback:submit` permission. Reports must exclude financial records, conversation history, tool payloads, and credentials.

Existing connections must reconnect to request a new permission. Production availability of version 0.4.0 remains unverified until the server release.

Eight skills ship with the connector. `household-review` covers every tool. Seven workflow skills each handle one task and work on their own: `monthly-review`, `subscription-audit`, `categorize-transactions`, `debt-plan`, `portfolio-check`, `connect-and-setup`, and `financial-checkup`.

## Approval and disconnection

Preparing a proposal changes no financial record. Open its authenticated BetterOff review page to choose the scope and approve any change. The connector cannot approve or apply it for you.

Only an eligible household owner can grant access. Access lasts up to 30 days. You can disconnect sooner in [BetterOff Agent connections](https://app.betteroff.finance/settings/agents).

For the MCP endpoint, data boundaries, and correction flow, read the [connector guide](plugins/betteroff/README.md). To change this repository, read the [contribution guide](CONTRIBUTING.md). For help, [contact BetterOff](https://betteroff.finance/contact).
