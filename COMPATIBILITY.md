# BetterOff connector compatibility review

Reviewed and updated on 2026-10-02 for BetterOff maintainers deciding what to support and release. The implementation status below supersedes the initial audit findings that follow.

BetterOff has a shared remote MCP service and package formats suitable for broad client compatibility. Production verification is strongest for Codex and interactive Claude Code. The other documented clients have plausible installation and authentication paths, but this repository does not contain evidence that each completed the full BetterOff connection lifecycle. Public directory availability requires separate review and publication.

This review covers the relevant official packaging, installation, MCP transport, authentication, permissions, and publication documentation for the 10 clients named in the README. It also checks ChatGPT, Claude consumer surfaces, and two additional editor clients. It does not claim to cover every page on those documentation sites or every MCP client.

## Release follow-up on 2026-10-05

The production fixes and synthetic household checks recorded on October 2 remain the latest authenticated evidence. On October 5, the package audit, regression test, strict Claude marketplace and plugin validation, live endpoint audit, and Git whitespace check passed. The package audit still reports missing demo recording URLs in both OpenAI manifests.

Anthropic recorded a publication request for version 0.3.0 at source revision e64aee5. Its security scan passed; reviewer approval and public listing remain pending. OpenAI still reports an incomplete MCP configuration and a scan that did not complete. The user already opened a support case; no duplicate report was sent.

The main application's source-sync check now reports seven differences. Its source uses the older `betteroff-connectors` repository URL, which GitHub resolves to this checkout's `betteroff.connectors` repository. Differences also include manifest formatting and generated metadata. Preserve the existing contents until the source and public package are reconciled. No source-sync write was performed.

The demo recording, Gemini sign-in, eligible Copilot access, and remaining client journeys are pending. Installation and transport checks do not establish a complete AI journey. This follow-up received a plain-text review; an automated grammar check was not run.

## Implementation status on 2026-10-02

The local package fixes are complete, and all 20 tools passed production HTTP checks against a separate synthetic household. Authenticated journeys through every named client, the demo recording, and public-directory submission remain unfinished.

- The main source preserves the public portable and Codex metadata and Cursor manifest. The existing sync emits Gemini metadata and native skills, reports no drift, and refuses target-only file removal before writing. Regression checks cover both preservation and drift.
- The README, shared skill, release notes, and submission guides describe 20 tools, including setup status. Prerequisites include paid access, household AI-processing consent, and applicable Terms acceptance. Historical verification records retain their original tool counts.
- Muse Code examples use canonical user-settings keys and explain its plugin OAuth limitation. Approval descriptions qualify client policy and harness differences.
- Gemini uses extension-root native skills. Its generated skill matches the shared plugin skill; the package audit detects drift. Persistent context injection was removed to avoid loading the same instructions twice.
- The package audit independently validates inline OpenAI metadata and the Codex fallback. Its regression check rejects an unsupported inline review field and a stale Gemini skill. CI runs that check.
- Package identity and the Claude manifest now retain the existing public description. The release builder retains its name, version, and description checks. It builds two client distributions and one submission-only package in the scratch project. No existing release artifacts were replaced.
- A recording script is prepared in the main application's private submission materials. No video or accessible recording URL exists yet.

Checks performed after the changes:

