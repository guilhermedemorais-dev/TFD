# Bug reproduction and fix verification

Read when a reported/candidate bug needs reproduction, rework or fix validation.
Use the approved spec as expected behavior and capture the actual affected
revision/environment. Do not guess a cause when evidence does not isolate it.

## Disposition

| Status | Evidence threshold |
| --- | --- |
| CANDIDATE | Suspicion or failure not yet reproduced/classified |
| CONFIRMED | Reproduced actual/expected mismatch with the fields below; equivalently CONFIRMED_BUG, not a security finding |
| NOT_REPRODUCED | Attempts/conditions recorded without reproducing; not proof the issue is absent and not authorization to invent a fix |
| FIXED | FIXED requires QA retest at the fixed revision plus relevant regression evidence |
| ACCEPTED | Recorded authorized decision accepts identified residual impact, owner and rationale; not FIXED |
| DEFERRED | Recorded authorized decision postpones work with owner/follow-up; not FIXED |

Severity is functional/business impact: BLOCKER prevents the required flow or
risks unacceptable loss; HIGH seriously affects core use/data with poor recovery;
MEDIUM has bounded impact/workaround; LOW is minor. Consider frequency, affected
scope, user blockage, corruption/loss and recoverability. Separate severity
from confidence and reproducibility. Do not assign security severity/CVEs.

## Minimal bug report

```text
ID / Title:
Status: CANDIDATE | CONFIRMED | NOT_REPRODUCED | FIXED | ACCEPTED | DEFERRED
Severity / business rationale:
Reproducibility: attempts / observed failures / conditions
Confidence: evidence strength and uncertainty
Affected revision:
Environment: relevant versions, configuration and synthetic fixture
Preconditions:
Reproduction steps:
Expected behavior: source/acceptance criterion
Actual behavior:
Evidence: sanitized command/exit code, trace or artifact pointer
Impact:
Potential responsible area / owner:
Recommended regression test:
Retest status: NOT_VALIDATED | failed | passed
Fixed revision and retest/regression evidence:
Authorized acceptance/deferral decision: only when applicable
```

CONFIRMED requires Expected behavior, Actual behavior, Reproduction steps,
Environment, Affected revision, Evidence, Impact and Reproducibility/Confidence.
A tool crash or screenshot without those facts is not confirmed reproduction.
Keep sensitive data out of committed/shared evidence; avoid publishing raw logs.

## Handoff and retest

Bug report -> QA reproduction -> CONFIRMED -> regression designed ->
Implementation fix/developer tests -> QA retest -> bounded PASS -> PR gate.

Request REWORK through the Harness with failed criterion and reproducible
evidence. Implementation writes fixes and developer regression tests; QA does
not fix product code while reviewing it. Prefer a regression that fails before
and passes after the fix when technically/economically reasonable. If automation
is not viable, retain manual reproduction/retest evidence and explain why.

For fix-verification, compare exact affected/fixed revisions, repeat original
steps and required adjacent regressions under comparable conditions. A changed
file, developer claim or newly green test alone is insufficient for FIXED.
If the original cannot be reproduced, report the limit honestly; do not fabricate
the before-failure. Missing retest keeps the bug unverified and blocks required
QA completion. ACCEPTED/DEFERRED never silently waive a mandatory gate: a scope
or acceptance change needs the Harness and authorized decision recorded first.

Potential confidentiality/integrity/availability or abuse impact becomes a
SECURITY_CANDIDATE with minimal evidence handed to security-standard. QA may
confirm the functional mismatch, but Security validates/classifies the security
claim and its publication gate separately.
