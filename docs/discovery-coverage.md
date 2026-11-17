# Discovery coverage and autonomous task preparation

New workflows use `python -B scripts/pipeline.py <workflow.json> --init --project-root <project>`. This creates an empty workflow with `coverage_version: 1` and refuses to overwrite an existing file. The coordinator then records actual project artifacts and decisions. Existing unversioned workflows remain readable. Upgrade an active workflow only with reviewed evidence and fresh QA for the affected transition.

## Before the spec

Discovery writes sources, evidence, findings and a compact coverage matrix under the project's `docs/discovery/`. Follow the [coverage contract](../skills/TFD-discovery/references/coverage.md). Reuse answered business decisions and applicable research. Resolve technical facts through the affected specialist and version-matched sources. Product asks the human only for missing material business or scope decisions.

G2 submits all four artifacts with hashes. G3 submits findings plus the same sources, evidence and coverage. Independent QA compares the inventory against the approved PRD, actual code/tests and sources. It checks every applicable perspective and end-to-end flow. Its PASS receipt uses the existing findings format with `artifact` equal to the coverage path and `revision` equal to the G3 submission revision. The pipeline verifies those bindings and rejects unresolved coverage on PASS. This structural verification complements the reviewer's semantic assessment.

For REWORK, preserve earlier snapshots. Discovery corrects the affected research and G3 resubmits the full revised bundle under a new revision. The existing retry limit applies. G4 and subsequent spec authoring wait for the current independent coverage PASS and the applicable approval or authorized coordinator completion.

## Task and review

Architecture produces the spec and one task per module within approved scope. Use the [covered task example](../examples/task-coverage.example.json) and `python -B scripts/validate_task.py <task.json> --require-coverage`. Legacy tasks keep their original validation and rendering.

Version 1 tasks summarize eight technical areas and link their applicable reference, MT, AC and rule IDs. Every business rule has acceptance coverage. G6 requires the submitted spec path, coverage-aware task, generated view and exact G3-reviewed Discovery coverage. The task's requirement and rule inventories must match the module's reviewed Discovery, including across its implementation phases. Task QA checks contract content and sufficiency. Structural validation alone proves neither implemented behavior nor human approval.

With explicit authorization for reviewed task preparation, the principal records `preparation.mode=reviewed_task` and delegates G2–G5 through the existing Harness loop. It produces and corrects the artifacts autonomously, then presents matching spec/task and independent QA PASS for human G6 approval.

## Context budget

Keep the skill short and load this procedure only for preparation/coverage work. Read the approved module scope, compact matrix and relevant evidence first. Retrieve only the technical sources needed for unresolved questions. Routed microtasks retain their applicable coverage, constraints and mandatory references. Save detailed evidence once in the project and hand off paths/IDs. Recheck changed areas and impacted dependencies while preserving unrelated verified content.
