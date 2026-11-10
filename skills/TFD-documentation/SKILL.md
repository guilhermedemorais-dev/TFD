---
name: TFD-documentation
description: "Write internal docs and user help from verified, human-reviewed module behavior."
metadata:
  version: "1.1.0"
  owner: "documentation"
---

# documentation

Explain public contracts, nonobvious intent, operating steps and observed limits. Link project ADRs and reusable sources instead of copying manuals; keep examples aligned with the verified revision and omit redundant inline commentary.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

After QA and human review of the PR and local behavior, document the exact reviewed revision. Keep technical architecture, operations and troubleshooting in project docs. Write user-facing tutorials for verified flows, fields, roles, errors and limits. Use only relevant library templates. Cite observed behavior and label untested cases. Add in-product help only when requested, using the versioned tutorial as source.
