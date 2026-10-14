<!-- Generated from tools.json by scripts/tools_catalog.py. Edit tools.json, then run the script. -->
<picture><source media="(prefers-color-scheme: dark)" srcset="../assets/betteroff-mark-white.svg"><img src="../assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff tools

[All clients](../README.md#install-the-connector) · [Connector reference](connector.md)

Version 0.5.0 of `https://api.betteroff.finance/mcp` defines 29 tools: 21 read tools and 8 write tools. A client sees only the tools its granted scopes allow.

- **Read** tools return data and change nothing.
- **Write** tools save a pending correction or transfer request, cancel a pending request, or send feedback. None of them can approve, sign, or execute a change; you do that in BetterOff.
- **Core** tools need a BetterOff Core plan. The other tools are free.

The same catalog is available as [tools.json](../tools.json). With an API token, call any tool at `POST https://api.betteroff.finance/v1/tools/{name}`; see the [developer documentation](https://betteroff.finance/developers) and the [public OpenAPI document](https://api.betteroff.finance/openapi/public.json).

| Tool | Access | Plan | Scopes | Description |
| --- | --- | --- | --- | --- |
| `betteroff_get_overview` | Read | Free | `accounts:read`, `networth:read` | Household valuation, data coverage, identity, and connection health. |
| `betteroff_get_setup_status` | Read | Free | `accounts:read` | Remaining setup steps, billing status, and reconnect links. |
| `betteroff_list_accounts` | Read | Free | `accounts:read` | Accounts with balances and balance observation dates. |
| `betteroff_get_net_worth_history` | Read | Free | `networth:read` | Stored net-worth valuations over a period. |
| `betteroff_explain_net_worth_change` | Read | Free | `networth:read` | Reconciles the change between two stored valuations. |
| `betteroff_search_transactions` | Read | Free | `transactions:read` | Finds transactions and totals a filtered set, including merchant history. |
| `betteroff_analyze_spending` | Read | Free | `transactions:read` | Spending by category or merchant, with an optional period comparison. |
| `betteroff_detect_spending_patterns` | Read | Free | `transactions:read` | Spending habits, trends, and unusual transactions. |
| `betteroff_get_account_flows` | Read | Free | `accounts:read`, `transactions:read` | Gross deposits and withdrawals for specific accounts. |
| `betteroff_get_cash_flow` | Read | Free | `cashflow:read` | Household income, expenses, and savings rate. |
| `betteroff_list_recurring` | Read | Core | `cashflow:read` | Observed recurring bills, subscriptions, and income. |
| `betteroff_get_portfolio` | Read | Free | `investments:read` | Investment positions, allocation, and concentration. |
| `betteroff_get_defi_positions` | Read | Free | `investments:read` | DeFi lending, staking, and liquidity positions with assets and liabilities. |
| `betteroff_get_vault_yields` | Read | Free | `investments:read` | Reported APY of vaults available in Investing; not recommendations. |
| `betteroff_search_markets` | Read | Free | `investments:read` | Public FX rates, Hyperliquid spot and perpetual markets, and prediction markets. |
| `betteroff_list_debts` | Read | Free | `debts:read` | Debt balances, terms, and missing terms. |
| `betteroff_simulate_debt_payoff` | Read | Free | `debts:read` | Arithmetic payoff scenarios; refuses when terms are missing. |
| `betteroff_get_checklist` | Read | Core | `checklist:read` | Financial checklist progress, such as insurance, estate documents, and emergency fund. |
| `betteroff_search_activity` | Read | Free | `activity:read` | Recorded financial record changes and correction proposals. |
| `betteroff_list_observations` | Read | Core | `accounts:read`, `networth:read`, `transactions:read`, `cashflow:read`, `investments:read`, `debts:read` | Stored financial findings and their status. |
| `betteroff_propose_category_change` | Write | Core | `transactions:read`, `corrections:prepare` | Saves a pending category correction for approval in BetterOff. |
| `betteroff_propose_recurring_kind` | Write | Core | `cashflow:read`, `corrections:prepare` | Saves a pending bill-or-subscription classification for approval in BetterOff. |
| `betteroff_propose_debt_details` | Write | Core | `debts:read`, `corrections:prepare` | Saves user-stated debt terms for approval in BetterOff. |
| `betteroff_request_transfer` | Write | Core | `accounts:read`, `transfers:prepare` | Requests a USDC transfer between the household's own wallets; the user signs in BetterOff. |
| `betteroff_request_bank_transfer` | Write | Core | `accounts:read`, `transfers:bank` | Requests a transfer between the user's own linked accounts; the user confirms with a passkey. |
| `betteroff_request_vault_deposit` | Write | Core | `investments:read`, `transfers:vault` | Requests a USDC or USDT vault deposit; the user signs in BetterOff. |
| `betteroff_get_action_request` | Read | Free | `transfers:read` | Status of a transfer or deposit request. |
| `betteroff_cancel_action_request` | Write | Core | `transfers:prepare` | Cancels a pending request before it is signed. |
| `betteroff_submit_feedback` | Write | Free | `feedback:submit` | Sends a user-approved diagnostic report to BetterOff support. |
