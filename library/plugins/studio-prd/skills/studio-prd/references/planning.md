# Internal plan and supervised handoff

The PRD links the plan; do not bury scheduling in the PRD. MD is an internal
developer document, not a commercial proposal. JSON expresses the same decisions
for agents and never replaces the module's execution contract. One `revision`
identifies both. Keep actual progress as evidence, not silent normative edits.

## Contents

Adapt `assets/plan-template.json` after briefing. All template modules are drafts,
not approved real tasks. Preserve stable module/task IDs and record:

- stages, outcomes, module/task mappings, state found and proposed treatment;
- capability-level dependencies and why they precede another module;
- urgency, desired date, impact, feasible options and the approved priority;
- distinct specification, execution and integration order when needed;
- entry/exit conditions, deliverables, blockers, risks, resources/costs if known;
- effort-hour ranges separate from calendar-day ranges, capacity, external waits,
  assumptions, confidence and total projection; actual effort when measured;
- decision/change log with impact and one short contextual prompt per task.

Estimate QA, integration, risk/rework reserve, migration and operations when
applicable. Use `null` for unknown effort, duration, capacity or costs; do not
turn unknown into zero. Estimates are preliminary until supported by evidence.
Total elapsed duration is not a blind sum when work overlaps. More parallel
chats are not assumed to multiply capacity. Parallel groups require independent
work and no shared-file/integration conflicts; the user chooses whether to run
them. Reprioritization changes plan revision and cannot waive prerequisites.

## Helper and equivalence

Resolve `scripts/plan.py` relative to this skill, in a source checkout or the
actual installed bundle. It uses only Python's standard library:

```text
python3 <skill>/scripts/plan.py validate <project>/docs/planejamento/plano-de-execucao.json
python3 <skill>/scripts/plan.py render <project>/docs/planejamento/plano-de-execucao.json
python3 <skill>/scripts/plan.py check <project>/docs/planejamento/plano-de-execucao.json <project>/docs/planejamento/plano-de-execucao.md
```

`render` prints a human Markdown plan without writing files or contacting any
service. Save its exact output with the host's approved file-edit method.
The bundled [Markdown template](../assets/plan-template.md) is that same rendered
draft. Source paths in JSON are project-root relative, absolute, or HTTP(S)
URLs. Relative prompt links are rendered for `docs/planejamento/`; when adopting
a different plan directory, use absolute/versioned links to avoid broken routes.
`check` detects drift anywhere, including revision, sequence, assumptions and
prompts. Make changes in JSON and regenerate MD, or reconcile human MD edits
back into JSON before regenerating. Do not discard user edits blindly.
The helper checks required fields, estimates, unique mappings, dependency order
and stage coverage. It does **not** verify business completeness, existing
files/URLs, approvals or estimate accuracy; the specialist does those checks.

## Short prompt, not a new execution protocol

Each module carries 2–3 brief, specific `prompt.notes` from its approved context.
Do not repeat generic policy lists. `prompt.mode = specification` when the task
contract is absent: ask SDD to specify this module, explicitly not implement it.
Leave unknown task/contract links `null`, never invent a URL. `execution` requires
the actual task link and contract path plus observed approval through Harness;
the generated prompt still requires checking the task's current stage/gates.
Read task, contract, brief and PRD links before claiming they resolve.
Existing per-list execution prompts remain in the task contract, not duplicated
here. Opening a separate Codex chat is the user's action.

## Gates

1. Brief/PRD/module inventory/priority review by user, proposals distinguished.
2. Announce module count and first module; ask to start its specification.
3. SDD researches and specifies that module using the canonical task template,
   equivalent JSON, references, sector owners and all applicable validations.
4. Discuss material gaps while the user supervises; issue a completion report
   with coverage, pending decisions and measured tokens or NOT_AVAILABLE.
5. Await approval before advancing to the next module. Spec completion and
   PRD approval are not implementation, merge, deploy or final acceptance.
