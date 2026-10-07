# Contributing to BetterOff connectors

Changes reach `main` only through pull requests. Branch protection applies to administrators, every commit must be signed, and the `package` check must pass before a pull request can merge.

The **Audit** workflow in `.github/workflows/audit.yml` runs two jobs:

- **`package`** runs on pull requests, pushes to `main`, and manual runs. It tests and runs the public-content and package audits, scans the full Git history with gitleaks, and validates the marketplace and the plugin with `claude plugin validate --strict`.
- **`server`** runs daily and on manual runs. It checks the live MCP endpoint's OAuth discovery, token rejection, HTTPS redirect, HSTS, and CORS behavior. It does not run on pull requests, so a server outage cannot block a merge.

To run the same checks before you open a pull request, run these commands from the repository root. The server check needs `curl` and `jq`.

```sh
python3 scripts/test_audit_public.py && python3 scripts/audit_public.py
python3 scripts/test_audit_package.py && python3 scripts/audit_package.py
gitleaks git --redact --no-banner .
claude plugin validate --strict . && claude plugin validate --strict plugins/betteroff
scripts/audit_server.sh
```

Dependabot proposes GitHub Actions updates weekly and waits 7 days after each release. Update the other two pinned tools by hand in `audit.yml`:

- **gitleaks:** change `GITLEAKS_VERSION` and `GITLEAKS_SHA256` together. Take the hash from the `linux_x64` line of the release's `checksums.txt`.
- **Claude Code:** `--strict` validation needs version 2.1.281 or later. Bump it deliberately and confirm that validation still passes.
