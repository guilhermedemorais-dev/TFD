# Engineering Harness Execution Contract

This reference defines how `dev-workflow-standard` turns an approved plan into
verified execution.

## Execution States

Use exactly these states for each delegated checkpoint:

- `PENDING`: task exists but prerequisites are incomplete.
- `READY`: task contract, specs, scope and capability are resolved.
- `RUNNING`: the selected capability has actually been invoked.
- `VALIDATING`: execution returned and evidence is being checked.
- `REWORK`: execution ran but validation failed and correction is required.
- `BLOCKED`: no safe capable path can continue without user input or an external dependency.
- `COMPLETED`: execution evidence exists and all required validation passed.

Do not use `ASSIGNED` as a completion state.

## Mandatory Execution Loop

For new v2 tasks, finish collaborative Discovery/SDD and publish
`DISCOVERY_SDD_COMPLETED` with a returned comment identifier before seeking
human approval for Ready for Dev. This is a reporting checkpoint, not another
execution state. Harness verifies full card/JSON normative equivalence and
records the revision and Issue update time in its existing receipt. Specialists
check their routed slices against that current comparison evidence.
At this same checkpoint, require SDD's current spec consistency result under
its `references/spec-consistency-analysis.md`: requirement-to-microtask/list
coverage, actions without approved intent, ambiguities and contradictions.
Unresolved blocking findings prevent readiness; missing analysis returns to
SDD. Do not create another workflow state or duplicate the downstream QA loop.
Every material comment ends with changed surface and runtime/API token usage,
using NOT_AVAILABLE for measurements the runtime does not expose.

For every executable checkpoint:

1. Confirm task/spec/source-of-truth prerequisites.
2. Resolve the required capability via `capability-registry.md`.
3. Resolve the owner skill before selecting any provider/model. For executor
   runtimes follow `provider-routing.md`, verify configuration separately from
   availability, and record the provider/model choice.
4. Verify the preferred capability is available in the current runtime. After
   required sources are loaded, use `context-retrieval.md` only when additional
   bounded context materially helps the checkpoint.
5. Invoke the capability. Naming it, planning for it, or drafting a prompt is not invocation.
6. Set `RUNNING` and execute the bounded checkpoint.
7. Inspect the returned output, diff, files, commands, artifacts or specialist findings.
8. Complete an `EXECUTION_RECEIPT` from that observed result.
9. Update the Human Task and, for a material checkpoint, follow
   `execution-report-comments.md` to publish an `EXECUTION_REPORT_COMMENT` when
   a linked Issue and authorized capability exist.
10. Set `VALIDATING` and check acceptance criteria and mandatory specialist rules.
11. If validation passes, mark `COMPLETED` and publish the final factual report.
12. If validation fails, mark `REWORK`, report the failure and correction plan,
   and invoke the responsible capability again.
13. If the capability fails or becomes unavailable, select an approved fallback or create an `EXECUTION_HANDOFF`.
14. Mark `BLOCKED` only when no safe capable path remains, with an actionable report.

## EXECUTION_RECEIPT

Every invoked capability must return or be represented by this evidence. The
receipt may be opened while state is `RUNNING`, but it is not complete until the
execution result and command evidence have been observed:

```text
EXECUTION_RECEIPT
- task_id:
- sector: routed sector ID, when applicable
- phase: planning | validation
- revision: tested revision/artifact
- capability:
- provider_or_runtime:
- model:
- executor:
- state: RUNNING | VALIDATING | REWORK | BLOCKED | COMPLETED
- invocation_evidence:
- inputs_used:
- sources_loaded: paths and purposes
- conditional_sources_loaded: paths, conditions and activation evidence
- validation_scope:
- outputs_produced:
- changed_files_or_artifacts:
- commands_and_results:
- validation_evidence:
- tool_evidence: skill, capability, planned/used tool, official repository,
  version, cached/detected/installed state source, installation performed,
  initial result, findings, corrections, final result, and revalidation
- blockers:
- next_safe_action:
```

