// Generate dependency-free snippets for Zapier Platform UI Code Mode.
const fs = require('node:fs');
const path = require('node:path');

const operations = [
  { key: 'get_overview', name: 'Get Financial Overview', description: 'Gets the connected household’s financial overview, valuation, and data coverage.', tool: 'betteroff_get_overview', inputFields: [], args: '{}' },
  { key: 'get_net_worth_history', name: 'Get Net Worth History', description: 'Gets recorded net worth history for a selected period.', tool: 'betteroff_get_net_worth_history', inputFields: [{ key: 'period', label: 'Period', type: 'string', required: true, default: '30d', choices: ['7d', '30d', '90d', 'all'] }], args: '{ period: bundle.inputData.period || "30d" }' },
];

function code(operation) {
  return `const args = ${operation.args};
${operation.key === 'get_net_worth_history' ? 'if (!["7d", "30d", "90d", "all"].includes(args.period)) throw new z.errors.Error("Choose a supported period.", "INVALID_INPUT", 400);' : ''}
return z.request({
  url: "https://api.betteroff.finance/v1/tools/${operation.tool}",
  method: "POST",
  skipThrowForStatus: true,
  headers: { Authorization: "Bearer " + bundle.authData.api_token, "Content-Type": "application/json", Accept: "application/json" },
  body: args
}).then(response => {
  if (response.status === 401) throw new z.errors.Error("Reconnect BetterOff with a valid, unexpired API token.", "AUTHENTICATION_FAILED", 401);
  if (response.status === 403) throw new z.errors.Error("Check household consent, token permissions, and whether access was revoked in BetterOff.", "ACCESS_DENIED", 403);
  if (response.status === 429) {
    const delay = Number(response.headers['retry-after']);
    throw new z.errors.ThrottledError("BetterOff rate limit reached.", Number.isFinite(delay) && delay > 0 ? Math.ceil(delay) : 60);
  }
  response.throwForStatus();
  const result = response.data;
  if (!result || result.ok !== true || result.schemaVersion !== "4" || !result.data || typeof result.data !== "object" || Array.isArray(result.data) || !result.quality) {
    throw new z.errors.Error("BetterOff did not return a supported successful result.", "INVALID_RESPONSE", 502);
  }
  // Preserve currency, freshness, quality, warnings, and pagination qualifications.
  return result;
});
`;
}

const draft = {
  status: 'local-draft-not-submitted',
  name: 'BetterOff',
  description: 'BetterOff is a household finance app for tracking accounts, net worth, spending, investments, and debt.',
  homepage: 'https://betteroff.finance',
  apiDocumentation: 'https://betteroff.finance/developers',
  requestTemplate: { params: { source: 'zapier' }, headers: {} },
  authentication: {
    type: 'custom',
    platformUiLabel: 'API Key',
    fields: [{ key: 'api_token', label: 'API Token', type: 'password', required: true, helpText: 'Create a token in [BetterOff API tokens](https://app.betteroff.finance/settings/api-tokens). Select only accounts:read and networth:read. Reconnect here before the token expires.' }],
    requiredScopes: ['accounts:read', 'networth:read'],
    connectionLabel: 'BetterOff read-only: {{bundle.inputData.data.identity.name}}',
    testCodeFile: 'authentication.js.txt',
  },
  actions: operations.map(({ args, ...operation }) => ({ ...operation, type: 'create', codeFile: `${operation.key}.js.txt` })),
};

if (require.main === module) {
  const destination = path.resolve(process.argv[2] || '.private/zapier-draft');
  fs.mkdirSync(destination, { recursive: true });
  fs.writeFileSync(path.join(destination, 'platform-ui-draft.json'), JSON.stringify(draft, null, 2) + '\n');
  fs.writeFileSync(path.join(destination, 'authentication.js.txt'), code(operations[0]));
  for (const operation of operations) fs.writeFileSync(path.join(destination, `${operation.key}.js.txt`), code(operation));
  console.log(`Wrote local Platform UI draft to ${destination}`);
}

module.exports = { operations, code, draft };
