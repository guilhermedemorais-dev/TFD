---
name: TFD-harness
description: "Coordinate TFD gates, revisions, evidence, scoped rework, and human approval. Use to start, resume, or hand off a module task."
metadata:
  version: "1.5.0"
  owner: "harness"
---

# TFD harness

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md). Send only the routed task slice, global constraints and applicable mandatory references; Graphify ranking never removes a required read. Keep definitions of done, review evidence and technical debt explicit.

1. Read the [gate contract](references/gates.md). Identify the active module and phase. Give each sector its scope, exclusions, expected artifacts and acceptance checks. Load only the relevant skill and library resources.
   Before delegating a user instruction, use [Translator](../tfd-translator/SKILL.md) with the active sector and current IDs. If it returns `CLARIFY`, ask the user. Pass a `READY` handoff with the sector's canonical task context. When delegation is unavailable, apply the same translation rules in the harness and record the fallback.
2. Run `python -B <tfd-root>/scripts/resume_task.py <workflow.json> --project-root <project>` to recover the next gate or implementation item from the ledger. Recheck changed readiness facts. For a routed microtask, use the [execution reference](references/execution.md) for model selection, checkpoints and path verification. Record observed outputs and verdicts for the exact submitted revision. Keep the user's explicit decision as approval evidence.
3. At G6, QA reviews the spec and matching Discovery. At G7, applicable backend and UI QA independently review the current implementation. If QA returns REWORK, send the failed evidence and scope to the author and require review of the replacement revision. Stop after three failed rework attempts.
4. Default to human approval at every gate. With explicit `preparation.mode=reviewed_task` authorization, coordinate `complete` only at G2-G5 after applicable QA, as specified in the gate contract. Keep interactive G1 and human G6/G7/G8 approvals. Present the current task/spec and independent spec QA PASS before task approval, then preserve each implementation stage's self-test → QA → scoped rework → human approval loop. Keep a local review packet separate from an observed PR. Publish, merge, or deploy only with separate authorization. After QA and human verification, route documentation to its owner.
   Before each final TFD response, use [Token Usage](../tfd-token-usage/SKILL.md) and append its measured usage line.

Keep product edits with their owners. A missing tool, evidence, or approval blocks the affected transition.

For a project that adopts the [phase-based delivery board](../../docs/delivery-board.md), use its Status and label rules when coordinating the linked Issue and hand off documentation and release operations at the specified gates.

For a confirmed harness incident, report evidence and offer a separate Oficina maintenance session. Use the installed `oficina-tfd` skill for explicit TFD maintenance outside client execution. A client incident never authorizes a repair.
