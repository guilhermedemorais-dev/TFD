> Contexto TFD · 576 palavras · 928 tokens (o200k_base)

# Routed execution

Run from the project root. Pass `--project-root` if working elsewhere. Use the canonical `workflow.json` and its submitted `task.json`. `resume_task.py` calls the gate evaluator first and returns the approved constitution and environment paths when present. Read those records and recheck readiness facts that changed. `FOLLOW_GATE` follows the existing gates, including pre-Task G0.5. `LEGACY_TASK_ROUTE` uses the existing manual route. Keep pre-existing approvals and current project restrictions authoritative.

## Dispatch

Use `render_task.py <task.json> --sector <id> --microtask <id>` and the complete active skill. Keep applicable mandatory references and global limits. Carry project-level scope restrictions from the approved constitution into Task `out_of_scope` and `protected_paths`. Keep only the active MT's permitted paths and relevant additional rules in its handoff. For technical gaps, search validated project Discovery and ADR evidence first, then use the decision procedure. Keep external guide content at its source.

For Codex projects using model routing, write a request in project evidence and call `model_router.py select <request.json>`. Bind `task_id`, `contract_revision`, `microtask_id`, `sector`, `complexity`, `capabilities`, `min_context_tokens` and `coordinator_provider`. Supply ordered authorized `profiles` (`id`, `provider`, `model`, `effort`, `complexities`) and current `catalog` rows (`provider`, `model`, `availability`, `capabilities`, `context_tokens`, `efforts`, `launch`, `evidence`). Use actual host inventory and capability evidence. Codex `model/list` shows model IDs and supported efforts. Confirm provider, availability, context and tools separately. Keep unobserved models unavailable. With no routing policy, retain the existing native delegation.

On `SELECTED`, delegate the MT to its assigned role using the selected model and effort. `native` uses the coordinator provider. Use Codex CLI `exec --oss --local-provider` for `codex_oss` or configured `model_provider` for `codex_provider`. Pass model, effort and config as separate arguments. Preserve project permissions and required tools. Role overrides can change the effective model. Run `model_router.py verify <selection.json> <session.jsonl> --thread-id <id> --turn-id <id>` on the delegate's observed run. An equivalent observation JSON binds the same identity and `attempt` to effective `profile`, `provider`, `model`, `effort` and `evidence`. Label absent evidence `UNCONFIRMED`.

If the model fails or QA identifies an evidence-backed model limitation, keep the MT and checkpoint. Append the rejected profile and reason to `attempts` and rerun selection. The coordinator may pass `suggested` with an authorized profile from its provider. Retry within the configured maximum and recheck the changed work independently. `UNAVAILABLE` or `RETRY_LIMIT` leaves the work pending. Begin a new bounded round only after observing changed availability and retain the prior round's receipts. Keep selection, exclusions, observed route and QA verdict for Human Review.

## Checklist and review

For `EXECUTE_ITEM`, plan just that checklist item. Before actions, call `resume_task.py <workflow.json> --record started --microtask <id> --item <n>`. Work and verify in the same agent session where practical. Record only `--record verified --microtask <id> --item <n> --evidence <project-relative-file>` with immutable verification evidence. `RECONCILE_ITEM` means check existing effects before retrying after interruption or fallback. Store no microplan in the Task or its view.

Use `--git-base <reviewed-base> --microtask <id>` on the isolated MT delta before QA. Account separately for project ledger/evidence updates. `PATH_VIOLATION` covers protected paths and changes outside either allowlist. Resolve findings before advancing. This is a diff check, with host permissions still in force.

For `REQUEST_MICROTASK_QA`, record the independent verdict in existing `sector_receipts` with its `attempt` and evidence. On `REWORK_MICROTASK`, use `--record rework --microtask <id>` and correct the failed MT. Reconcile prior effects before replay. Revalidate dependents whose evidence was invalidated. Map gate-level REWORK to affected MT receipts. Submit the gate after all applicable MTs pass. Require phase QA and human approval before advancing.
