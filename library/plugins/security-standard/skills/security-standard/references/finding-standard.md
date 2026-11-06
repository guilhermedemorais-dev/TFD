# Finding Standard

## Evidence Contract

A confirmed finding must document:

1. **Boundary:** actor, privilege, tenant, or trust boundary being crossed.
2. **Source:** exact attacker-controlled input or unauthorized authority.
3. **Path:** transformations and calls leading to the effect.
4. **Control:** expected control and why it is absent, misplaced, or bypassable.
5. **Effect:** exact security-sensitive operation or disclosed asset.
6. **Reachability:** route, event, job, UI flow, or deployment path that invokes it.
7. **Preconditions:** authentication, role, configuration, timing, and user interaction.
8. **Impact:** bounded confidentiality, integrity, availability, privacy, or financial consequence.
9. **Counterevidence:** mitigations checked and why they do not close the path.
10. **Reproduction:** safe test, deterministic proof, or explicit reason runtime proof is unavailable.

If a required element is unknown, use `NEEDS_VALIDATION` or `DEFERRED`.

## Confirmation Gate

Treat scanner matches, grep hits, model suspicions, missing headers, old package
versions, and isolated dangerous-looking APIs as `CANDIDATE` evidence only.
Promote a candidate to `CONFIRMED` only after the evidence contract is complete
and the mandatory checklist in `false-positive-validation.md` passes.

Do not publish or externally track unconfirmed candidates as vulnerabilities.
Do not include them in confirmed severity totals or release-blocker counts.

## Finding Identity

Use stable IDs shaped as `SEC-YYYY-NNN`. Keep independently reachable vulnerable
instances separate when they have different entry points, permissions, tenants,
assets, or remediation ownership.

Group findings only when all are true:

- same violated invariant
- same enforcement boundary
- same security impact and preconditions
- one fix and one regression test strategy closes all instances

Never use grouping to hide affected locations.

## Severity Calibration

Severity considers:

- attacker position and required privilege
- exploit reliability and complexity
- required victim interaction
- scope across users, tenants, environments, or records
- sensitivity and recoverability of affected assets
- persistence and detectability
- compensating controls
- business and regulatory consequence

Do not label a finding `CRITICAL` or `HIGH` from a generic weakness category
alone. State why the demonstrated impact meets that level.

## Confidence

- `HIGH`: path and impact reproduced or proven deterministically
- `MEDIUM`: strong code evidence with one material runtime assumption
- `LOW`: plausible candidate with multiple unresolved assumptions

Confirmed findings normally require `HIGH` or `MEDIUM` confidence. Low-confidence
items stay in validation backlog rather than inflating vulnerability counts.

## Status Lifecycle

- `CANDIDATE`
- `NEEDS_VALIDATION`
- `CONFIRMED`
- `FALSE_POSITIVE`
- `FIX_PLANNED`
- `FIXED_PENDING_VERIFICATION`
- `FIXED`
- `ACCEPTED_RISK`
- `DEFERRED`

`FIXED` requires objective regression evidence. `ACCEPTED_RISK` requires human
owner, rationale, expiration/review date, and compensating controls.

## Remediation Quality

Prefer controls that:

- enforce the invariant at the narrowest shared trusted boundary
- fail closed with explicit errors
- preserve valid behavior and compatibility
- are testable and observable
- avoid duplicated policy logic
- cover sibling entry points
- support rollback without reopening the vulnerability silently

Reject fixes based only on blocking one payload string, hiding errors, changing
UI visibility, or trusting client-side checks for server-side authority.
