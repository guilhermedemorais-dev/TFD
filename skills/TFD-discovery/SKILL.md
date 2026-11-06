---
name: TFD-discovery
description: "Investigate gaps in an approved PRD using indexed sources. Produce traceable findings for the spec. Use for Discovery or research rework requested by spec QA."
metadata:
  version: "1.5.0"
  owner: "discovery"
---

# Discovery

1. Derive spec questions and project type (web, mobile, desktop, or other) from the approved PRD and project evidence. Ask if the type is unclear and affects research.
2. Start with the [TFD library index](../../library/indexes/resources.json). Resolve paths under the plugin's `library/`. Open only relevant resources and reuse compatible project `docs/` evidence. Keep origin, version, section, and purpose.
   If reverse engineering could answer a question, ask whether to use REA and which compatible variant the user authorizes for that project type. Confirm the target and scope. Use reference software only if the user identifies it. Call only the authorized variant on the authorized target. While approval, target, or capability is missing, continue independent research.
3. Report an inaccessible index path. For insufficient evidence, tell the user the open question, sources checked, and affected decision. Mark essential gaps `BLOCKED` and other gaps `UNKNOWN`.
4. Resume with a user-supplied source or requested research. For technical docs, try Context7 first, then official docs directly as needed. Record consulted, verified sources in project `docs/`.
5. Write sources, evidence, and findings to `docs/discovery/` using the [output contract](references/evidence-format.md). Run `python <skill-dir>/scripts/check_evidence.py <sources.json> <evidence.json>`.
   For authorized analysis, record the target, revision, and evidence limits.
6. Hand off findings to the spec author. QA reviews matching Discovery and spec revisions together. For research rework, revisit the flagged question, update evidence, and send the affected spec for correction and joint review. Production requires QA `PASS` and human approval.

Discovery gathers evidence. Leave architecture, implementation, and task approval to later stages.
