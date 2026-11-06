# Spec consistency analysis

Refine the existing Discovery/SDD coverage and Human Task/JSON equivalence
checkpoint. SDD owns semantic analysis; Harness verifies its current result
before handoff. Do not add a workflow state, duplicate approval, schema field
or Task. Preserve one complete Task per functional module and its microtasks.

## Inputs and coverage

Read the approved PRD/module slice, applicable specs, Human Task and matching
JSON revision. Reuse existing requirement/rule/acceptance and microtask IDs;
use an exact file/section locator when no ID exists. Do not copy entire sources
into the report or reopen approved decisions without a conflict.

For each approved in-scope obligation, map:

| Requirement/rule | Microtask/list | Acceptance | Planned validation/owner | Source/revision |
| --- | --- | --- | --- | --- |

Map at microtask/list level, not just to the enclosing module Task. Include
non-functional requirements and approved error/negative-path obligations.
Distinguish implementation, integration and validation actions. Documentation,
setup and required specialist reviews may trace to an approved constraint,
dependency or gate instead of a user-facing requirement; they are not orphans.
Exclude proposed, excluded and out-of-scope requirements from the readiness
denominator and identify approved requirements assigned to another module.
Post-launch business outcomes are not executable acceptance unless the needed
measurement/instrumentation is itself approved scope.

## Detection passes

1. **Requirements without microtasks:** find missing implementation or planned
   validation coverage, even when the module already has a Task.
2. **Microtasks without approved intent:** find actions with no requirement,
   constraint, dependency or gate; flag scope additions rather than approving
   them implicitly.
3. **Ambiguities:** identify unmeasurable acceptance, unresolved placeholders,
   unclear actors/permissions, inputs/outputs, conditions, error behavior,
   state transitions and recovery where material to implementation.
4. **Contradictions:** compare business rules, entities, contracts, dependencies,
   pre/postconditions, acceptance and card/JSON revision/content. Include
   conflicting ordering, impossible entry/exit conditions and requirement
   duplication that yields incompatible instructions.

## Result and disposition

Record a compact findings table in the existing discovery report/comment:
finding ID, category, severity, exact source locations, evidence, affected
requirement/microtask and correction or pending decision. Report checked scope,
coverage counts and limitations; zero findings still requires this evidence.
Do not claim semantic equivalence from field presence or keyword matching.

- **CRITICAL:** conflicting mandatory safety/authorization invariant or missing
  coverage that prevents the approved core outcome.
- **HIGH:** conflicting executable instructions, ambiguous material business
  behavior, any approved in-scope obligation missing implementation/action
  coverage or required validation, or unapproved scope addition.
- **MEDIUM/LOW:** non-blocking clarity/maintenance issues with bounded impact.

Block the affected readiness claim on CRITICAL/HIGH findings or unresolved
material decisions. Correct within approved intent; ask the user only for
material choices not already authorized. Update affected normative artifacts
and their shared revision together, then rerun affected checks. Preserve
unrelated content and do not create new Tasks for findings.

Planning coverage is not executed validation PASS. Existing Harness review,
independent QA, Security, UI and rework remain responsible for delivery checks.

## Provenance

This is a local refinement of existing Harness controls, informed by the
[Spec Kit analyze command](https://github.com/github/spec-kit/blob/0443760542e7e5269724744a2ac55c4bd386d095/templates/commands/analyze.md).
The requirement-to-microtask mapping and existing report/revision transport
are project choices. No external command or analyzer is claimed to have run.
