"""Exercise server audit outcomes without network requests."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MOCK_CURL = r'''
import json, os, sys
args = sys.argv[1:]
case = os.environ.get('AUDIT_TEST_CASE', '')
mcp = 'https://api.betteroff.finance/mcp'
issuer = 'https://app.betteroff.finance/api/auth'
metadata = 'https://api.betteroff.finance/.well-known/oauth-protected-resource/mcp'
url = next(arg for arg in args if arg.startswith(('https://', 'http://')))
if case == 'dns_failure': sys.exit(6)
if case == 'server_timeout': sys.exit(28)
if 'OPTIONS' in args:
    if case == 'cors_timeout': sys.exit(28)
    print('HTTP/2 204')
    if case == 'cors_open': print('access-control-allow-origin: *')
elif '%{content_type}' in args:
    if case == 'metadata_timeout': sys.exit(28)
    print('text/html' if case == 'metadata_html' else 'application/json')
elif url.startswith('http://'):
    print('HTTP/1.1 301 Moved Permanently')
elif url == mcp + '?access_token=x':
    print('401')
elif url == mcp:
    if '-sI' in args:
        print('HTTP/2 401\nstrict-transport-security: max-age=31536000')
    else:
        print('HTTP/2 401')
        print(f'www-authenticate: Bearer resource_metadata="{metadata}", scope="accounts:read", error="invalid_token"')
elif url == metadata:
    print(json.dumps({'resource': mcp, 'authorization_servers': [issuer]}))
elif url.endswith('/jwks'):
    print(json.dumps({'keys': [{'kty': 'RSA', 'alg': 'RS256', 'n': 'test', 'e': 'AQAB'}]}))
elif url.endswith('/.well-known/oauth-authorization-server/api/auth'):
    print(json.dumps({'issuer': issuer, 'code_challenge_methods_supported': ['S256'],
        'id_token_signing_alg_values_supported': ['RS256'], 'jwks_uri': issuer + '/jwks',
        'registration_endpoint': issuer + '/register', 'authorization_endpoint': issuer + '/authorize',
        'token_endpoint': issuer + '/token', 'authorization_response_iss_parameter_supported': True,
        'grant_types_supported': ['authorization_code', 'refresh_token']}))
else:
    raise AssertionError(f'Unexpected curl request: {args}')
'''


class ServerAuditTests(unittest.TestCase):
    def run_audit(self, case=''):
        with tempfile.TemporaryDirectory() as directory:
            curl = Path(directory) / 'curl'
            curl.write_text(f'#!{sys.executable}\n' + MOCK_CURL)
            curl.chmod(0o755)
            return subprocess.run(
                ['bash', 'scripts/audit_server.sh'], cwd=ROOT, capture_output=True, text=True,
                env={**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH'],
                     'AUDIT_TEST_CASE': case}, timeout=30,
            )

    def test_valid_responses_pass(self):
        result = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('ok   CORS', result.stdout)

    def test_cors_request_timeout_fails(self):
        result = self.run_audit('cors_timeout')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn('ok   CORS', result.stdout)

    def test_well_known_request_timeout_fails(self):
        result = self.run_audit('metadata_timeout')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertNotIn('is not HTML', result.stdout)

    def test_runner_dns_failure_skips(self):
        result = self.run_audit('dns_failure')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('SKIP', result.stdout)

    def test_unreachable_server_fails(self):
        result = self.run_audit('server_timeout')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('FAIL cannot reach', result.stdout)
        self.assertNotIn('SKIP', result.stdout)

    def test_permissive_cors_fails(self):
        result = self.run_audit('cors_open')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('FAIL CORS allows an arbitrary origin', result.stdout)

    def test_html_well_known_response_fails(self):
        result = self.run_audit('metadata_html')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('returns HTML', result.stdout)


if __name__ == '__main__':
    unittest.main()
