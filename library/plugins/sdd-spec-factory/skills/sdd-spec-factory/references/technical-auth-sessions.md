# Authentication, authorization and sessions

## When to consult
Use for login, sessions, OAuth/OIDC, token refresh, roles, tenant access or logout.
Security retains threat modeling, controls and approval; this reference helps
SDD specify the boundary without replacing security-standard.

## Inspect and decide
- Trace existing identity provider, session/token store, client types, middleware,
  access checks, cookie configuration, logout and token issuance/revocation.
- Separate authentication from object/action/tenant authorization. Specify who
  can perform each action and deny paths server-side; hiding buttons is not a
  permission check. Identify issuer, audience and trust boundaries.
- Choose session versus OAuth/OIDC from the actual clients and provider. Do not
  add OAuth or JWT merely for a first-party login. Check implementation/version
  support for the chosen protocol and security controls.
- Specify expiry, revocation, refresh rotation or sender constraint, storage,
  CSRF protection where applicable, redirect validation and account recovery.
- Model refresh as concurrent state transitions: define atomic consumption,
  token-family relationships, replay detection and provider-defined behavior.
  Determine how simultaneous legitimate client refreshes are coordinated. Do
  not invent a grace period that silently weakens replay detection.
- Match cookies and token storage to the actual origin/client architecture;
  record Secure, HttpOnly, SameSite and CSRF/CORS decisions with limitations.
- Keep secrets, tokens and authentication payloads out of logs/spec examples.

## Verification example: refresh rotation
With a synthetic account, test login, access expiry, valid refresh and use of
the newly issued token. Replay the consumed refresh token, test revoked/expired
tokens, and race independent refresh requests. Assert the provider's documented
outcome and the approved replay response; do not assume both succeed. Verify
logout/revocation at the intended scope and cross-user/cross-tenant denial.
Test invalid issuer/audience/signature for token-based implementations and CSRF
for cookie-based operations. Record mocks separately from provider sandbox runs.
Missing provider semantics or a critical authz decision blocks the affected spec.

## Primary sources and handoff
- [OAuth 2.0 security BCP, RFC 9700, section 4.14](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)

Checked 2026-10-11. RFC 9700 addresses refresh-token replay and requires public
clients' refresh tokens to be sender-constrained or rotated. It supplements the
base OAuth specification; it does not define this project's session design.
Pin applicable ASVS version/control IDs in the project. Resolve the active
security-standard references and tool registry for validation, not another
scanner catalog. Proposed tests here are LOCAL TEST DESIGN until executed.
