# Quality, security and operational readiness

## When to consult
Use when selecting validation for a failure mode, dependency change, release,
infrastructure, observability or recovery. Route each obligation to its existing
owner. This is a planning companion, not another Quality Gate implementation.

## Reuse canonical owners
- QA: active qa-testing-standard `references/test-strategy.md` for risk-based
  scenarios and `references/bug-report.md` for reproduction/retest.
- Security: active security-standard SKILL and triggered coverage/review/tool
  references; advisories via its existing OSV route, not a new scanner registry.
- DevOps: active devops-standard references for CI/CD, deployments,
  observability, backup/disaster recovery and operations.
- Harness: active context-routing, execution receipts and final reconciliation.
  Resolve installed bundles or an explicit canonical checkout. Missing mandatory
  owner/source blocks its checkpoint; never guess a sibling cache path.

## Questions and validation design
- What invariant can fail, on which boundary, with what impact? Map requirement
  to microtask, test level, owner and exact evidence. Cover success and rejection,
  recovery, regression and concurrency where triggered, not a test-count target.
- Which checks need real DB/provider/browser behavior? Mark fixture-only claims.
  Use the existing test framework; avoid rewriting its runner or inflating unit
  tests that mirror implementation without checking observable behavior.
- Is the failure reproducible? Record baseline, input, environment/version and
  oracle. Classify flakes and tooling failures before claiming a product bug.
- Which sensitive data/trust boundaries/dependencies changed? Route controls
  and advisories to Security; scanner absence/PASS cannot prove security.
- For advisories, identify package ecosystem, exact resolved version, affected
  range, reachability and mitigation; never infer safety from a package name.
- What artifact is deployed and how is provenance established? Reuse existing
  CI, least privilege, protected secrets and release gates. Configuration is not
  evidence that a required check actually ran or is enforced remotely.
- For releases define compatibility, health checks, rollout/rollback conditions
  and responsible human. For backups define approved RPO/RTO and execute restore
  verification in an isolated target; a backup job success alone proves no restore.
- Derive logs, metrics and traces from actual failure detection and debugging
  needs. Specify redaction, correlation, retention, ownership and alert response.
  Never invent numerical SLOs, recovery guarantees or business acceptance.

## Verification and gate outcome
Put executable commands, expected results, artifact/revision and limitations
in the existing Task and receipts. Independent owners validate their sectors;
Harness reconciles current evidence. PENDING, PARTIAL, BLOCKED and NOT_VALIDATED
do not close REQUIRED gates. Human approval and separately authorized deploy
remain intact. This checklist is LOCAL DECISION SUPPORT, not proof of execution.

## Primary source pointers
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OSV](https://osv.dev/)
- [NIST SSDF 1.1, SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

ASVS, SSDF and OpenTelemetry pointers checked 2026-10-11. OSV reuses the
repository's already documented advisory source; an actual lookup is required
per dependency/version. These references guide controls/telemetry, not a claim
of certification, regulatory compliance or an executed security scan.
