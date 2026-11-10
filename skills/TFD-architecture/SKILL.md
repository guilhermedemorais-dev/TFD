---
name: TFD-architecture
description: "Author architecture, contracts, phase plans, and testable specs from approved product scope and Discovery."
metadata:
  version: "1.1.0"
  owner: "architecture"
---

# architecture

Choose boundaries by cohesion, coupling and measurable quality drivers. Compare a simpler existing structure before patterns, layers or distributed services; record the tradeoff in a project ADR. Do not impose every SOLID principle or pattern mechanically.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

## Architecture and specification
- G4: record measurable quality drivers, context and boundaries, C4 views and critical sequences, data and migration, integration contracts, threat controls, deployment and rollback, observability and SLOs, ADRs, executable NFR checks, risks, and traceability. Explain any inapplicable item. Compare viable alternatives before choosing. Use OpenAPI or AsyncAPI where applicable.
- G5: define one task per functional module with ordered phases, dependencies, owners, deliverables, and a three-point estimate per phase. State assumptions, confidence, and measurement basis. Keep scope, exclusions, protected paths, and stop conditions explicit.
- G6: use the [phase spec template](references/phase-spec.md). Define actors, permissions, inputs, transitions, outputs, persistence, errors and concurrency or idempotency when applicable. Link every requirement to approved scope, evidence, a microtask, an acceptance criterion and a test. Use the existing task schema. Treat material unknowns as research gaps.
- Submit the exact spec and matching Discovery revision to QA. Route findings to research or spec, revise, and resubmit. Start implementation after QA PASS and human approval. Leave implementation to its owners.
