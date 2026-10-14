<img src="../../assets/clients/zapier.ico" alt="" width="40" height="40" align="absmiddle">

# BetterOff Zapier private preview

[Preview integrations](../../README.md#preview-integrations) · [Connector reference](../../docs/connector.md) · [Directory guide](../directories/README.md)

**Private preview — not yet approved for public listing.**

This guide contains setup instructions and historical test evidence for BetterOff's private Zapier integration. The October 13, 2026 record describes integration `247763`, version `1.0.0`, with two read-only actions. On October 13, 2026, its Publishing page showed **Getting Ready for Review** and a disabled **Submit for review** button. All five saved record links were verified under the original creator account.

## Open Zapier

Sign in with the original creator account, which is listed as an integration Admin. Both test drafts belong to that account’s personal workspace. The company-domain Admin invitation was still pending at this check. Use these current navigation links:

- [Zapier Developer Platform](https://developer.zapier.com/): open the BetterOff integration from **My integrations**. Integration `247763`, version `1.0.0`, is accessible to its Admin account.
- [Zapier Zaps](https://zapier.com/app/assets/zaps): search by the Zap name or ID recorded below.
- [Zap history](https://zapier.com/app/history): find runs under the owning account. A run may be unavailable because of permissions, retention limits, or a different account.

The original record URLs below are valid with the creator account. The earlier 404 and missing-access pages occurred under a different signed-in account; no URL replacement was needed.

## Historical evidence — October 13, 2026

The following results were recorded during earlier testing; they were not rerun during this link review. Authentication and both actions passed synthetic production reads. The first test API token was revoked, and a fresh Zapier read failed with the expected reconnect message. The disconnect fix was subsequently deployed, and the original OAuth grant showed **Disconnected** after a fresh page load.

The separate MCP connection passed synthetic-household tests. BetterOff's **Disconnect** control initially failed twice with error reference `2769416454`; a subsequent Zapier read still succeeded. After deployment of the fix, Disconnect succeeded for **Zapier MCP Integration**, client `UttLaxWefSoLAZMBsJvPdKNHEQMiGFBO`. A fresh production page load confirmed **Disconnected**. Its permissions were limited to `accounts:read` and `networth:read`. With user approval, the saved Zapier MCP connection “BetterOff (0.5.0)” had already been deleted. A fresh request with that original OAuth credential could therefore not be replayed from Zapier.

Authenticated link check on October 13, 2026: all five original links opened under the creator account. The [private integration actions](https://developer.zapier.com/app/247763/version/1.0.0/actions) page showed **Get Financial Overview** and **Get Net Worth History**. Both draft pages and both successful run records were accessible. These checks verify access to saved records; they do not rerun the actions or establish public approval. The private GitHub commit and failed Vercel deployment links were also verified with authenticated access.

### Recorded test results

The [historical MCP test Zap (sign-in required)](https://zapier.com/editor/383433019/draft/383433020/sample) was an unpublished draft at the time of testing. The page still shows the saved successful sample, but it also reports **Authentication not found** after the test connection was deleted. These are historical editor step tests, not a currently working connection.

| MCP check | Result | BetterOff request ID |
| --- | --- | --- |
| OAuth connection | Connected to BetterOff 0.5.0; Zapier labels it Read-Only | Not applicable |
| Scoped discovery | Five read tools; no transfers or writes | Not captured |
| Financial overview | Success; synthetic net worth USD 1,200.75; valuation covers three accounts; current coverage contains four | `087ebaea455a` |
| Net worth history, `30d` | Success; zero points and partial quality because fixture snapshots are older | `87b2a2a477ac` |
| Net worth history, `all` | Success; two snapshots; USD 1,000.25 to USD 1,200.75; change USD 200.50 | `7ade0c5dd23c` |
| Setup status | Success; four accounts, one needs action; complimentary access | `e2fbbe4db7cc` |
| Read after failed disconnect | Still succeeds; revocation did not take effect | `3fe98254b3bd` |

The discovered tools were `betteroff_get_overview`, `betteroff_get_setup_status`, `betteroff_list_accounts`, `betteroff_get_net_worth_history`, and `betteroff_explain_net_worth_change`. Only the first, second, and fourth were called. The two other discovered tools are excluded from the listing draft.

The saved draft includes a required password field for the API token, an authentication test, fixed read endpoints, history period choices, typed output definitions, and samples derived from the synthetic MCP responses. The overview sample uses selected observed fields.

With approval, a 30-day token named **Zapier synthetic read-only validation** was created for **BetterOff Review Owner**, limited to `accounts:read` and `networth:read`. Zapier saved it in **BetterOff read-only: BetterOff's Household Account**. Authentication, overview, and history (`all`) each returned **Request Successful** in Developer Platform.

Both actions also passed editor step tests in [historical validation Zap 383440977 (sign-in required)](https://zapier.com/editor/383440977/draft/383440978/sample). History returned two snapshots and USD 200.50 change, request `38adb487b705`. Overview returned USD 1,200.75 net worth with the expected coverage warning, request `deaf5f8e02e1`. The three-step Zap was left as an unpublished draft with its switch off: Zapier requires Pro for multi-step Zaps.

After testing, BetterOff showed **Token revoked**. A fresh overview retest in Zapier failed with **Reconnect BetterOff with a valid, unexpired API token** and no output data. Zapier retained the now-invalid saved connection at that check. This API-token result does not establish revocation of the separate OAuth grant.

### Separate two-step live tests

With approval, a replacement 30-day token named **Zapier two-step synthetic validation** was created with the same two read permissions. The existing Zapier connection was reconnected with that token. Authentication passed again. Two separate Zaps used Schedule by Zapier followed by one BetterOff read action. Both saved run records show **Successful**, version `v2`, and one task. The link review displayed `2026-10-13 15:30:05` with a `UTC` time-zone label; the earlier note labeled the time Pacific. The run IDs below identify the records without relying on that conflicting time-zone annotation.

| Zap | Historical run (sign-in required) | BetterOff request ID | Observed result |
| --- | --- | --- | --- |
| BetterOff synthetic overview test (`383441707`) | [Historical overview run](https://zapier.com/app/history/018ac651-7a5b-af39-1a10-2d7f10f090d4?root_id=383441707) | `6b78b3dbb1fc` | USD 1,200.75 net worth; expected synthetic household and coverage warning |
| BetterOff synthetic history test (`383441723`) | [Historical net worth history run](https://zapier.com/app/history/018ac651-d458-af36-0ede-98a7e56c3ab4?root_id=383441723) | `c25abc0c8907` | Two snapshots; USD 1,200.75 current net worth; USD 200.50 change |

Both Zaps were turned off after the successful runs. BetterOff then confirmed that the replacement token was revoked. A fresh Zapier overview retest failed with **Reconnect BetterOff with a valid, unexpired API token** and no output data. No transfer or write permission was granted. Zapier cleared both **Needs a successful task** checks. Turning off the test Zaps restored the live-Zap requirements, so these completed tests do not establish listing readiness.

The source copied from Zapier is saved locally at `.private/zapier-draft/zapier-ui-source.json`. It confirms that the shared request template contains only `source=zapier` in URL parameters and no extra headers. Each operation sends the token in the Authorization header. Editing an authentication field can regenerate Zapier's default credential mappings; inspect the source again after such edits.

### Historical disconnect fix and deployment

Production logs for error reference `2769416454` show that both Disconnect attempts failed with HTTP 415 (`UNSUPPORTED_MEDIA_TYPE`) before revocation. The app's `serverApiFetch` omitted the JSON content-type header when a command had no body. The API's content-type guard rejected the request.

The fix in `betteroff.finance/apps/app/lib/bff/server-api.ts` declares JSON for bodyless POST and DELETE requests while preserving the signed empty body. It does not change ownership, session freshness, scope checks, or API content validation. Four new regression tests and 74 existing targeted tests passed. App TypeScript and focused Biome checks also passed.

Only the fix and its regression-test file were committed and pushed to `main` as [a1ec42289](https://github.com/raintree-technology/betteroff.finance/commit/a1ec42289bced2cca6297c80d7102fe8ad916a14). Its [historical failed deployment](https://vercel.com/raintree-technology/app.betteroff.finance/8BSWVVbzBWv8VCe3KpT66DxzApY6) failed the database migration gate: `0150_investing_vaultsfyi` and `0151_investing_morpho_loans` were missing. CI also failed on unrelated investing formatting and Turbo environment declarations. No migration gate was bypassed and no unrelated migration was applied by this task.

On October 13, the production alias `app.betteroff.finance` resolved to ready deployment `dpl_Gx7c53kM1sy2xX4dEWjW2LcqDmP9`, commit `6002d3002d446ca2d1a6527e06b5c8cb67aaa9b1`. Git ancestry and the deployed commit's source confirm that it includes `a1ec42289` and the JSON header fix. The original Zapier grant changed from active to **Disconnected**, and that state persisted after reloading the production page. The original saved OAuth credential is no longer available for a post-revocation request test.

## Included operations

| Zapier action | BetterOff tool | Required permissions |
| --- | --- | --- |
| Get Financial Overview | `betteroff_get_overview` | `accounts:read`, `networth:read` |
| Get Net Worth History | `betteroff_get_net_worth_history` | `networth:read` |

These are retrieval actions. Zapier’s `create` operation type describes their placement in a Zap, not a financial write. Each snippet fixes its destination and tool name. There is no generic tool runner, transfer operation, correction proposal, feedback submission, or user-supplied URL.

The listing draft uses BetterOff’s public REST tool adapter and API token authentication. This is separate from the OAuth MCP connection test. Create a dedicated token with only `accounts:read` and `networth:read`; the adapter does not inspect a token’s other permissions. Never use a token with write or transfer permissions. Tokens expire, so users must reconnect with a replacement before expiry.

No dependencies are required to generate or test these Platform UI snippets. This is not a CLI upload package or a Platform UI import format.

## Generate and verify

Run from the repository root:

```sh
node --test integrations/zapier/draft.test.cjs
node integrations/zapier/build-draft.cjs
```

The generator writes configuration and Code Mode snippets to `.private/zapier-draft/`. It does not contact Zapier or include credentials. Tests use mocked responses and cannot establish live compatibility.

## Test the MCP connection first

Use a dedicated synthetic BetterOff owner account. Confirm its household identity before granting access. Do not connect a real household for this test.

1. In Zapier Apps, add an MCP Client connection with URL `https://api.betteroff.finance/mcp`, Streamable HTTP transport, and OAuth enabled.
2. Sign in to the synthetic BetterOff account. Select only `accounts:read` and `networth:read` in consent if the client permits scope selection. If it requests broader access that cannot be narrowed, stop and record the limitation.
3. Confirm tool discovery and run `betteroff_get_setup_status`, `betteroff_get_overview`, and `betteroff_get_net_worth_history` with `period: "30d"`.
4. Compare account coverage and net worth with the known synthetic fixture. Preserve incomplete-data warnings. Record the date, tool names, Zap IDs, and successful run IDs without tokens or real financial data.
5. Disconnect the test grant in BetterOff and verify that a new read fails. Reconnect only the synthetic account if a retained test connection is needed.

## Prepare the private integration

1. Create or reuse the BetterOff integration in Developer Platform. Keep it private. Copy the name, description, homepage, and API documentation URL from `platform-ui-draft.json`.
2. Choose API Key authentication and create the required password field `api_token` with the supplied help text. Paste `authentication.js.txt` into the authentication test’s Code Mode. Replace Zapier's generated request template with the supplied credential-free template. Verify the saved source has no token in URL parameters or action input fields.
3. Connect a synthetic account with a dedicated token carrying only the two read permissions above. The authentication test reads the overview, which exercises both permissions.
4. Add the two actions using the generated definitions and Code Mode snippets. For history, use the supplied period choices. Keep the complete response envelope, including currency, `asOf`, quality, warnings, and pagination.
5. Obtain samples from successful synthetic runs. Define output fields from those responses. For overview, expose `data.identity.name`, `data.valuation.netWorth`, and `data.valuation.baseCurrency`; valuation may be null. For history, expose `data.period` and the `data.dataPoints` line items. Also expose envelope currency, freshness, quality, and warnings. Do not claim fabricated samples are live test evidence.
6. Run each action in an enabled test Zap with a harmless destination containing only synthetic data. Retain successful history. Test expired/revoked access and missing permissions without weakening authorization.
7. Run Zapier validation. Record every unresolved error and publishing task. Submit only after all requirements are met and submission is authorized. The user has authorized submission, but the requirements below remain unresolved.

## Listing materials and remaining work

At the end of testing on October 13, 2026, Zapier listed five publishing tasks: the logo, a company-domain user, three users with live Zaps (zero after cleanup), and at least one live Zap for each action. Both successful-task checks have cleared. The last code validation reported zero errors and zero warnings. No readiness attestation or public listing submission was made.

- Name: **BetterOff**.
- Description: **BetterOff is a household finance app for tracking accounts, net worth, spending, investments, and debt.**
- Homepage: <https://betteroff.finance>.
- API documentation: <https://betteroff.finance/developers>.
- Support: <https://betteroff.finance/contact>.
- Logo: the public [BetterOff icon](https://api.betteroff.finance/.well-known/betteroff-icon.png) was downloaded to `.private/zapier-draft/betteroff-icon.png` and verified as a 512 × 512 PNG with an alpha channel. Upload is unfinished: the Chrome file chooser timed out, and native Chrome control was not approved.
- Category selected in Zapier: **Accounting**.
- Add or verify an integration admin with an approved company-domain email. The requested Gmail login alone does not meet this publication requirement.
- Arrange three genuine users with successful live Zaps. Do not create fake users to satisfy this check.
- Provision the required non-expiring reviewer account for `integration-testing@zapier.com`, populated exclusively with synthetic data. An existing reviewer account for another directory is not sufficient evidence.
- Confirm the publicly launched product and documented API meet Zapier’s requirements. BetterOff documents its API as beta; obtain clarification if Zapier considers that a publication blocker.
- Provide user setup documentation and disclose token expiry/reconnection. Record live test evidence and final validation before considering submission.

## Sources

- [Connect remote MCP servers](https://help.zapier.com/hc/en-us/articles/38777069364109-Connect-remote-MCP-servers-to-Zapier-using-MCP-Client)
- [API key authentication](https://docs.zapier.com/integrations/build/apikeyauth)
- [Publication requirements](https://docs.zapier.com/integrations/publish/integration-publishing-requirements)
- [Validation checks](https://docs.zapier.com/integrations/publish/integration-checks-reference)

Historical verification on October 13, 2026: eight focused snippet tests passed; public-file and package audits passed; `git diff --check` passed. Zapier's own validation passed the code and warning checks. API-token authentication, both live read actions, and first-token rejection passed against production. Original OAuth Disconnect persisted in production at that check. A post-revocation request with the original OAuth credential was unavailable because its Zapier connection had already been deleted. Public review and publishing requirements remain unfinished. The disconnect fix and regression tests were pushed; the connector draft was uncommitted at that check.
