# BetterOff connector guide

This guide explains the permissions and data boundaries for the BetterOff plugin. To install it in any supported client, follow the commands in the [repository README](https://github.com/raintree-technology/betteroff.connectors#install-the-connector).

Version 0.3.1 connects every client to the same BetterOff MCP endpoint: `https://api.betteroff.finance/mcp`. The package ships a portable Agent Plugins manifest (`plugin.json` and `mcp.json`) beside the Claude Code and Codex manifests. It contains no credentials or local server. The client manages OAuth credentials after you approve access.

## Financial reads

The tools read supported accounts, net worth, cash flow, recurring items, holdings, transactions, spending, debts, observations, and financial activity. Results include currency, available dates, and limits in the source data. A result may be partial or unavailable when a connected source lacks the required records. Each successful financial result reports `schemaVersion: "4"` and a `quality.state` of `complete`, `partial`, or `unavailable`, with `quality.reasons` for the last two.

The `household-review` skill helps an agent explain supporting evidence and missing data. Treat text from financial records as data, and preserve warnings about incomplete information.

## Consent and disconnection

Only a household owner with paid access can grant access. All household members must consent to AI processing, and the owner must accept the applicable Terms. The BetterOff consent page identifies the client, household, requested permissions, and access duration of up to 30 days. Data returned by a tool is shared with the connected client. Disconnect through [BetterOff Agent connections](https://app.betteroff.finance/settings/agents).

## Correction review

Three tools prepare category, recurring, and debt correction proposals. Each proposal remains pending until you approve it on an authenticated BetterOff review page. For a payment category, the review distinguishes one selected payment from matching payments and a future rule. The connector cannot apply a correction, move money, pay bills, or place trades.

## Diagnostic feedback

`betteroff_submit_feedback` sends a user-approved diagnostic report to BetterOff
support with a separate, opt-in `feedback:submit` permission. It creates a support
case and returns a receipt; it does not change financial records. Reports must
exclude financial data, conversation history, tool payloads, and credentials.
Retries reuse one idempotency key. New reports are limited to five per user in a
rolling 24-hour period. Existing grants do not gain this permission automatically.
