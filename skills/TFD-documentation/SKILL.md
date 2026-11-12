---
name: TFD-documentation
description: "Write internal docs and user help from verified, human-reviewed module behavior."
metadata:
  version: "1.1.1"
  owner: "documentation"
---

# documentation

Explain public contracts, nonobvious intent, operating steps and observed limits. Link project ADRs and reusable sources instead of copying manuals; keep examples aligned with the verified revision and omit redundant inline commentary.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

For a project that adopts the [phase-based delivery board](../../docs/delivery-board.md), start after G8-review local acceptance and follow its in-product access and QA rules. Otherwise, start after QA and human review of the PR and local behavior. Document the exact reviewed revision. Keep technical architecture, operations and troubleshooting in project docs. Write user-facing tutorials for verified flows, fields, roles, errors and limits. Use only relevant library templates. Cite observed behavior and label untested cases. Use versioned tutorials as the source of requested in-product help.
