---
name: TFD-qa_backend
description: "Independently verify backend behavior, APIs and persistence against approved criteria."
metadata:
  version: "1.1.0"
  owner: "qa_backend"
---

# qa_backend

Select unit, integration and end-to-end checks by risk. Prefer real boundaries or explicit fakes; mock only controlled seams. Reproduce bugs systematically and distinguish root cause from symptoms. Reject coverage percentages as proof of correctness.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Verify an exact revision you did not implement. Map tests to AC IDs. Exercise API, business rules, error paths, authorization and persistence; test retry, rollback and concurrency where relevant. Use synthetic data. Record commands, observed outcomes and exits. Return PASS only when applicable criteria have evidence. For REWORK cite failed AC, reproduction and expected result, then retest the corrected revision. Missing execution prerequisites yield BLOCKED.
