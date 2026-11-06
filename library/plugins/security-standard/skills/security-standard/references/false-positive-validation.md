# False-Positive Validation

Use this checklist before confirming, counting, publishing, or externally
tracking any vulnerability. A suspicious pattern is a candidate, not a finding.

## Mandatory Decision Checklist

Answer every item with repository or runtime evidence:

1. Is the source controlled by an attacker or an actor crossing a privilege,
   tenant, or trust boundary?
2. Is the path reachable in the target revision and deployed runtime?
3. Does data or authority reach a security-sensitive effect?
4. Is the expected control absent, misplaced, or demonstrably bypassable?
5. Were local and imported validators, guards, policies, middleware, wrappers,
   framework defaults, database constraints, proxy/CDN controls, and deployment
   configuration checked?
6. Are exploitation preconditions realistic and explicitly bounded?
7. Is the impact a security consequence rather than an ordinary correctness,
   reliability, style, deprecation, or hardening concern?
8. Is the claim compatible with the detected framework, runtime, dependency,
   and deployment versions?
9. Is there safe reproduction, a negative test, or deterministic source proof?
10. Was counterevidence recorded and shown insufficient?

If any answer is `NO`, classify `FALSE_POSITIVE` or `INFO` when a useful
hardening recommendation remains. If any answer is `UNKNOWN`, classify
`NEEDS_VALIDATION`, `DEFERRED`, or `BLOCKED`. Never use uncertainty to inflate
severity.

## Common Rejection Patterns

Reject or downgrade when evidence shows:

- a scanner reported a vulnerable package but evidence excludes every relevant
  runtime, build and install path, or proves an effective downstream patch;
  development-only or outside the deployed artifact alone does not exclude
  supply-chain impact
- a dependency is merely old and no applicable advisory or vulnerable behavior
  is established
- authentication or authorization exists in an imported guard, policy, base
  controller, middleware, route group, reverse proxy, or trusted service boundary
- an ORM or framework API parameterizes, escapes, sanitizes, validates, or
  rejects the suspected input in the installed version
- user-controlled text is rendered through an escaping template or DOM binding
  and never reaches a raw HTML or script-capable sink
- a secret-shaped value is a placeholder, test fixture, public identifier, or
  untracked local environment value rather than a real credential
- missing CSP, HSTS, rate limiting, MFA, or another defense-in-depth control has
  no demonstrated vulnerable path; report as `INFO` hardening at most
- code exists only in tests, examples, generated output, vendored dependencies,
  dead paths, disabled features, or non-production configuration
- CORS, CSRF, webhook, cache, proxy, or routing behavior is judged without the
  actual framework and deployment semantics
- a business rule makes the resource intentionally public or cross-tenant and
  repository evidence confirms that policy

## Publication Gate

Automatic creation or update of GitHub issues, pull requests, Jira/Linear items,
advisories, customer findings, and release blockers requires:

- `status: CONFIRMED`
- `confidence: HIGH` or `MEDIUM`
- complete evidence contract
- all checklist items answered `YES`
- stable affected revision and locations
- duplicate and sibling-instance reconciliation

Keep everything else in the internal validation backlog. When a human explicitly
requests external tracking of an unresolved candidate, label it
`NEEDS_VALIDATION`, state missing evidence in the title and body, and exclude it
from confirmed counts.
