---
name: TFD-harness
description: "Coordinate TFD gates, revisions, evidence, scoped rework, and human approval. Use to start, resume, or hand off a module task."
metadata:
  version: "1.3.0"
  owner: "harness"
---

# TFD harness

1. Read the [gate contract](references/gates.md). Identify the active module and phase. Give each sector its scope, exclusions, expected artifacts and acceptance checks. Load only the relevant skill and library resources.
   Before delegating a user instruction, use [Translator](../tfd-translator/SKILL.md) with the active sector and current IDs. If it returns `CLARIFY`, ask the user. Pass a `READY` handoff with the sector's canonical task context. When delegation is unavailable, apply the same translation rules in the harness and record the fallback.
2. Keep a project-local workflow log and run `python <tfd-root>/scripts/pipeline.py <workflow.json>` before advancing. Record observed outputs and reviewer verdicts for the exact submitted revision. Keep the user's explicit decision as evidence for approval.
3. At G6, QA reviews the spec and matching Discovery. At G7, applicable backend and UI QA independently review the current implementation. If QA returns REWORK, send the failed evidence and scope to the author and require review of the replacement revision. Stop after three failed rework attempts.
4. Present each stage's scope, deliverables, commands, exits, and limits for human approval. Keep a local review packet separate from an observed PR. Publish, merge, or deploy only with separate authorization. After QA and human verification, route documentation to its owner.
   Before each final TFD response, use [Token Usage](../tfd-token-usage/SKILL.md) and append its measured usage line.

Keep product edits with their owners. A missing tool, evidence, or approval blocks the affected transition.

For a confirmed harness incident, report evidence and offer a separate Oficina maintenance session. Use the installed `oficina-tfd` skill for explicit TFD maintenance outside client execution. A client incident never authorizes a repair.
