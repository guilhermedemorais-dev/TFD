# Gate contract

Keep one workflow JSON per module in project docs. The root has `phases` (ordered list of objects with unique `id` and boolean `backend`, `ui`, `security`) and `events`. Start with an empty phase list and fill it before G5 submission. Mark applicability from the phase plan. Database work uses backend QA. Use one task contract per module.

| Gate | Submission artifacts | Required review |
|---|---|---|
| G0 | constitution | human approval |
| G0.5 | environment | human approval |
| G1 | briefing, prd | human approval |
| G2 | sources, evidence, findings | human approval |
| G3 | findings | qa_spec |
| G4 | architecture, contracts | qa_spec |
| G5 | phase_plan, estimates | human approval |
| G6 per phase | spec, discovery, task, task_view | qa_spec |
| G7 per phase | implementation, self_tests | applicable qa_backend, qa_ui, security |
| G8-review | review_packet, local_verification | human approval |
| G8 | technical_docs, user_help | final human approval |

All gates require a human approval after applicable reviews. G6 and G7 carry a `phase` ID. For all other gates omit `phase`.

Each event identifies `gate`, `action`, `actor`, and `revision`. Revision is the unique submitted snapshot identifier. Keep snapshots stable and cite actual receipts, commands, exit codes and reviewed revisions. Use these actions:

- `submit` includes project-relative `artifacts` and matching `sha256` hashes. At G5, `phase_plan` matches the exact `phases` list. At G6, include `task_id` and `contract_revision` from the canonical JSON. Edit that JSON in place, increment its revision when changed, and refresh its Markdown sibling with `python -B scripts/render_task.py <task.json>`. Update the same GitHub Issue if linked and authorized. Use one active task ID, JSON path, view path and Issue per module. Earlier task hashes and decisions stay in the ledger. Keep other review evidence stable.
- `review` includes `reviewer` (the required sector), `verdict` (PASS, REWORK, or BLOCKED), and `evidence` (project-relative file). Each revision needs fresh reviews. A REWORK permits a replacement submission. After three replacement submissions, another REWORK blocks the stage. For missing prerequisites use BLOCKED and record the reason.
- `approve` includes `evidence` (record of the user's explicit approval). Submit it only on behalf of the approving human. Actor identifiers support separation of duties and are supplied by the operator; the CLI does not authenticate them.
- `block` includes `evidence` explaining a missing prerequisite and how to unblock it. Use the current revision when a submission exists.

The CLI evaluates the log and verifies referenced files are inside the project. It does not dispatch agents or publish changes. For BLOCKED, stop and resolve the prerequisite or get a human decision before restarting the affected stage. Keep remote publication, merge and deploy separate.

## Context and run receipts

Before loading selected local PRDs, stack notes, references or code, run `python -B scripts/context_budget.py <files>`. Apply the per-reference or project limit with `--max-tokens` and the allocated context with `--max-total-tokens`. Select narrower sources if over budget. Before handoff, stamp authored Markdown, Python, JS or TS in place, then hash them. Record counts for other formats in the receipt. See [Codex receipts](../../../hosts/codex/README.md).

Record one row per task, gate and attempt in the final report. Include approved and failed checks, score as passed/total executed, blocked/skipped checks separately, status, estimated source words/tokens, observed input/output/total tokens and evidence. Use unavailable for missing counters and no score when no check ran. Include separate reviewer runs. Token estimates and quota never replace test evidence.

For routed tasks, use [sector routing and receipts](../../../docs/sector-task.md).