| Check | Result |
| --- | --- |
| Package audit and Python regression check | Passed; recording URL remains absent in both OpenAI manifests. |
| Strict Claude marketplace and plugin validation | Passed with Claude Code 2.1.287. |
| Source-to-public sync check | Passed with no drift. |
| Source sync, marketplace, MCP transport, OAuth discovery, OAuth flow, resource authorization, reviewer credentials, and setup-denial regression | 28 passed, zero failed. These are local tests, not client production journeys. |
| Authenticated production HTTP OAuth and MCP | Owner and viewer sign-in passed; public registration, owner consent, PKCE exchange, initialization, and the 20-tool catalog passed. |
| Production read and analysis tools | 17/17 passed with valid fixture inputs. Holdings, recurring streams, transactions, snapshots, and debt terms were populated; DeFi, observations, and initial activity responses were empty. |
| Production correction boundary | All three proposals left financial records unchanged. Authenticated review approval and undo passed for each type; follow-up reads confirmed that undo restored the original values. |
| Production scope and token lifecycle | Accounts-only token exposed two tools and rejected an ungranted transaction tool with HTTP 403 and `insufficient_scope`. Refresh rotated; used-token replay failed. After disconnect, a fresh read returned 403 and refresh returned 400 `invalid_grant`. |
| Independent fixture reconciliation | Cash flow, transfer exclusion, net-worth change, holding value and gain, recurring count, debt balance, and payoff matched Decimal calculations from the known synthetic inputs. |
| Main app TypeScript and scoped Biome | Passed for the local setup-denial fix and regression test. |
| Live unauthenticated endpoint audit | Passed. |
| Release distribution build | Passed. |
| Clean Claude installation | Installed plugin and setup-aware skill; resolved HTTP server, which reports that authentication is needed. |
| Hermes 0.16.0 scratch configuration | Recognized the enabled server and household-review skill. No OAuth login or tool call was performed. |
| Copilot CLI 1.0.91 local marketplace installation | Installed plugin and skill; resolved BetterOff as an enabled HTTP server from plugin 0.3.0. No authenticated tool call was performed. |
| Gemini CLI 0.62.0 clean local extension | Installed and enabled the extension, discovered the native skill, and resolved the HTTP server. Authentication is required; no tool call was performed. |
| Codex 0.159.2 inventory | Existing BetterOff 0.3.0 is enabled. No fresh installation or grant was performed. |

Gemini CLI 0.62.0 and Copilot CLI 1.0.91 were installed from their official npm packages into `/Users/mb1/Code/scratch/betteroff-connector-verification/clients`; they were not added as application dependencies. Initial Gemini local installation attempts waited for its folder-trust prompt and timed out. After accepting trust for the reviewed scratch extension, installation and native skill discovery passed.

Neon access was available. The existing reviewer household was preserved, and the existing provisioning script created a separate synthetic owner and viewer. The fixture now has three accounts, four transactions, two snapshots, one holding, one detected recurring stream, and one debt with terms. Credentials and connection strings remain private outside both repositories. The script required the existing worker database role for household admission; the database owner role was insufficient. No security check was changed.

Viewer OAuth authorization returned HTTP 500. The local fix makes the existing setup exception a Better Auth `APIError`, returning HTTP 403 with `AGENT_SETUP_REQUIRED`. A real OAuth regression test covers owner, subscription, Terms, and AI-consent denials and confirms that no consent or token is created. The fix has not been deployed.

The production reviewer page remained on “Loading authentication form” in the task browser and logged React error 412 after reload and a fresh response. The official React error message is “Connection closed.” Direct HTTP responses contained the form, and authenticated server actions worked; this does not establish the browser failure's cause or behavior in other browsers. Tests used normal HTTP authentication, consent, and review actions rather than inserting sessions, tokens, or grants into the database. They do not verify rendered browser journeys.

The remaining clients and consumer surfaces still need their own accounts, installed runtimes, and authenticated journeys. Keep `releaseEligible` false until those promised paths and directory requirements pass. The tested synthetic corrections were undone, and the verification grant was disconnected. No real household financial records were modified. No commits, pushes, deployments, or directory submissions were performed.

## Initial audit: what we had

