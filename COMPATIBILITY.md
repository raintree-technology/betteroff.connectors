# BetterOff client compatibility

BetterOff uses one remote MCP endpoint across clients. Installation instructions
are available for the clients below, but a documented configuration does not
establish a complete authenticated journey. Status recorded on 2026-10-06.

## Connection requirements

A client must support Streamable HTTP and BetterOff's OAuth authorization flow.
The endpoint is `https://api.betteroff.finance/mcp`. Static-token, local-stdio,
legacy-SSE, and machine-to-machine-only clients do not satisfy this contract.

Only an eligible household owner can grant access. Paid access, household
AI-processing consent, and acceptance of the applicable Terms are required.
The connector reads permitted financial data and prepares corrections. Applying
a correction requires authenticated approval in BetterOff.

## Client status

| Client | Available route | Verification limit |
| --- | --- | --- |
| Codex | Plugin and marketplace | Authenticated synthetic tool checks passed. A complete fresh-install, renewal, and revocation journey for the current client version remains unverified. |
| Claude Code | Plugin and marketplace | Interactive authenticated synthetic tool checks passed. Automated sessions and the complete current-version lifecycle remain unverified. |
| GitHub Copilot | Plugin and marketplace | CLI installation passed. Authenticated journeys and other Copilot surfaces remain unverified. |
| Cursor | Local plugin or remote MCP configuration | Installation instructions are provided. A complete authenticated journey remains unverified. |
| Gemini CLI | Extension with native skill | Extension installation and skill discovery passed. Authentication and financial tool calls remain unverified. |
| Devin | Plugin and personal MCP connection | Configuration instructions are provided. A complete authenticated journey remains unverified. |
| Hermes Agent | Remote MCP configuration and skill | Authenticated synthetic tool checks passed. A complete current-version lifecycle remains unverified. |
| Muse Code | User MCP settings and separate skill | Configuration instructions are provided. A complete authenticated journey remains unverified. |
| OpenClaw | Remote MCP connection and skill | Configuration instructions are provided. A complete authenticated journey remains unverified. |
| Pi | Built-in MCP connection and shared skill | Configuration instructions require Pi 0.99.0 or later. A complete authenticated journey remains unverified. |
| Instinct | No verified route | BetterOff connection support remains unverified. |

These results cover synthetic data and the tested configurations. They do not
establish compatibility with every client version, policy, extension, or host.
See the [installation guide](README.md#install-the-connector) for configuration.

## Access and approval boundaries

Client tool prompts depend on client policy. BetterOff's authenticated review
page remains the approval boundary for applying financial corrections.

Devin organization access shares a BetterOff sign-in across member sessions.
Use personal access and consider who can interact with your sessions. OpenClaw
can share a sign-in with everyone who can message an agent; use a direct chat
with the household owner unless requester isolation has been verified.

Disconnect through [BetterOff Agent connections](https://app.betteroff.finance/settings/agents).
Do not paste credentials or access tokens into agent conversations.

## Directory availability

Repository installation does not establish availability in the ChatGPT or
Claude connector directories. Directory publication and review remain separate.
This repository does not claim that every consumer surface is publicly listed.

## Verification coverage

Candidate 0.3.1 adds one diagnostic feedback tool to the 17 read or analysis
tools and three correction proposal tools. Feedback requires separate opt-in
permission and user approval of the report. Its production availability remains
unverified. Shared synthetic HTTP checks for the earlier release covered the catalog, scope enforcement,
correction review and undo, token rotation, and denial after disconnection.
Those service checks do not replace authenticated tests in each client.

Full client verification must cover installation, skill loading, consent,
permitted tool discovery, populated reads, missing-data responses, correction
preparation, token renewal, and denial after disconnection. Record the client
version, package revision, and test date when publishing results.
