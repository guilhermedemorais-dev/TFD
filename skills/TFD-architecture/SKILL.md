---
name: TFD-architecture
description: "Author architecture, contracts, phase plans, and testable specs from approved product scope and Discovery."
metadata:
  version: "1.2.0"
  owner: "architecture"
---

# architecture

Choose boundaries by cohesion, coupling and measurable quality drivers. Compare a simpler existing structure before patterns, layers or distributed services; record the tradeoff in a project ADR. Do not impose every SOLID principle or pattern mechanically.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

## Architecture and specification
- Before G4, require independent G3 coverage PASS for the current Discovery revision. Read the [coverage handoff](../../docs/discovery-coverage.md). Resolve technical gaps through targeted research and the affected specialist; return only unanswered business or scope decisions to Product. Produce the spec and complete task autonomously within approved scope.
- G4: record measurable quality drivers, context and boundaries, C4 views and critical sequences, data and migration, integration contracts, threat controls, deployment and rollback, observability and SLOs, ADRs, executable NFR checks, risks, and traceability. Explain any inapplicable item. Compare viable alternatives before choosing. Use OpenAPI or AsyncAPI where applicable.
- G5: define one task per functional module with ordered phases, dependencies, owners, deliverables, and a three-point estimate per phase. Use coverage version 1 and the [covered task example](../../examples/task-coverage.example.json) for new tasks. Link applicable technical areas, business rules, references, microtasks and acceptance tests. Justify N/A. State assumptions, confidence, and measurement basis. Keep scope, exclusions, protected paths, and stop conditions explicit.
- G6: use the [phase spec template](references/phase-spec.md). Define actors, permissions, inputs, transitions, outputs, persistence, errors and concurrency or idempotency when applicable. Link every requirement to approved scope, evidence, a microtask, an acceptance criterion and a test. Use the existing task schema. Treat material unknowns as research gaps.
- Submit the exact spec and matching Discovery revision to QA. Route findings to research or spec, revise, and resubmit. Start implementation after QA PASS and human approval. Leave implementation to its owners.