| Component | Evidence | Assessment |
| --- | --- | --- |
| Shared remote service | `https://api.betteroff.finance/mcp`; all package configurations use this URL | Reuse this service across clients. |
| Portable plugin | `plugins/betteroff/plugin.json`, `mcp.json`, and `skills/household-review/SKILL.md` | Matches the standard component layout. |
| Client compatibility manifests | Codex, Claude Code, and Cursor manifests; Gemini extension manifest | Existing formats cover the documented package installation routes. |
| Manual connection routes | README instructions for Hermes, Muse Code, OpenClaw, and Pi | These clients do not need another BetterOff server implementation. |
| OAuth discovery | Live resource and authorization-server metadata | Advertises authorization code, refresh tokens, S256 PKCE, dynamic client registration, client metadata documents, and issuer identification. |
| Tool catalog | This chat's connector exposes 20 tool names; local API transport tests expect 20 | The public README and skill still describe 19. The omitted tool is `betteroff_get_setup_status`. |
| Response contracts | Main application MCP adapter and transport tests | Structured responses, JSON text equivalents, output schemas, scope filtering, and explicit safety annotations exist. |
| Financial authorization | Main application authorization source | Household owner, paid access, household AI-processing consent, applicable Terms acceptance, active grants, and tool scopes govern access. |
| Correction boundary | Main application source and retained verification | Three tools persist proposals. Financial application requires authenticated review in BetterOff. |

