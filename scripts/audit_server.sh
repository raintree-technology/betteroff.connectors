#!/usr/bin/env bash
# Unauthenticated MCP endpoint and OAuth discovery checks (MCP authorization spec 2025-11-25).
# Usage: scripts/audit_server.sh  (run from repo root; needs curl and jq). Exits 1 on any FAIL.
set -u
# Bound every request so an unresponsive server fails fast instead of hanging the job.
curl() { command curl --max-time 20 "$@"; }
F=0
fail() { echo "FAIL $*"; F=1; }
ok() { echo "ok   $*"; }
warn() { echo "warn $*"; }

MCP=$(jq -r '.mcpServers | to_entries[0].value.url' plugins/betteroff/.mcp.json)
[[ $MCP == https://* ]] && ok "MCP URL $MCP" || fail "MCP URL is not HTTPS: $MCP"

# 401 challenge
H=$(curl -si -X POST "$MCP" -H 'Content-Type: application/json' -d '{}' | tr -d '\r')
grep -q '^HTTP/[0-9.]* 401' <<<"$H" && ok "unauthenticated request gets 401" || fail "no 401 without a token"
WA=$(grep -i '^www-authenticate:' <<<"$H")
RM=$(sed -n 's/.*resource_metadata="\([^"]*\)".*/\1/p' <<<"$WA")
[[ -n $RM ]] && ok "resource_metadata $RM" || fail "WWW-Authenticate has no resource_metadata"
grep -q 'scope="' <<<"$WA" && ok "challenge includes scope" || warn "challenge has no scope"
BAD_TOKEN='invalid.token.value' # gitleaks:allow deliberately invalid token for the 401 check
curl -si -X POST "$MCP" -H "Authorization: Bearer $BAD_TOKEN" -d '{}' | grep -i '^www-authenticate:' | grep -q 'error="invalid_token"' \
  && ok "bad token gets error=invalid_token" || fail "bad token response lacks error=\"invalid_token\""
[[ $(curl -s -o /dev/null -w '%{http_code}' "$MCP?access_token=x") == 401 ]] && ok "query-string token rejected" || fail "query-string token not rejected"

# Protected resource metadata
PRM=$(curl -s "${RM:-$MCP}")
if jq -e . >/dev/null 2>&1 <<<"$PRM"; then
  [[ $(jq -r .resource <<<"$PRM") == "$MCP" ]] && ok "PRM resource matches .mcp.json" || fail "PRM resource $(jq -r .resource <<<"$PRM") != $MCP"
else
  fail "protected resource metadata is not JSON"
fi
AS=$(jq -r '.authorization_servers[0] // empty' <<<"$PRM" 2>/dev/null)
[[ $AS == https://* ]] && ok "authorization server $AS" || fail "no HTTPS authorization server in PRM"

# Authorization server metadata, in spec priority order for an issuer with a path
ORIGIN=$(sed -E 's#(https://[^/]+).*#\1#' <<<"$AS")
ISSPATH=$(sed -E 's#https://[^/]+##' <<<"$AS")
ASM=""
for u in "$ORIGIN/.well-known/oauth-authorization-server$ISSPATH" "$ORIGIN/.well-known/openid-configuration$ISSPATH" "$AS/.well-known/openid-configuration"; do
  body=$(curl -s -H 'Accept: application/json' "$u")
  if jq -e .issuer >/dev/null 2>&1 <<<"$body"; then ASM=$body; ok "AS metadata at $u"; break; fi
  warn "no AS metadata: $(curl -s -o /dev/null -w '%{http_code} %{content_type}' "$u") $u"
done
if [[ -z $ASM ]]; then
  fail "authorization server metadata unreachable"
else
  [[ $(jq -r .issuer <<<"$ASM") == "$AS" ]] && ok "issuer matches" || fail "issuer $(jq -r .issuer <<<"$ASM") != $AS"
  jq -e '.code_challenge_methods_supported | index("S256")' >/dev/null <<<"$ASM" && ok "PKCE S256" || fail "S256 not advertised"
  jq -e '.registration_endpoint or .client_id_metadata_document_supported' >/dev/null <<<"$ASM" && ok "DCR or CIMD" || fail "no DCR or CIMD"
  jq -e '.registration_endpoint' >/dev/null <<<"$ASM" || warn "no DCR: Pi, OpenClaw, Muse Code, and Cursor register clients with DCR by default"
  jq -e '.authorization_response_iss_parameter_supported' >/dev/null <<<"$ASM" && ok "RFC 9207 iss" || warn "RFC 9207 iss not advertised"
  jq -e '.grant_types_supported // [] | index("implicit") or index("password")' >/dev/null <<<"$ASM" && fail "implicit or password grant offered"
  jq -r '[.authorization_endpoint, .token_endpoint, .registration_endpoint] | .[] | select(. != null)' <<<"$ASM" | grep -v '^https://' && fail "non-HTTPS AS endpoint"
fi

# Unknown well-known paths must not return the app's HTML page
for u in "$ORIGIN/.well-known/oauth-authorization-server" "$ORIGIN/.well-known/openid-configuration"; do
  ct=$(curl -sL -o /dev/null -w '%{content_type}' "$u")
  [[ $ct == text/html* ]] && fail "$u returns HTML" || ok "$u is not HTML"
done

# Transport
curl -sI "${MCP/https:/http:}" | head -1 | grep -qE ' 30[18]' && ok "HTTP redirects to HTTPS" || fail "HTTP not redirected"
curl -sI "$MCP" | grep -iq '^strict-transport-security' && ok "HSTS" || fail "no HSTS"
curl -si -X OPTIONS "$MCP" -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: POST' \
  | grep -iqE '^access-control-allow-origin: (\*|https://evil)' && fail "CORS allows an arbitrary origin" || ok "CORS"

exit $F
