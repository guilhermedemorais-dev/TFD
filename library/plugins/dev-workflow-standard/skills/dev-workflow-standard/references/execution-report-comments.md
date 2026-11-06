# Human Execution Report Comments

`EXECUTION_REPORT_COMMENT` is the chronological human summary of a material
execution checkpoint. It is a local Engineering Harness extension, not an
official GitHub, OpenAI, or industry standard.

## Boundaries

- Human Task: persistent technical record.
- Execution Contract v2: LLM-readable normative equivalent of the Human Task.
- `EXECUTION_RECEIPT`: structured evidence that execution occurred.
- `EXECUTION_REPORT_COMMENT`: readable summary published to the linked Issue.
- Project/Board: visual state.
- PR: reviewable delivery.

The comment may summarize facts from the task, receipt, diff, and command
results. It never replaces those sources or proves execution by itself.

## Material Checkpoints

Consider a report for `DISCOVERY_SDD_COMPLETED`, `RUNNING`, `VALIDATING`,
`REWORK`, `BLOCKED`, and `COMPLETED`. Publish only when the state or material
outcome changed. Consolidate small operations and do not publish the same normalized report body twice for the same task and checkpoint.

## Publication Protocol

1. Resolve the real Issue linked from the Human Task or board card.
2. Build a short factual report using the executor template.
3. Compare it with the latest report for the same checkpoint when available.
4. Publish through an available authorized GitHub capability.
5. Treat the report as `PUBLISHED` only with the returned comment URL or identifier;
   record that evidence in the task/receipt.
6. If Issue resolution or publication is unavailable, store the report in the
   Human Task as `NOT PUBLISHED` with the reason. For
   `DISCOVERY_SDD_COMPLETED`, do not advance to Ready for Dev while an available
   linked-Issue publication capability failed; remain in Discovery / SDD and
   report the blocker.
7. Synchronize Project status using existing board rules when a compatible
   linked Project exists. Never attach a task to an unrelated Project.

## Content Rules

Include only applicable sections: status, work completed, method, technical
decisions, reuse, validation, unvalidated areas, problems, blockers, evidence,
out-of-scope items, and next step.

Every material report ends with these audit blocks, in this order after the
next step: changed surface, then token usage as the final data block:

- token usage: `input_tokens`, `output_tokens`, `total_tokens`, and
  `measurement_source`;
- changed surface: `changed_files`, Issue/card changes,
  JSON/spec/reference changes, `remote_mutations`, whether code changed, and
  branch/commit/PR.

Token counts are exact only when returned by the runtime or API. When the
runtime exposes no count, use `NOT_AVAILABLE` for every unavailable value and
the measurement source. Never present an estimate as an exact measurement.

Technical rationale must be concise and verifiable, for example why an existing
service was extended instead of duplicated. Never publish private
chain-of-thought, token-by-token deliberation, secrets, credentials, or
unnecessary internal logs.

For tool preparation, mention whether the tool was already available or was
verified after installation. For validation, report initial findings,
confirmed findings, false positives, correction, and revalidation when useful.
Omit machine-specific executable paths and installation logs.

## State Requirements

- `DISCOVERY_SDD_COMPLETED`: questions and user answers, research and sources,
  consolidated decisions, open hypotheses, card/JSON contract revision,
  normative equivalence status, and the approval requested from the human.

- `REWORK`: failed criterion, evidence, known cause, correction strategy, next step.
- `BLOCKED`: concrete blocker, impact, completed work, stopped work, required
  decision, next safe action.
- `COMPLETED`: actual delivery, method, decisions, validation, remaining risks,
  out-of-scope items, and branch/commit/PR when available. It also requires an
  updated task, completed receipt, validation evidence, and no open blocker.

The Harness must verify consistency among task, receipt, Issue report, Project
state, and PR. A comment is communication, not execution evidence.