The [Agent Plugins specification](https://agent-plugins.org/specification) defines root `plugin.json`, fixed `skills/` discovery, and root `mcp.json`. Our portable package uses those locations and declares `streamable-http`. Compatibility manifests serve clients that use their own formats.

The [MCP transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) permits JSON responses, stateless operation, and HTTP 405 for an unused GET stream. These are deliberate choices in the BetterOff adapter. A legacy SSE service, local proxy, persistent session store, and interactive widget are not requirements for the existing workflows.

## Client assessment

“Documented fit” means the official client requirements match our configuration. It does not mean a live BetterOff journey passed.

| Client | What we have | Evidence and remaining work |
| --- | --- | --- |
| Codex | Portable plugin, Codex fallback manifest, and marketplace | Retained production evidence covers actual calls to all former 19 tools. Repeat against the 20-tool/schema-4 service and record the client version, refresh, and revocation. Official [plugin packaging](https://developers.openai.com/plugins/build/plugins) supports our layout. |
| Claude Code | Native manifest, HTTP MCP configuration, skill, and marketplace | Strict validators pass. Retained evidence covers interactive production calls to all former 19 tools. Noninteractive `claude -p` plugin loading was not verified successfully in that record. Test it separately if we support automation. See [manifest reference](https://code.claude.com/docs/en/plugins-reference) and [MCP authentication](https://code.claude.com/docs/en/mcp). |
| GitHub Copilot | Portable plugin and marketplace install instructions | Documented fit for CLI, VS Code, and the Copilot app. Verify each surface separately. GitHub confirms [portable plugin discovery](https://docs.github.com/en/copilot/concepts/agents/about-plugins); VS Code documents [installation from source](https://code.visualstudio.com/docs/agent-customization/agent-plugins). |
| Cursor | Portable plugin, native Cursor manifest, local install, and direct MCP configuration | Documented fit. Confirm local loading, OAuth, and skill availability. Enterprise policy can block local imports. [Cursor plugin reference](https://prod.cursor.com/docs/reference/plugins) and [plugin installation](https://prod.cursor.com/docs/plugins) distinguish local development, team distribution, and marketplace listing. |
| Gemini CLI | Root extension manifest with `httpUrl` and `contextFileName` | MCP configuration fits the [official MCP guide](https://geminicli.com/docs/tools/mcp-server/). OAuth callbacks require matching `iss`; our metadata advertises support, but a successful Gemini callback remains unverified. Our review skill loads as extension context, not a native extension skill. Native discovery requires extension-root `skills/`, per the [extension reference](https://geminicli.com/docs/extensions/reference/). |
| Devin | Repository-subdirectory plugin install and separate MCP sign-in | Documented fit. Verify web and CLI independently. Personal access does not isolate a session from other organization members who can interact with it; organization access shares one sign-in. Keep the README warning. See [plugins](https://docs.devin.ai/product-guides/plugins) and [MCP connections](https://docs.devin.ai/work-with-devin/mcp). |
| Hermes Agent | OAuth server configuration, `trust: untrusted`, sampling disabled, and skill install | Configuration fits the [MCP reference](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference/). Untrusted mode asks before tools lacking a true read-only annotation. Verify browser callback, refresh, proposals, and isolation for the deployment's profiles and users. |
| Muse Code | User settings connection, OAuth login, and separate skill install | Correct route. The README's settings keys are accepted legacy spellings; prefer canonical `mcpServers`, `type: streamable-http`, and `required: false`. Muse Code plugin servers cannot receive OAuth credentials, and its login command does not authenticate project-only servers. See [official MCP documentation](https://meta-models.github.io/muse-code-sdk/next/guides/extend/mcp-servers/). |
| OpenClaw | Direct remote MCP connection, OAuth login, probe, and skill install | Documented fit. Verify the actual Gateway and agent harness, because credential storage and approval behavior depend on the runtime. Retain the direct-owner-chat restriction unless requester isolation is explicitly configured and tested. See [connection guide](https://docs.openclaw.ai/tools/mcp) and [MCP CLI reference](https://docs.openclaw.ai/cli/mcp). |
| Pi | Built-in MCP setup, OAuth, direct tool exposure, and shared skill copy | Version floor is correct: [Pi 0.99.0 introduced built-in MCP](https://pi.dev/changelog/releases/0.99.0). Verify the installed version and extensions. An extension registering `/mcp` can replace built-in session support even while shell `pi mcp` commands still work. Permission extensions can also change approval behavior. See [MCP documentation](https://pi.dev/docs/latest/mcp). |

## Additional surfaces

- **ChatGPT:** The portable package can use OpenAI's shared public directory, but repository installation in Codex does not establish ChatGPT directory availability. Complete developer identity, domain verification, server scanning, review materials, and publication. See [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission).
- **Claude web, Desktop, mobile, and Cowork:** A remote connector can reach these surfaces, subject to account and organization access. For directory distribution, Anthropic requires a separate MCP connector submission even when a plugin references the same server. See [directory publishing](https://claude.com/docs/directory/publish) and [remote connector availability](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors).
- **Windsurf / Devin Desktop Cascade:** Official [MCP documentation](https://docs.devin.ai/desktop/cascade/mcp) supports Streamable HTTP and OAuth. We have no public setup section or retained BetterOff verification for this route. This is a candidate for a configuration example and lifecycle test.
- **Cline:** The [official MCP overview](https://docs.cline.bot/mcp/mcp-overview) documents remote servers and requires explicit `type: streamableHttp` to avoid legacy SSE defaults. That page alone does not establish the complete BetterOff OAuth lifecycle. Confirm OAuth behavior before advertising support.
- **Consumer Muse:** This is distinct from Muse Code. The [Muse Connector Platform](https://muse.ai/platform) describes review and end-to-end testing, but does not establish the client registration, redirect, or refresh contract needed here. Retained internal records put this integration on hold. Do not infer consumer support from Muse Code documentation.

An MCP-capable client can still be incompatible if it only supports local stdio, legacy SSE, static tokens, machine-to-machine grants, or an OAuth flow we do not accept. Our live authorization metadata offers authorization code and refresh grants; it does not offer `client_credentials`.

## Required work, in order

1. **Reconcile the two package sources before synchronizing.** The main application's `tools/connectors/sync-public.ts --check` reports five differing files. Write mode deletes files absent from its source, including the public Cursor manifest. It also replaces the portable and Codex manifests, including existing uncommitted work. Preserve the expanded public formats, then make the existing drift check protect them. Do not add a second generator.
2. **Update the public catalog and prerequisites.** Add `betteroff_get_setup_status` to the shared skill and explain that the catalog has 17 reads or analyses and three proposals. Keep version 0.3.0 unless a release decision changes it. Document paid access, household AI-processing consent, and applicable Terms requirements; an owner account alone is insufficient.
3. **Record live verification per client and surface.** Start with the eight clients lacking retained full lifecycle evidence, then recheck Codex and Claude Code against the current catalog. Record installation, skill loading, authorization, tools, typed errors, renewal, scope upgrades, disconnect, and denied access after disconnect. Pin the tested client version and package revision.
4. **Qualify approval claims.** The README describes several clients as always asking or never asking. Client policies, allowlists, extensions, and agent harnesses can change this behavior. State the tested default and configuration. BetterOff review remains the enforcement point for applying financial corrections, regardless of client prompts.
5. **Decide Gemini skill delivery.** Persistent extension context already carries the instructions. If native on-demand skill activation is part of our support promise, expose the skill through Gemini's extension-root `skills/` convention and test discovery. This is a packaging change, not a new backend.
6. **Finish directory review materials.** The OpenAI manifest contains five positive cases, three negative cases, and release notes, but no `demo_recording_url`. Prepare an accessible recording and a populated synthetic reviewer household; run the cases with that account. Verify publisher identity and domain ownership in the portal. Anthropic also requires a populated account and every tool tested in MCP Inspector and Claude. See [OpenAI review materials](https://developers.openai.com/plugins/deploy/submission) and [Anthropic's connector checklist](https://claude.com/docs/connectors/building/review-criteria).
7. **Refresh the retained release record.** Its top-level `releaseEligible` remains false and its newest client evidence predates schema 4 and the setup tool. Historical results include data-limited success paths and a spending-pattern failure followed by a local fix. Recheck those paths before describing the current release as fully verified. A contract-compliant error is not a successful financial operation.

## Minimum acceptance sequence

Use a synthetic household with populated accounts, transactions, recurring items, positions, activity, and debt terms. Keep credentials outside this package.

1. Install through the documented route in a clean client configuration and confirm the skill or extension context loads.
2. Authorize with the intended owner and selected permissions; confirm that rejected consent returns cleanly to the client.
3. Discover the expected scope-filtered catalog and execute every permitted tool with valid fixture inputs.
4. Verify partial data, empty data, pagination, schema validation, and typed errors without treating missing values as zero.
5. Prepare each correction type and verify that records remain unchanged until BetterOff review approval. Exercise approval and undo only against the synthetic household.
6. Confirm token renewal after expiry and reauthorization for added scopes.
7. Disconnect in BetterOff and verify that a fresh read and refresh are denied. Test wrong household, non-owner, lost entitlement, and audit failure through isolated fixtures.
8. Save sanitized outcomes with client version, environment, source revision, and date. Record failures and untested paths explicitly.

## Checks and limits

Checks run for this review:

- `python3 scripts/audit_package.py`: passed; one warning for the absent demo recording.
- `claude plugin validate --strict .`: passed with Claude Code 2.1.287.
- `claude plugin validate --strict plugins/betteroff`: passed with Claude Code 2.1.287.
- `scripts/audit_server.sh`: passed the live unauthenticated endpoint, discovery, invalid-token, redirect, HSTS, and CORS checks.
- Direct public metadata reads: confirmed eight permission families, both supported grant types, S256, registration, CIMD, and issuer identification.
- Main application's `bun test apps/api/test/mcp-transport.test.ts`: four tests passed, with 123 assertions. This checks local source, not a production deployment.
- Main application's `sync-public.ts ... --check`: failed as expected, identifying five differing files. No synchronization was performed.
- Portable OpenAI review and publication settings match the Codex fallback. Current audit code primarily validates the fallback; root portable metadata also needs independent validation because OpenAI's inline extension replaces the fallback rather than merging it.

Retained production evidence is in the main application's `docs/agent-connectors.verification.json`, especially `productionCodexClaudeFollowUp` and `codexClaudeNineteenToolVerification`. Those checks were recorded on 2026-09-28 and remain scoped to their revisions. Existing source and package work was preserved.

The initial audit performed no new household tool calls, OAuth grants, corrections, directory submissions, installations, commits, pushes, or deployments. Its findings establish documentation fit and the checks listed in that section. The later implementation status above records the new authenticated synthetic tests and their limits. Full live support for every client and current portal status remain unverified. The report received a plain-text author review; an automated grammar check and rendered review were not run.
