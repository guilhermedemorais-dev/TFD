> Contexto TFD · 585 palavras · 974 tokens (o200k_base)

# Gate contract

Keep one workflow JSON/task per module. Ordered `phases` starts empty; fill before G5 with unique `id` and boolean `backend`, `ui`, `security`. `events` records transitions. Database uses backend QA.

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

This table is the legacy protocol. For `stage_loop_version: 1`, use the [stage-loop contract](stage-loop.md): every production stage requires source/self-check receipts and independent QA before acceptance; G2 hands off to G3 and G10 uses authorized terminal completion. G6/G7 carry a `phase` ID; others omit it.

Optional workflow root `preparation` has exactly `mode: "reviewed_task"` and `authorization: "<project-relative file>"`. Require an existing nonempty record of explicit human authorization. Only G2-G5 then permit coordinator `complete`, with nonempty evidence, current revision, all applicable QA PASS and an actor distinct from author/reviewers. Human `approve` remains valid. G0/G0.5/G1/G6/G7/G8-review/G8 stay human; preparation never authorizes implementation, merge or deploy.

Events identify `gate`, `action`, `actor` and unique snapshot `revision`. Keep snapshots stable and cite receipts, commands and exits.

- `submit` includes project-relative `artifacts` and matching `sha256` hashes. At G5, `phase_plan` matches the exact `phases` list. At G6, include `task_id` and `contract_revision` from the canonical JSON. Edit that JSON in place, increment its revision when changed, and refresh its Markdown sibling with `python -B scripts/render_task.py <task.json>`. Update the same GitHub Issue if linked and authorized. Use one active task ID, JSON path, view path and Issue per module. Earlier task hashes and decisions stay in the ledger. Keep other review evidence stable.
- `review` includes `reviewer` (the required sector), `verdict` (PASS, REWORK, or BLOCKED), and `evidence` (project-relative file). Each revision needs fresh reviews. A REWORK permits a replacement submission. After three replacement submissions, another REWORK blocks the stage. For missing prerequisites use BLOCKED and record the reason.
  In reviewed preparation, G6 PASS evidence must validate as the existing findings JSON, with PASS verdict, `artifact` equal to submitted `spec` and matching submission `revision`. Require canonical `task.spec` equal to that path. Other verdicts preserve rework/blocking. Submission hashes bind spec, Discovery, task and generated view.
- `approve` includes `evidence` (record of the user's explicit approval). Submit it only on behalf of the approving human. Actor identifiers support separation of duties and are supplied by the operator; the CLI does not authenticate them.
- `block` includes `evidence` explaining a missing prerequisite and how to unblock it. Use the current revision when a submission exists.

The CLI verifies project-local evidence. BLOCKED stops the affected transition until its prerequisite or human decision is resolved. Publication, merge and deploy require separate authorization.

For new workflows, the [coverage protocol](../../../docs/discovery-coverage.md) requires G3/G6 QA consultation via `review_version: 1`; legacy reviews remain valid.

## Context and run receipts

Measure selected files with `python -B scripts/context_budget.py <files>` and the applicable `--max-tokens`/`--max-total-tokens` limits. Narrow over-budget context. Before hashing, stamp authored Markdown/Python/JS/TS; record other formats in receipts. See [Codex receipts](../../../hosts/codex/README.md).

Report task/gate/attempt checks/exits, passed/executed, blocked/skipped, status, estimates, observed usage and evidence. Separate reviewer runs; missing counters stay unavailable. Estimates/quota never prove tests.

For routed tasks, use [sector routing and receipts](../../../docs/sector-task.md).
