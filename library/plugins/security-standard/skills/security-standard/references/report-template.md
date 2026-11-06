# Security Review: <scope>

## Executive Decision

- Date:
- Revision/baseline:
- Mode:
- Risk level:
- `SECURITY_STATUS`:
- Release blockers:
- Human decision required:

## Authorization And Scope

- Authorized target:
- Included:
- Excluded:
- Environments used:
- Prohibited actions:
- Source-of-truth documents:

## System And Threat Summary

- Protected assets:
- Actors and privileges:
- Trust/tenant boundaries:
- Primary entry points:
- High-impact effects:
- Key assumptions:

## Coverage

Include the coverage ledger from `coverage-model.md` and summarize:

- Banco:
- API/Backend:
- Frontend/UI:
- Infra/DevOps:
- Dependencias/Supply Chain:
- Privacidade/Observabilidade:

## Findings

### SEC-YYYY-NNN: <title>

- Status:
- Severity:
- Confidence:
- Layer/owner:
- Affected locations:
- Boundary and source:
- Attack/data path:
- Missing or bypassed control:
- Preconditions:
- Impact:
- Counterevidence checked:
- Safe reproduction/evidence:
- Recommended remediation:
- Regression tests:
- Residual risk:

## Rejected Candidates

Record candidates rejected as false positives and the exact counterevidence.

| Candidate | Trigger | Counterevidence | Disposition | Validation owner |
| --- | --- | --- | --- | --- |

## Validation Backlog

List `NEEDS_VALIDATION`, `DEFERRED`, and `BLOCKED` candidates separately. These
items are not confirmed vulnerabilities, do not enter confirmed severity totals,
and are not eligible for automatic external issue creation.

| Candidate | Missing evidence | Confidence | Next validation action | Owner |
| --- | --- | --- | --- | --- |

## Fixes And Validation

| Finding | Fix | Tests | Legitimate behavior | Security behavior | Result |
| --- | --- | --- | --- | --- | --- |

## Tooling

| Tool | Version/config | Scope | Result | Failure/blind spot |
| --- | --- | --- | --- | --- |

## Deferred Work And Blind Spots

| Item | Assurance impact | Reason | Owner | Required action |
| --- | --- | --- | --- | --- |

## Release Gate

- `QA_STATUS`:
- `SECURITY_STATUS`:
- Rollback readiness:
- Accepted risks and approver:
- Recommendation for human review:

This report provides technical evidence and does not replace human approval.