A task without `invocation_evidence` is `NOT EXECUTED`.

A task without `validation_evidence` cannot be `COMPLETED`.

An Issue comment without a completed receipt is communication, not execution
evidence. A prepared comment without a returned remote URL/identifier is not a
published `EXECUTION_REPORT_COMMENT`.

`EXECUTION_RECEIPT` is a local Engineering Harness extension. It adapts the
consolidated practice of retaining inspectable tool output and validation
evidence; this name and schema are not claimed as an OpenAI or industry standard.

## Invocation Evidence

For DevOps, use this same `EXECUTION_RECEIPT`, not a second receipt type.
Record target_environment, affected revision/artifact, authorized operation,
rollback_strategy (including limits), initial/final validation and health
evidence in its existing inputs/output/validation fields. Tool evidence follows
skill-owned-tools. Config syntax, plan, deploy health and restore are different
claims. Record NOT VALIDATED rather than infer an unexecuted stage. A task or
PR approval alone does not authorize a destructive or production operation.

Valid evidence depends on the capability:

- skill/specialist: canonical `SKILL.md` loaded plus specialist output
- code executor: process/tool invocation plus resulting diff/files
- MCP/plugin/tool: actual tool call plus returned result
- script: command plus exit status/output
- reviewer: concrete findings tied to files/specs/criteria

The orchestrator must not fabricate evidence from intended actions.

## Handoff Contract

Each capability receives only the minimum complete context:

- `task_id`
- `execution_contract_path`
- `sector` and `phase` for routed contracts
- current branch/revision when code is involved
- relevant prior receipts
- relevant prior handoff, when resuming another executor

The Harness reads the complete Human Task; the specialist validates the
contract first and loads its routed microtasks (v2) or task_sections (v1), relevant global acceptance
and constraints, required_sources, activated conditional_sources, necessary
code and dependency_receipts. Follow `context-routing.md`; do not load OPTIONAL
automatically. The active SKILL.md is always read completely. Do not paste those bodies into
the bootstrap prompt. An `EXECUTION_RECEIPT` is produced after execution from
observed evidence; it is never treated as an implementation input for the same
checkpoint. The output of one capability becomes explicit input to the next
only when there is a dependency. Conversation memory alone is not a source of
truth.

For v1 without sectors, Harness resolves a bounded legacy handoff and records
the routing decision; no bulk migration. Missing required references or
source_of_truth_conflict stop the affected checkpoint. Planning completion
does not satisfy final validation dependencies. A material artifact change
requires checking receipt freshness and rerunning affected validations.

## Recovery

When an invocation fails:

1. record the failure in the receipt;
2. classify the failure as capability unavailable, provider unavailable, invalid
   output, validation failure, scope conflict or source-of-truth conflict;
3. retry only when the failure is transient and retrying is safe;
4. otherwise use an approved fallback from the capability registry;
5. if switching executor/provider, create or update `EXECUTION_HANDOFF`;
6. never restart completed work merely because the provider changed.

## Completion Gate

The harness may mark a checkpoint `COMPLETED` only when all are true:

- selected capability actually ran;
- required skill receipts exist;
- expected output exists;
- acceptance criteria were checked;
- mandatory tests/reviews passed or are explicitly marked not applicable;
- no unresolved blocker remains;
- evidence is inspectable from repository/tool state.
- the Human Task is current and any applicable final Issue report is consistent
  with the receipt and validation result.

This checkpoint gate applies to its own scope and phase prerequisites, not to
future sectors that depend on it. Completing implementation enables dependent
QA; it does not declare the complete Task finished.

For final Task completion, every REQUIRED sector must have current owner
evidence and receipts; N/A requires a verified reason. PARTIAL/NOT_VALIDATED
never closes REQUIRED work. Harness reconciles all owners without fabricating
their PASS and issues its own final receipt after reconciliation, preserving
human acceptance gates.
