<picture><source media="(prefers-color-scheme: dark)" srcset="../../assets/betteroff-mark-white.svg"><img src="../../assets/betteroff-mark-graphite.svg" alt="" width="40" height="40"></picture>

# BetterOff MCP directory guide

[All clients](../../README.md#install-the-connector) · [Contributing](../../CONTRIBUTING.md) · [Zapier private preview](../zapier/README.md)

**BetterOff 0.5.0 is published in the official MCP Registry** as `finance.betteroff/mcp`, with explicit user approval on October 13, 2026. Publication contains metadata only and creates no household-data grant. Smithery is also published after synthetic acceptance testing. Glama and PulseMCP remain unsubmitted. The recorded publication required no application deployment, commit, or push.

Status and evidence recorded October 13, 2026. This guide owns directory submission fields, acceptance procedures, and publication status. See the [contributor guide](../../CONTRIBUTING.md) for repository maintenance and the [Zapier private preview guide](../zapier/README.md) for that integration. Historical checks below have not been rerun as part of documentation consolidation.

## ChatGPT and Claude connector directories

**Public approval and listing unverified in this repository.** The recorded evidence does not establish an approved public listing in either directory. Do not infer approval from package preparation, a private test, or installation from this repository.

ChatGPT has a separate [submission package procedure](../../CONTRIBUTING.md#chatgpt-submission-package). Claude Code uses a repository plugin; its recorded authenticated checks do not verify the Claude connector directory. Confirm each destination's review decision and public listing before changing this status.

## Prepared materials

| Destination | Material | Readiness |
| --- | --- | --- |
| Official MCP Registry | [Payload](server.json) and [publication notes](#official-mcp-registry) | Published and verified active; exact payload matches the Registry response |
| Smithery | [Submission fields and test requirements](#smithery) | Published; synthetic OAuth, five scoped tools, valuation comparison, and disconnect passed |
| Glama | [Connector submission fields](#glama) | Draft ready; OAuth callback handoff, ownership, and authenticated health check remain |
| PulseMCP | [Editorial submission fields](#pulsemcp) | Manual submissions paused; Registry entry published, downstream ingestion unverified |

[Shared listing copy](#shared-listing-copy) supplies descriptions, links, pricing qualifications, authentication, and examples.

## Release holds

These client acceptance holds apply to Smithery and Glama. They do not block the separate Registry metadata entry; the Registry entry is now published after DNS ownership verification and user authorization.

1. **Smithery limited-scope acceptance passed and the listing is published.** All five tools passed using existing synthetic history. Test and publication-scan grants were disconnected. Refresh remains untested because `offline_access` was excluded. See [publication evidence](smithery-publication-2026-10-13.json).
2. **Resolve Glama's OAuth callback handoff.** Chrome reaches consent and the callback page, but the inspector does not receive the authorization code. Glama relies on the popup's opener, which BetterOff's opener-isolation policy severs. See the [unsent reproduction and proposed client fix](#glama-oauth-callback-handoff-reproduction). The synthetic Glama grant is disconnected. No real household was connected, and no tool call completed through Glama.
3. **Finish destination acceptance tests.** Glama still needs authenticated discovery, synthetic reads, renewal, and revocation tests through its client. Smithery renewal was deliberately not tested because only two read scopes were approved, without `offline_access`. The independent production lifecycle test below establishes server behavior, not either destination's readiness.

## Production lifecycle verified

The production app deployment for commit `55af7c0663e80879e1ee39c8af5e024f1d4d9b8b` reached READY. Git ancestry confirms it includes disconnect fix `a1ec42289`. No deployment was triggered by this task.

An isolated HTTP client signed in as the existing synthetic reviewer, verified the session identity, and completed normal PKCE authorization. It received only `accounts:read`, `networth:read`, and `offline_access`. Initialization reported 0.5.0; discovery exposed five read-only tools. Reads and token refresh passed before disconnection. The test submitted the production Agent connections disconnect form, which calls the same server action as the button. It then confirmed read refusal with HTTP 403 and refresh refusal with HTTP 400 `invalid_grant`. See the [sanitized results](production-lifecycle-2026-10-13.json).

The separate Glama test grant was also disconnected through the production UI. Its last-use field remained Never. Connector manifests and both skill copies now match source version 0.5.0 and its 29-tool catalog; a limited production grant correctly exposes fewer tools. The ChatGPT package continues to exclude all five transfer tools.

## Recorded verification evidence

| Check | Result and limitation |
| --- | --- |
| Existing `scripts/audit_server.sh` | Passed: unauthenticated 401, invalid-token rejection, query-token rejection, protected-resource identity, issuer discovery, PKCE S256, public RS256 key, registration support, issuer response parameter, HTTPS redirect, HSTS, and CORS checks |
| Live OAuth metadata | Advertises both `registration_endpoint` and `client_id_metadata_document_supported: true` |
| Public resource metadata | Resource is `https://api.betteroff.finance/mcp`; includes read, correction, feedback, and transfer scopes |
| Public listing URLs | User/developer documentation, privacy, terms, support, and GitHub connector repository returned HTTP 200 |
| Public icon | HTTP 200, `image/png`; existing repository notes identify the icon as 512 × 512 |
| Optional Smithery static card | HTTP 401; no public card established |
| MCP transport, branding, transfer-publication tests | 18 passed, 0 failed, 247 assertions. Tests use local fixtures/mocks. Warning logs report missing database/signing configuration in exercised error paths; this run does not validate production database-backed tool execution |
| OAuth tests | 8 passed, 0 failed, 238 assertions, using local in-memory fixtures. Includes refusal of code exchange and refresh after read access ends; production disconnect was verified separately in the lifecycle evidence above |
| Production tool calls and token lifecycle | Passed against the dedicated synthetic reviewer only; see the lifecycle results above. No real household financial data was fetched |
| Official Registry duplicate search | Follow-up succeeded: existing `finance.betteroff/public` 1.0.0 points to the old anonymous endpoint. Before publication, exact lookup of `finance.betteroff/mcp` returned 404. After publication, the new record is active and the existing record remains unchanged |
| PulseMCP live form | Browser inspection confirmed manual submissions and listing changes are paused |
| Registry JSON schema | Passed offline validation with `jsonschema` against the official 2025-12-11 schema, including format checks. Description is 98 characters. Ownership and Registry acceptance were verified separately during publication |
| Registry live validation | Passed with `valid: true` and no issues; DNS ownership proof saved and publisher login succeeded. Publication returned success, and the public record matches the payload. See [publication evidence](registry-publication-2026-10-13.json) |
| Draft file checks | Public-content audit, package audit, local Markdown link checks, and trailing-whitespace checks passed. `git diff --check` passed for tracked changes; the new drafts were also checked directly because they are untracked |

The initial application inspection used commit `34366f91d56d2ec7bda91a21f6326c5f09d74650`. Follow-up checks included the disconnect fix `a1ec42289`, with unrelated existing working-tree edits preserved. Local evidence is not a deployment attestation.

Follow-up validation on October 13:

- BFF request-header regression suite: four passed.
- API-token revocation, OAuth, and MCP transport suites: 24 passed, zero failed, 482 assertions. These checks use local fixtures; they do not establish production revocation.
- Connector audit tests: eight passed. ChatGPT packaging regression test: one passed, including exclusion of all five transfer tools and bank/vault scopes.
- Public-content and package audits, strict Claude marketplace and plugin validation, and `git diff --check`: passed.
- Catalog comparison: both household-review tool tables include all 29 source tools; the source reports version 0.5.0 and 21 read-only tools.

## Synthetic acceptance procedure

Run this separately for Smithery and Glama after resolving their account and callback prerequisites. Production disconnect already passes the independent synthetic test. A Glama submission may immediately publish, so do not create its connector record as a test draft.

1. Use a dedicated synthetic household owner and verify the household identity before granting access.
2. Request `accounts:read` and `networth:read`, the explicit `/mcp` resource audience, and `offline_access` only for refresh testing. Record any client that cannot narrow its scopes.
3. Initialize the connection and record server name, version, and negotiated protocol. List tools and confirm the limited grant exposes no correction, feedback, or transfer tools.
4. Call `betteroff_get_setup_status`, `betteroff_get_overview`, and `betteroff_get_net_worth_history`. Compare values with the synthetic fixture and preserve missing-data warnings. Record request IDs, not tokens or household records.
5. Refresh the connection and repeat a read to confirm renewal.
6. Disconnect in BetterOff. Confirm a new read and a refresh attempt are denied. Removing a connection from the directory client alone is insufficient.
7. Record the destination, date, scopes, version, outcomes, and sanitized request IDs. Keep credentials in private storage. Resolve failures before seeking authorization to submit.

## Verification commands

From the connectors repository, run `scripts/audit_server.sh`, `python3 scripts/audit_public.py`, `python3 scripts/audit_package.py`, and `git diff --check`.

From the application repository, the focused local checks used were:

```sh
bun test apps/api/test/mcp-transport.test.ts apps/api/test/mcp-branding.test.ts apps/api/test/mcp-transfer-publish.test.ts
bun test packages/security/test/agent-oauth.test.ts
```

Provider requirements and field mappings appear below. The official Registry accepted the metadata. This is not a security certification or Smithery/Glama client acceptance. Downstream ingestion has not yet been verified.

The draft Markdown was manually reviewed as plain text. A separate grammar checker and rendered-page review were not run.

## Shared listing copy

Use these fields for directory submissions. The official Registry and Smithery entries are published; Glama and PulseMCP remain unsubmitted in the recorded evidence. Resolve the [release holds](#release-holds) before submitting to Glama; Smithery retains the recorded refresh and vendor-ownership limits.

### Shared fields

| Field | Draft value |
| --- | --- |
| Display name | BetterOff |
| Publisher | FinSync LLC |
| Short description | Review household finances and prepare corrections and transfer requests for approval in BetterOff. |
| Suggested categories | Finance; Personal finance; Productivity. Select only categories the destination actually offers. |
| Homepage | https://betteroff.finance |
| User documentation | https://betteroff.finance/agents |
| Developer documentation | https://betteroff.finance/developers |
| Connector distribution | https://github.com/raintree-technology/betteroff.connectors |
| Support | https://betteroff.finance/contact |
| Privacy policy | https://betteroff.finance/legal/privacy |
| Terms | https://betteroff.finance/legal/terms |
| Icon | https://api.betteroff.finance/.well-known/betteroff-icon.png |
| Remote URL | https://api.betteroff.finance/mcp |
| Transport | Streamable HTTP |
| Authentication | OAuth with authorization code and PKCE S256; per-user household consent |
| API key or fixed header | None for this OAuth connection |
| Server version | 0.5.0 in the recorded production initialization; verify again for a new release |
| License | Proprietary. The connector repository is public but does not grant an open-source license. |

### Full description

BetterOff connects an AI assistant to your household finances. Review accounts, net worth, spending, cash flow, recurring charges, investments, and debt. Ask for a household overview, review a month of spending, or identify recurring subscriptions. Results include dates, source status, and incomplete-data warnings.

An eligible BetterOff household owner signs in and chooses permissions. All household members must consent to AI processing, and the owner must accept the applicable Terms. Financial information returned by tools is shared with the connected client. Most reads are free. Recurring items, checklist progress, observations, correction proposals, and transfer requests require BetterOff Core.

Correction tools prepare changes for approval in BetterOff. Separate transfer permissions can expose tools that prepare wallet transfers, bank transfers, or vault deposits; the user must approve each request in BetterOff and complete the required wallet signature or passkey confirmation. MCP tools cannot approve or execute those requests themselves. A separate, opt-in feedback tool sends user-approved diagnostic reports.

Available tools depend on granted permissions. BetterOff does not provide individualized financial, tax, or legal advice through this connector.

### Example prompts

- Show my household overview and flag missing or out-of-date data.
- Review my spending and cash flow for the last complete month.
- Review recurring charges and identify bills and subscriptions.
- Summarize my investment allocation and concentration.
- Find payments that may be miscategorized and prepare corrections for review.

### Reviewer setup notes

Use a dedicated synthetic household. Start with `accounts:read` and `networth:read`; do not request transfer, correction, or feedback permissions for the initial connection check. Include the resource parameter `https://api.betteroff.finance/mcp` in OAuth authorization and token exchange. Request `offline_access` only if testing refresh.

This is a limited test grant, not a promise that the general endpoint only supports read tools. Do not describe the endpoint as read-only or claim that all its tools have passed live tests.

Keep reviewer credentials outside this public repository. The recorded Glama test used an existing synthetic reviewer; Smithery signup and limited-scope private testing are complete. Neither establishes a completed reviewer setup for another destination. A contact form URL is available; if a submission requires a named contact or email, obtain the approved business contact before completing that field.

## Official MCP Registry

**Published metadata — recorded active on October 13, 2026.** Registry acceptance does not establish approval or working connections in other clients.

BetterOff version 0.5.0 was published as `finance.betteroff/mcp` on October 13, 2026, at 23:14:29 UTC, after explicit user approval. The Registry reports the record as active and latest. Its returned server object exactly matches [server.json](server.json). See [publication evidence](registry-publication-2026-10-13.json).

### Ownership and verification

DNS ownership verification used a new Ed25519 key. The public MCP TXT proof was saved at `betteroff.finance` and verified against authoritative DNS. The private key remains in ignored local storage with restricted permissions; it was not published. Publisher DNS login succeeded.

The official publisher v1.8.1 binary was downloaded to local scratch storage and its SHA-256 checked against the official release checksums. Live nonpublishing validation returned `valid: true` with no issues. The exact-name lookup returned 404 immediately before publication. The publisher then reported success, and a separate public GET confirmed the name, version, endpoint, and active status.

The listing points to `https://api.betteroff.finance/mcp`. Publication includes metadata only. It creates no household-data grant and required no personal BetterOff login or application deployment.

### Existing listing and remaining work

**Historical only — do not use for setup:** `finance.betteroff/public` version 1.0.0 listed `https://betteroff.finance/mcp` and described anonymous public tools. That endpoint returned 404 during preflight and the October 13, 2026 link check. This record preserves the old listing; it is not a working connector URL. Use `https://api.betteroff.finance/mcp` for the authenticated household connector.

Smithery limited-scope acceptance passed; Glama client acceptance remains incomplete. Downstream ingestion has not yet been verified. Registry acceptance does not certify server security or client compatibility. The authorization relay remains a local prototype and is not deployed.

The repository field is omitted because the public connectors repository distributes client configuration and skills, not the hosted server implementation. No npm package, Docker image, or public server source was submitted.

[Preflight evidence](registry-preflight-2026-10-13.json) records the historical state before publication. Sources checked October 13, 2026: [remote-server format](https://modelcontextprotocol.io/registry/remote-servers), [authentication](https://modelcontextprotocol.io/registry/authentication), and the schema URL in `server.json`.

## Smithery

**Published after synthetic acceptance testing on October 13, 2026.** [Open BetterOff on Smithery](https://smithery.ai/servers/b432acfe/betteroff). The release succeeded and discovered five read-only tools. Publication does not grant household access.

| Field | Value |
| --- | --- |
| Server | `b432acfe/betteroff` |
| Owner namespace | Dedicated test-account namespace `b432acfe`; verified vendor ownership is not established |
| Hosting | Existing BetterOff hosting at `https://api.betteroff.finance/mcp` |

Smithery documents Streamable HTTP, OAuth, and automatic client registration using Client ID Metadata Documents (CIMD). BetterOff advertises CIMD and dynamic client registration. Its unauthenticated endpoint returns the required 401 discovery challenge. A later live private test established a successful Smithery connection with the two approved read scopes.

Smithery scans tools after authentication. Use only a synthetic household and review requested permissions before authorizing a future scan. Smithery's gateway proxies upstream traffic; confirm that the intended test and production data handling matches BetterOff's disclosures before enabling it.

The optional static server card at `/.well-known/mcp/server-card.json` currently returns 401. Do not claim it exists. An authenticated scan is the primary preparation path; if a static card is later needed, generate it from the release catalog and verify its schemas. Do not weaken endpoint authentication to make a scan pass.

The user authorized publication after the valuation test passed. The authenticated publication scan used only `accounts:read` and `networth:read`. Its grant was revoked after the release succeeded. Refresh was intentionally excluded from this acceptance scope.

Source checked October 13, 2026: [Smithery publishing requirements](https://smithery.ai/docs/build/publish).

### Acceptance and publication result — October 13, 2026

The dedicated test account completed signup and authorized the CLI. The CLI's older connection endpoint returned 404; the documented `api.smithery.ai/connect` API created private test connections successfully. The listing was subsequently published after the successful valuation retest.

The production app compatibility fix discards only the exact Smithery document's optional `client_uri: https://smithery.ai`. The existing origin checks, protected fetch transport, redirect matching, PKCE, and consent remain in place. The release uses the previous production source plus the three focused fix files. The application deployment reached READY and serves `app.betteroff.finance`.

The live test verified the synthetic owner email, owner ID, and fixture household ID before consent. It approved only `accounts:read` and `networth:read`. Smithery completed OAuth and discovered five tools. Setup status, overview, account listing, and 30-day net-worth history passed. The initial valuation explanation returned `INCOMPLETE_DATA` for dates without two stored valuations. The successful retest used existing synthetic snapshots from August 1 and September 1, 2026. Net worth increased from USD 1,000.25 to USD 1,200.75; the explanation reported a USD 200.50 increase, matching the asset change, with zero liability contribution and zero reconciliation residual. Missing attribution warnings remained intact; the comparison does not establish investment performance. No new history was inserted.

All Smithery test grants, including the publication scanner grant, were disconnected through BetterOff's production settings action. A follow-up settings read confirmed disconnected status and no remaining disconnect forms. A subsequent Smithery overview call returned no data and HTTP 502 `upstream_error`; Smithery masks the upstream refusal, so this does not identify its underlying HTTP status. Refresh was not tested because `offline_access` was excluded. See [final publication evidence](smithery-publication-2026-10-13.json) and [earlier live results](smithery-live-results-2026-10-13.json).

## Glama

**Unsubmitted — authenticated connection blocked.** No public record or completed authenticated tool call is recorded. The relay experiment remains local and undeployed.

Use **Connector** on [Glama's connectors page](https://glama.ai/mcp/connectors). BetterOff is an existing hosted server. The open-source GitHub server route is inappropriate for this proprietary distribution. No Glama record was created.

| Field | Value |
| --- | --- |
| Authentication | OAuth 2.0 badge; authorization code with PKCE S256 |
| Documentation, policies, icon, full description | Copy from [shared listing copy](#shared-listing-copy) |
| Private test credentials | Not supplied; use a synthetic OAuth connection if required |

Glama documents automatic registration for servers supporting OAuth dynamic client registration. BetterOff advertises that registration endpoint, but authenticated Glama discovery and health checks remain incomplete.

Glama states that submitted connectors are public once healthy. Treat **Add MCP Server → Connector** as a potentially publishing operation, not as a private draft save. Keep this draft local until publication is authorized.

Claim ownership with Glama's issued DNS or HTTP challenge after choosing the correct verified domain. Prefer the Registry publisher identity if the official entry already exists. Do not invent a claim token, upload a credential as proof, or assert vendor verification before it succeeds.

Glama's gateway stores complete tool request and response payloads in call logs. Use synthetic data for evaluation. Document this data path before making a gateway-based connection available to households. A directory record and an actual gateway connection have different effects.

Source checked October 13, 2026: [Glama submission, ownership, and gateway documentation](https://glama.ai/mcp/faq).

### Inspector result — October 13, 2026

Chrome opened the OAuth consent popup that did not appear in the in-app browser. The session was explicitly signed in as the existing synthetic BetterOff reviewer. With user confirmation, consent granted only `accounts:read` and `networth:read`; all other scopes were unchecked.

The callback displayed **Authentication Successful**, but the inspector remained at **OAuth Required**. A fresh flow reproduced the problem. That callback message confirms receipt of an authorization code, not a successful token exchange. The [reproduction report](#glama-oauth-callback-handoff-reproduction) traces the handoff failure to Glama's dependence on the popup opener and BetterOff's opener-isolation header.

No tool call, token refresh, or successful authenticated discovery completed through Glama. The synthetic grant was disconnected in BetterOff; the production UI confirms **Disconnected** and **Last used: Never**. The inspector's proxy setting was restored to its default. No public Connector listing was created.

An independent synthetic HTTP client passed production initialization, scoped discovery, read, refresh, and disconnect checks. Those results establish server lifecycle behavior but do not substitute for a successful Glama client test.

### Glama OAuth callback handoff reproduction

Glama's hosted inspector reaches BetterOff consent but cannot complete its popup handoff. This report is prepared for a maintainer; it has not been sent or submitted. Tests on October 13, 2026 used only a synthetic BetterOff household.

#### Reproduction

1. Open [Glama's inspector](https://glama.ai/mcp/inspector) in Chrome. Add `https://api.betteroff.finance/mcp`, select OAuth 2.0, and keep the default proxy enabled.
2. Connect and choose **Authenticate**. The popup reaches BetterOff's consent page through dynamic client registration and PKCE.
3. Sign in as a dedicated synthetic reviewer. Keep only account and net-worth read permissions, then approve consent.
4. Observe the callback page at `/mcp/inspector/oauth/callback`: **Authentication Successful**, followed by **You can now close this window and return to the inspector.**
5. Return to the inspector. It remains at **OAuth Required**; no tools are discovered. A fresh popup flow reproduces the failure.

The first in-app-browser attempt did not expose the popup at all. Chrome resolves that first symptom but still fails at callback handoff.

#### Evidence and diagnosis

BetterOff's production app sends `Cross-Origin-Opener-Policy: same-origin-allow-popups`. This permits popups opened by BetterOff but isolates BetterOff when another origin opens it. [Chrome's explanation](https://developer.chrome.com/blog/coop-restrict-properties/) describes that distinction.

Glama's publicly served [popup helper](https://glama.ai/client/openPopup-sJ9GPUSH.js) opens the authorization URL with `window.open`. Its [callback module](https://glama.ai/client/_route-C__JfHfW.js) sends the code only when an opener exists and remains open. The exact callback message observed above is the branch used when no available opener is found. The [inspector module](https://glama.ai/client/_route-OGXrCaEH.js) waits for the callback message before exchanging the code.

Together, the live headers, callback branch, and repeated browser result identify the broken handoff. They do not establish that the token endpoint rejected a request: no successful inspector token exchange was observed. Asset filenames are deployment-specific evidence and may change.

#### Proposed client fix

Glama can complete the handoff through a same-origin channel between its callback and inspector, without depending on a cross-origin opener. A BroadcastChannel-based implementation should bind each response to a cryptographically random, single-use OAuth state, validate the expected server and pending flow, expire abandoned flows, and retain PKCE. A full-page authorization flow with validated state and preserved verifier is another option. Do not show success until the inspector acknowledges the callback and token exchange succeeds.

This is a proposed fix to Glama's client, not an implemented or verified patch. This repository does not contain that client. BetterOff's opener isolation, authorization checks, and CORS policy were not relaxed.

#### Cleanup and remaining verification

The synthetic Glama grant was revoked through BetterOff's production Disconnect control. The UI reports **Disconnected** and **Last used: Never**. No real account or financial data was shared.

After a client fix, rerun discovery, synthetic reads, refresh, and server-side disconnect. Confirm reads and refresh fail after revocation. The independent [production lifecycle result](production-lifecycle-2026-10-13.json) already verifies that behavior for a separate synthetic HTTP test client.

#### BetterOff-side options reviewed — October 13, 2026

No small, verified BetterOff-side fix preserves the current security boundary. Source review confirmed that `apps/app/proxy.ts` applies opener isolation to the app, including sign-in and consent. The consent page verifies the signed OAuth request and requires an authenticated household owner. Changing token exchange, scopes, or CORS would not restore Glama's lost popup reference.

| Option | Assessment |
| --- | --- |
| Remove COOP or use `unsafe-none` on consent/sign-in | Reject: exposes those authenticated documents to cross-origin opener interactions that the existing policy blocks. A route exception still reduces protection. |
| Allow an exception based on client name, redirect URL, or referrer | Reject: those values do not establish a trusted opener. Dynamic client names are self-asserted. |
| Replace COOP with `restrict-properties` | Not safe to ship as a cross-browser fix. Chrome's documentation describes an origin trial; the current HTML standard and MDN compatibility data do not establish interoperable support. An unrecognized value leaves the default `unsafe-none` policy. |
| Send a message or use BroadcastChannel from BetterOff | Insufficient: the opener is already severed, and BetterOff cannot use a same-origin channel belonging to Glama. Glama must receive the response through a channel it implements. |
| Build a separate authorization relay origin | Possible architecture to investigate, not a verified fix. It requires a separate popup that retains Glama's opener while authentication runs in an isolated window, plus a secure server-mediated handoff. This adds an authentication surface and needs design and browser testing. It is not justified as a small compatibility patch. |

A relay would need to avoid ambient app credentials, bind each one-time handoff to the exact validated client, redirect URI, OAuth request, and approved household, retain PKCE and consent checks, expire abandoned requests, and prevent replay. It must return only the authorization response to the registered callback. These are design requirements, not evidence that such a relay is implemented or safe.

The recommended fix remains Glama's callback channel. No application code, security headers, grants, or deployment changed during this follow-up review. No new live authorization or financial-data request was made. Browser regression tests were not run because no implementation changed.

Sources: [Chrome's experimental `restrict-properties` documentation](https://developer.chrome.com/blog/coop-restrict-properties), [HTML opener-policy processing](https://html.spec.whatwg.org/multipage/browsers.html#the-coop-headers), and [MDN browser compatibility data](https://github.com/mdn/browser-compat-data/blob/main/http/headers/Cross-Origin-Opener-Policy.json).

#### Subsequent local relay experiment — October 13, 2026

At the user's request, a standalone synthetic prototype tested the separate-origin relay architecture. The [sanitized results](local-relay-results-2026-10-13.json) show successful callback delivery and simulated PKCE exchange in Chromium, Firefox, and WebKit. Each engine first reproduced the lost-opener failure without the relay.

The relay retains the simulated client's opener and opens consent in a second window with `noopener`. Consent keeps `same-origin-allow-popups`. A server-side transaction releases a one-use callback URL to the relay's authenticated poll. The app session cookie never reaches the relay, and consent's opener remains null. Negative tests reject invalid request bindings, unauthorized polling, forged consent, household/session changes, expiry, and replay.

This verifies the local handoff mechanism, not the live Glama integration or an unchanged overall security posture. The simulated callback matches Glama's observed opener check and message delivery; other client behavior and the OAuth service are fixtures. The relay introduces a new security surface. Production would require an isolated origin, a narrowly authenticated handoff to the existing OAuth service, distributed one-use enforcement, abuse controls, and review. The prototype also adds a consent window and does not implement cancellation or delivery recovery.

The prototype remains outside the application repository. No real credentials or financial data were used. No deployment or submission occurred. Glama's live acceptance tests remain incomplete.

## PulseMCP

**Public listing unverified.** Manual submissions were paused at the October 13, 2026 check; downstream Registry ingestion has not been verified.

Manual submissions are paused. On October 13, 2026, the live [submission page](https://www.pulsemcp.com/submit) stated that it accepts neither new server/client submissions nor changes to existing listings. The notice was last updated September 3, 2026. It recommends publishing to the official MCP Registry and says its pipeline will pick entries up when it resumes.

This supersedes the older API page's description of an active manual submission route. No submission form is currently available, and no PulseMCP record was created.

### Prepared editorial fields

| Field | Draft value |
| --- | --- |
| Server name / provider | Use Display name / Publisher from the shared fields |
| Summary | Connect an AI assistant to BetterOff to review household accounts, spending, net worth, investments, and debt. Prepare corrections and transfer requests for approval in BetterOff. |
| Hosted endpoint / setup documentation / public connector repository | Use Remote URL / User documentation / Connector distribution from the shared fields |
| Registry name | finance.betteroff/mcp; published October 13, 2026 |
| Authentication / license / pricing | Use the shared fields and full description |

Use [shared listing copy](#shared-listing-copy) for the full description, policies, support, icon, and example prompts. These are prepared editorial fields, not a verified form or import schema.

Check for a matching PulseMCP entry when ingestion resumes; the official Registry publication is complete. Claim or correct an existing entry rather than create a duplicate. No reopening date or ingestion timeline is established. No monitoring automation has been created.
