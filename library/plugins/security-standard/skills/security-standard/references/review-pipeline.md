# Security Review Pipeline

This pipeline separates discovery from judgment so plausible candidates do not
become findings through repetition or scanner confidence alone.

## Phase 0: Intake And Authorization

Required outputs:

- exact repository, revision, path, or diff scope
- authorization and permitted environments
- source-of-truth documents
- risk classification
- prohibited or destructive actions
- expected report destination

Gate: scope and authority are explicit.

## Phase 1: System And Attack-Surface Map

Map deployed components, identities, trust boundaries, external integrations,
data classes, privileged actions, and security controls. Link each relevant
surface to files, routes, jobs, infrastructure, or configuration.

Gate: every high-risk surface has an owner or an explicit exclusion.

## Phase 2: Control Review

Review controls by invariant rather than keyword count:

- identity is established before trust is granted
- authorization is checked against the requested object and current actor
- tenant context cannot be selected or overwritten by untrusted input
- untrusted data cannot alter executable syntax or resource identity
- sensitive data is minimized, protected, and not exposed through secondary channels
- external messages are authenticated, fresh, bounded, and idempotent where required
- privileged effects are observable and recoverable

Gate: controls are traced to enforcement points and negative paths.

## Phase 3: Candidate Discovery

Use manual review and approved tools in parallel when useful. Each candidate
records source, control, effect, assumptions, and missing evidence. Tool output
without a reachable path remains unconfirmed.

Gate: candidates are complete enough for an independent validator to reproduce
the reasoning without relying on the discoverer's conclusion.

## Phase 4: Independent Validation

Challenge each candidate:

- Is attacker control real and reachable?
- Is the relevant control absent or bypassable?
- Does framework/runtime behavior neutralize the path?
- Is the impact security-relevant and correctly bounded?
- Are permissions, deployment configuration, and preconditions realistic?
- Is there a safe local test or deterministic code proof?

The validator may confirm, narrow, defer, or reject. Record counterevidence.

Apply every mandatory item in `false-positive-validation.md`. Validation must
use the detected stack and installed versions from `stack-profiles.md`; a rule
copied from another framework or major version is not evidence.

Gate: every reported vulnerability satisfies the finding evidence contract.

## Phase 4A: Publication Eligibility

Separate internal classification from external tracking. Only `CONFIRMED`
findings with `HIGH` or `MEDIUM` confidence may proceed to vulnerability totals,
release blockers, GitHub/Jira/Linear issues, advisories, or customer-facing
findings.

Gate: evidence contract complete, false-positive checklist passed, revision and
locations reproducible, and duplicates reconciled. All other candidates remain
internal as `NEEDS_VALIDATION`, `FALSE_POSITIVE`, `DEFERRED`, or `BLOCKED`.

## Phase 5: Remediation Design

Define the security invariant, preferred enforcement boundary, compatibility
impact, migration needs, tests, telemetry, rollback, and sibling instances.
Avoid remediations that only hide one payload while preserving the unsafe model.

Gate: the fix addresses root cause and has an objective validation plan.

## Phase 6: Fix And Regression Validation

Apply the smallest complete change. Run focused security tests and the project's
normal regression suite. Prove both malicious rejection and legitimate success.

Gate: evidence shows the original path is closed and expected behavior remains.

## Phase 7: Release Decision

Reconcile findings, deferred surfaces, tool failures, test results, accepted
risks, and rollback readiness. Produce `SECURITY_STATUS`; do not approve on
behalf of the user.

## Parallel Review Rules

Parallelize only independent surfaces or candidates. Assign explicit ownership
and expected evidence. Workers must not edit the same files concurrently.

The coordinator owns:

- scope and threat model consistency
- shared-control analysis
- duplicate and sibling reconciliation
- severity calibration
- coverage ledger closure
- final release status

Independent validation is required for `CRITICAL` findings and recommended for
`HIGH` findings. A second scanner is not independent validation unless its
result is checked against code and runtime evidence.
