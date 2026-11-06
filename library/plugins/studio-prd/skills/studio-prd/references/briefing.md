# Interview and authorized inventory

Use these topics as a coverage map, not a fixed questionnaire. Start with
available project evidence; ask up to three unresolved business decisions per
round with alternatives and a recommendation where useful.

1. Business problem, intended outcome, production scope and exclusions.
2. Actors and external systems: goals, responsibilities, permissions and data
   visibility. Reuse approved identity/RBAC/platform decisions.
3. End-to-end journeys across modules: trigger, preconditions, main path,
   alternatives, failures, recovery and observable result for each actor.
4. Shared entities, ownership, lifecycles, invariants, cross-module interfaces.
5. Professional capabilities where relevant: audit, filters/search, pagination,
   import/export, notifications, accessibility, recovery, privacy and operation.
   Present missing capabilities as proposals with purpose, not automatic scope.
6. Functional/visual references, source rights/access, reuse and evidence gaps.
7. Complete module inventory, urgency reason/deadline/impact, dependencies.
8. Working capacity, external waiting, resources, risks, estimate confidence.

For existing software, first inventory supplied app/code/data/docs/integrations.
For each capability record evidence path + revision, observed coverage, limits
and one recommendation: MAINTAIN, COMPLETE, FIX, REFACTOR, REPLACE or RETIRE.
Separate visible interface, code found and tested behavior. Include missing
access as UNKNOWN. RETIRE is a recommendation, never permission to remove data.
Do not execute downloaded code or connect production services merely to inspect.

Research reference implementations beyond README: relevant implementation,
schemas/migrations, API contracts, examples and tests. A screenshot/scrape cannot
establish hidden rules or full backend behavior. Save a concise source record in
the project library and cross-check contradictions before making a requirement.

Each decision has ID, status (APPROVED/PROPOSED/UNKNOWN/EXCLUDED), source, rationale
and impact. Ask when a gap changes scope, business rules, urgency feasibility or
acceptance. Technical details derivable from approved context can be researched
and proposed without repeatedly asking the user to write the specification.


## Critical discovery: phases and proportional gates

These phases belong to Studio product discovery, not SDD's module-spec phases.
Reuse existing context; do not reopen approved decisions without new evidence.
For a bounded existing change assess only the affected gap. Ask preferably one
critical question, up to three independent questions when useful. No obligatory
questionnaire, research quota, document per reply or adversarial performance.

- **Fase 0 — Diagnóstico:** state what is clear, missing, assumed and risky;
  prioritize questions by business/scope/acceptance impact. Establish the problem,
  actors and desired outcome before endorsing the suggested implementation.
- **Fase 1 — Debate e consolidação:** compare alternatives against constraints,
  user outcomes, success indicators, dependencies and maintenance/operational
  cost. Recommend simpler options, deferral or removal when supported; removal
  remains a proposal. Surface contradictory requirements and their consequences.
  Confirm included/excluded scope, business rules and material open decisions.
- **Fase 2 — Consolidação do PRD:** update the existing canonical PRD/brief/plan;
  keep source-to-requirement-to-acceptance traceability, alternatives and decision
  rationale. Present DRAFT/IN_REVIEW and actual unresolved blockers to the owner.
  Only observed human approval establishes approval. Do not auto-advance to SDD
  or implementation, and do not declare critical blocked discovery complete.

A draft may contain explicit unknowns. Block only a dependent conclusion when a
missing fact/decision affects scope, business invariants, feasibility, security
or acceptance; continue independent work. Nonmaterial details are not grounds
for endless interviewing. Do not require every implementation detail to approve
product intent; hand unresolved technical design to Architecture/SDD explicitly.

## Evidence-based technical debate

For each material technical recommendation:

1. Inspect the approved brief/PRD/decisions and relevant code, tests, versions and
   constraints. Separate observed implementation from desired product behavior.
2. Reuse current project records and relevant catalog metadata. If evidence is
   missing, stale, version-incompatible or the claim could have changed, consult
   original vendor/framework docs or primary protocol/security standards. Check
   publication/version and applicability. Community examples are secondary and
   need source verification; popularity and model memory are not validation.
3. Record a concise claim/source link or project path, version/commit or UNKNOWN,
   consulted section/date, what it supports, applicability and limits in the
   existing project reference library. Cite it near the recommendation. Links
   never fetched/read are candidates, not consulted evidence. Do not invent quotes.
4. Compare meaningful compatible alternatives, including current implementation
   or a smaller solution. Explain trade-offs in requirements, cost/resources,
   security, operations, reversibility and user impact where applicable. Distinguish
   sourced facts from your inference and LOCAL DECISION. No stack/service/Redis/
   container is introduced just because an external guide uses it.
5. State uncertainty and a way to resolve it. If a required source is unavailable,
   mark the claim NOT_VALIDATED and continue unrelated discovery. Do not install,
   benchmark, execute downloaded code or contact production to resolve it here;
   propose a separately authorized spike/test or specialist review instead.

Use two independent dimensions in existing decision/reference tables:
**kind** FACT/HYPOTHESIS/PREFERENCE/DECISION, and existing approval state
APPROVED/PROPOSED/UNKNOWN/EXCLUDED. An owner-approved hypothesis remains a
hypothesis until evidence validates it. A business preference cannot establish
runtime feasibility. Revisit a decision only on changed requirements or concrete
new evidence, preserving the original ID, reason and impact in the existing log.
No parallel memory, database or new execution JSON schema.

## Preliminary impact triage, not implementation design

When relevant, keep three visible dimensions in the brief/PRD; otherwise use a
short N/A reason. Scale depth to idea maturity and risk:

| Area | Conceptual questions | Detailed owner |
| --- | --- | --- |
| Banco de dados | Entities/relationships, ownership, consistency, migration compatibility, privacy/retention | Architecture/Data/SDD |
| API / Backend | Business rules, integration boundaries, authz, concurrency, failure/dependencies and plausible scale | Architecture/Backend/Security/SDD |
| Frontend / UI | User journeys, role permissions, loading/empty/error/success states, accessibility/responsiveness and UX consistency | UX/Frontend/SDD |

Record required qualities as scenarios/observable outcomes; do not invent numeric
latency, capacity or retention targets. Route detailed schemas, endpoints,
components and deployment topology to owners. SDD consumes approved product
context and asks only newly exposed module gaps; it does not repeat this debate.

## Method sources and limits

Consulted 2026-10-21: CMU SEI, Quality Attribute Workshops, Third Edition (2003),
https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/ :
early stakeholder quality scenarios before architecture. NN/g, Discovery in Agile
(2023), https://www.nngroup.com/articles/discovery-in-agile/ : targeted questions
and assumptions rather than exhaustive discovery. These inform this LOCAL phase
adaptation, not a claim of QAW certification or universal workflow. They do not
replace version-matched technical documentation for the chosen project stack.
