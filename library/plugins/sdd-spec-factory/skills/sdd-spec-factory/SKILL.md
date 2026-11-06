---
name: sdd-spec-factory
description: "Use to turn a client request, feature, idea or problem into spec-driven development artifacts: product, module, page/feature, component, validation, database, API/backend and frontend/UI specs, plus an executable task linked to issue, branch and PR, with code review and QA checklists. Specialist companion to dev-workflow-standard."
---

# SDD Spec Factory

Specialist workflow for **Spec-Driven Development (SDD)**. It converts an idea,
client request, feature or problem into detailed specs and one complete
executable Task per functional module, then hands execution back to `dev-workflow-standard` and the review
specialists. Keep this file lightweight: create only the specs and the task the
current request actually needs, and load the templates on demand.

The LLM using this skill acts as the requirements LLM. Before producing specs,
it must read this `SKILL.md` completely and return a `SKILL_RECEIPT`. Naming the
skill in a prompt is not evidence of activation.

For applicable backend/library, payments, fiscal or commerce needs, consult
[Backend component sources](references/backend-component-sources.md) metadata
before targeted new research. Select eligible free editions only, preserving
license obligations and separate provider/infrastructure costs. This adds
candidates, not dependencies or a stack decision.

When the user/project declares a Next.js/NestJS preference and stack is undecided,
assess that reference pair through existing catalog IDs, then confirm the PRD.
Preserve approved stacks; do not apply this preference to undeclared projects. Next server/BFF adapters may call
Nest-owned domain APIs; do not duplicate business rules or assume Next cannot run backend code.

## Mission

Transform NORMAL work with unspecified behavior and COMPLEX work into, when
applicable:

- product spec (only when the request defines or changes the product itself)
- module spec
- page/feature spec
- component specs
- validation/business rules spec
- database spec (only when there is database impact)
- api/backend spec (only when there is a backend)
- frontend/ui spec (only when there is UI)
- one executable task
- one v2 machine-readable execution contract with normative equivalence to the
  complete GitHub Issue/card for each new executable task
- a PR checklist
- a QA/review checklist

This plugin **does not implement product code**. It produces the contract and the
order of execution. `dev-workflow-standard` orchestrates; implementation is
carried out by `dev-implementation-standard`, reviewed with `security-standard`,
functionally validated with `qa-testing-standard` when required, and visually
validated with `ui-ux-standard`.

## Vocabulary (non-negotiable)

- **Spec is not a PR.** A spec is the contract of what must be built.
- **Task is the order of execution.** Its default unit is a complete functional
  module, with reviewable internal microtasks and end-to-end acceptance.
- **PR is the reviewable delivery.**
- **Issue is the complete human task/card.** A local Markdown may mirror it but
  does not replace it when GitHub Issues is available.
- **Review is approval or rejection.**
- **Deploy only happens after the PR is approved.**

A spec describes intent and acceptance. The Human Task tells people everything
needed to understand and govern the work. The v2 Execution Contract expresses
the same normative content as structured JSON for the LLM. This **normative
equivalence** is deliberate, while runtime status, evidence and discussion stay
in Issue comments and receipts.

## Mandatory hierarchy

For work routed to this skill, respect this top-down order. Do not create every
artifact mechanically: reuse an existing parent or record an explicit,
traceable parent intent when a new product/module/page document would add no
information.

```text
Product Spec
  -> Module Spec
    -> Page/Feature Spec
      -> Component Specs
        -> Human Task
          -> Execution Contract
            -> Branch
            -> Pull Request
              -> Review / QA
                -> Merge / Deploy
```

## Mandatory separation of concerns

Every spec and every task must keep these dimensions visibly separated. Do not
collapse them into one prose blob; if a dimension does not apply, write
"N/A" with a one-line reason.

1. **Banco** (database / data model / migrations)
2. **API/Backend** (endpoints, contracts, services, jobs)
3. **Frontend/UI** (screens, components, states)
4. **Testes** (unit, integration, e2e, what must be covered)
5. **Segurança** (authz/authn, tenant boundaries, secrets, sensitive data)
6. **Observabilidade/logs** (events, metrics, audit trail)
7. **Decisões pendentes** (open decisions waiting for a human)
8. **Riscos** (what can break, regressions, unknowns)
9. **Critérios de aceite** (objective, testable acceptance)

## Operating principles

- The repo, PRD, existing architecture, approved mockups and `AGENTS.md` are the
  source of truth. Inspect the real repo before writing specs.
- Before external research, apply the active Harness capability registry's
  whole-inventory consultation and research routing. Inspect the MCP Library,
  all active specialist tool-registry metadata and actual host tools,
  prefer suitable available documentation/code/extraction/search capabilities,
  and record the reason for generic fallbacks. Reuse existing source records.
- **Do not invent existing architecture.** If you do not know whether a table,
  endpoint, service or component exists, do not assert it. Mark it as a
  hypothesis (`HIPÓTESE:`) or as a pending decision.
- Mark every assumption explicitly. Unverified facts are hypotheses, not specs.
- Generate one complete Task per functional module in the approved demand.
  Decompose large work into internal microtasks and resumable checkpoints,
  never separate Tasks merely by layer, phase or specialist. Size, token budget,
  context limits and review convenience are not exceptions.
- Before specifying a new service, helper, component, route, abstraction or
  subsystem, search the source-of-truth repository for an existing equivalent.
  Prefer reuse or extension and record the decision in `REUSE_INVENTORY`.
- When an unresolved implementation question needs public code examples, read
  [public code discovery](references/public-code-discovery.md). Prefer the
  official Grep service when available; validate candidates at their source.
- Reject speculative abstractions and duplicated responsibilities. New
  abstractions require two current concrete consumers or an explicit approved
  architectural requirement.
- Stop and ask when critical scope is missing. Do not guess core scope.
- Final acceptance belongs to the user.
- Planning depth is selected by `dev-workflow-standard`: TRIVIAL changes remain
  outside full SDD and use an inline intent contract; NORMAL changes use the
  smallest focused spec needed; COMPLEX changes use durable layered specs and
  traceability. This skill must not inflate a bounded change into a full
  document tree.

## Consultative Technical Knowledge Routing

For NORMAL/COMPLEX modules, before finalizing technical specs, read [Technical Knowledge Router](references/technical-knowledge-router.md). Select only the domains triggered by the changed surfaces and risk; inspect current code, tests, architecture, version-matched official sources and existing specialist references. Record decision alternatives, provenance, negative/positive tests and unresolved blocking decisions in the existing specs, Human Task and equivalent JSON fields. Never infer project behavior or tax/regulatory rules. The resulting PR must carry a concise Engineering Explanation linked to evidence. This is not a new schema or a reason to load every technical reference.

Conditional topic references, load only those selected by the router:
[architecture](references/technical-architecture.md),
[data/concurrency](references/technical-data-concurrency.md),
[auth/sessions](references/technical-auth-sessions.md),
[APIs/jobs](references/technical-apis-jobs.md),
[quality/operations](references/technical-quality-operations.md),
[fiscal](references/technical-fiscal.md).

If the selected knowledge is missing, stale or insufficient, follow the router's
knowledge-gap research/update procedure. Persist verified findings in the owning
reference library and reuse them by source/version/purpose; never invent patterns
or treat a saved reference as executed validation. Use existing continuous
improvement ownership rules for cross-project plugin updates.

## Phases

### Studio PRD handoff

When briefed through `studio-prd`, consume the approved briefing, PRD module
inventory and matching-revision internal plan MD/JSON. Reuse decisions and
research instead of repeating the interview. Approval of the PRD is not
implementation authorization. The handoff proposes the first module in the
approved dependency/urgency order and waits for the user's instruction to
start its specification; do not silently specify all modules in a batch.
Unspecified module cards remain awaiting Discovery/SDD, not Ready for Dev.

Work through that module's actors, journeys, business rules, database, backend,
frontend, integrations, observability, security and tests using the existing
templates below. Research relevant source implementation/tests, not README
alone; record exact source/revision/purpose in the project's reference library.
Ask material gaps as they arise. Finish with coverage, pending decisions and
the existing `DISCOVERY_SDD_COMPLETED` Issue report, then request approval
before the next module. Report publication only with the returned comment URL.
Update the plan's real task/contract links after creation; its short task
prompt is not a replacement for the execution-list prompts or authorization.

An in-scope discovery or acceptance fix updates the same module Task and
equivalent JSON with revision/impact. A genuinely independent or out-of-scope
demand needs a scoped decision; do not fragment by layer or specialist.

### Fase 0 - Diagnóstico

Before writing any spec, produce a short diagnosis:

- **O que está claro** — what is unambiguous in the request.
- **O que falta** — missing information needed to spec safely.
- **Riscos iniciais** — early risks (technical, scope, security, data).
- **Perguntas críticas numeradas** — numbered, specific blocking questions.
- **Aguardar resposta humana** when critical scope is missing. Do not proceed to
  specs that depend on unanswered critical questions. Non-blocking gaps may
  continue as marked hypotheses.

### Fase 1 - Consolidação

When planning/spec discovery requires an API, external integration or validation
endpoint, read [API Research Library](references/api-research-library.md).
Prioritize free APIs or a suitable free tier to validate application features
and test the application when relevant, with verified limits and synthetic data.
Use its relevant discovery sources or curated provider candidates, verify them against
official documentation and record the decision plus validation plan/evidence.
An API listing is neither an approved dependency nor an available MCP. Do not
install or send real customer data during research; untested claims remain
NOT VALIDATED. Skip directory research when the task does not need it.

Consolidate the closed scope (becomes the basis of the product/module spec):

- Objetivo
- Escopo incluído
- Fora de escopo
- Restrições
- Usuários impactados
- Dependências
- Riscos
- Decisões pendentes

### Fase 2 - Geração de Specs

When dependencies are selected/changed or security boundaries apply, route
early planning to `security-standard` and its preventive security research
reference. Incorporate applicable OSV advisories and versioned ASVS controls
as explicit rules, enforcement points and negative tests in the existing
module Task/security sector. Reuse the project dependency/source inventory;
do not claim a planned control or advisory match proves runtime security.

When UI applies, route `ui-ux-standard` and its `references/live-design-guide.md`
from the active bundle (or explicit canonical checkout, not guessed sibling
cache paths). Before closing frontend specs, require the client project's
Markdown Design Guide plus cumulative HTML catalogue or mapped existing
equivalent, tokens, source inventory and the applicable visual approval.
Extend the same catalogue while specifying each module. Route exact component
IDs/revisions, catalogue anchors, rules, fixtures and limitations through the
existing design/references fields of the Human Task and equivalent JSON.
Missing catalogue/approval blocks frontend readiness, never becomes a fictitious
PASS or a separate frontend Task. Backend-only work records UI N/A.

For selected UI libraries, preserve the PRD's stable library/source ID in the
frontend/component spec and Human Task. Retain official repository/docs, exact
version/commit or UNKNOWN, component path/variant, purpose/module, license,
dependencies, adaptations and decision state. Reuse native UI first, curated
matching-stack candidates second, targeted Context7/official GitHub research for
gaps. Resolve active ui-ux-standard references/library-source-handoff.md only when
needed; no assumed cross-plugin paths or global catalog loading. Map the same
source ID into existing JSON references and REQUIRED sources only for selected,
necessary dependencies. Resolve material UNKNOWN choices before execution;
nonselected candidates do not become mandatory references. No new schema/gate,
standalone library skill or automatic per-project dependency installation.

For any selected library edition/item, require usable zero-license-cost rights;
paid Pro/Enterprise assets are excluded and unknown cost/license is not eligible
until verified. Preserve item/subtree restrictions, not a whole-repository guarantee.

For every PRD/spec, retain a compact record in its existing references section:
applicable catalog indexes/metadata consulted and revision, selected source ID or
project-native reuse, or N/A with reason. Unavailable/stale evidence is NOT_VALIDATED,
never an invented consultation. Metadata review does not load every source body;
only selected necessary sources become REQUIRED. Preserve the Harness whole-inventory rule.

When the requested surface includes CI/CD, containers, IaC, servers, deployment,
cloud, GitOps, observability, backup/DR, incidents or advanced release strategy,
load [DevOps planning](references/devops-planning.md) and add
`devops-standard` to the required skills. Identify target_environment,
validation, rollback_strategy and human gates in the spec/task. Do not add
DevOps to unrelated application changes, UI-only work or routine Git commits.
Keep tool availability, logs and installation state out of the normative contract.

Generate the specs the request needs, following the hierarchy:

- Create specs per module, page/screen, component and rule.
- Always separate **Banco**, **API/Backend** and **Frontend/UI** (plus the other
  mandatory dimensions).
- Mark hypotheses explicitly (`HIPÓTESE:`).
- Do not invent existing architecture; reference real files/paths only when
  verified.
- Use the templates:
  - `templates/product-spec-template.md`
  - `templates/module-spec-template.md`
  - `templates/page-spec-template.md`
  - `templates/component-spec-template.md`
  - `templates/validation-rules-spec-template.md`
  - `templates/database-spec-template.md` (only with DB impact)
  - `templates/api-spec-template.md` (only with backend)

Suggested location for generated specs (create only what is needed):

```text
docs/specs/<modulo>/
  module-spec.md
  pages/<pagina>.md
  components/<componente>.md
  validation-rules.md
  database.md
  api.md
```

### Fase 3 - Geração de Task Executável

Load the active Harness `references/context-routing.md` before designing the
sector matrix. In this monorepo its source is
`plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md`;
installed hosts resolve the active skill, never assume sibling cache paths.
If unavailable, use an explicitly available canonical checkout or return the
missing reference to the Harness before producing a conflicting contract.

Run the module-boundary gate below before generating Tasks, then validate the
generated set with the same gate before publication or handoff.

#### Module-boundary gate

1. Identify each functional module and its approved end-to-end outcome. Group
   proposed and relevant existing Tasks by scope, dependencies and acceptance
   criteria, not titles or folders alone. A module is a coherent business
   capability, not a layer, phase or specialist. For an existing module, cover
   the requested change completely without rebuilding unrelated functionality.
2. Plan one complete Task per module. Put spec, database, backend, frontend,
   TDD, independent QA, security and documentation into its existing microtasks
   and sector matrix. Preserve owners, dependencies and evidence; justify N/A
   where a discipline does not apply. Separate specs are supporting documents,
   not a reason to create separate spec-only Tasks.
3. Reject Tasks for the same module separated only into "spec", "backend",
   "frontend", "QA" or "implementation", including synonyms and renamed
   fragments. Stop generation/publication/handoff, list affected IDs/titles
   and missing end-to-end coverage, and require consolidation into one complete
   module Task. Do not declare the output ready until it passes a fresh check.
   Detect relevant existing fragments without automatically approving, closing
   or rewriting their Issues or mass-migrating historical Tasks.
4. Allow separation only for production migration, cutover, destructive
   operation, or a genuinely independent delivery requiring its own
   authorization and rollback. Document each exception's boundary, independent
   acceptance criteria, dependencies, explicit authorization gate and rollback
   plan in existing fields. Missing justification blocks generation; size or
   different specialists do not qualify. An ordinary development schema
   migration remains a module microtask.
5. Validate the complete output set, not just each card in isolation: every
   module has its full approved outcome covered by one Task, all applicable
   disciplines are microtasks, and each separated exception is justified.
   Recheck Human Task/JSON equivalence after consolidation. Keep the Task
   template structure and existing contract fields; keep execution_lists in
   the same JSON file and preserve legacy reads. Render action
   checklists with checkboxes as specified below.

Examples: "Orders spec" + "Orders backend" + "Orders frontend" + "Orders QA"
must consolidate into one Orders Task, even if renamed as sequential phases.
One Orders Task with those microtasks passes. Orders and Inventory may be
distinct Tasks when they are genuinely distinct functional modules. A separate
production data cutover needs the documented authorization and rollback above;
calling a backend fragment an "independent delivery" does not make it one.

Produce one reviewable, complete GitHub Issue/card per module using
`templates/task-template.md` and one equivalent v2 JSON contract using
`templates/execution-contract-template.json`:

- Link the mandatory specs.
- Link the GitHub issue (or state that one must be created).
- Suggest the branch name (e.g. `feat/<modulo>-<resumo>`,
  `fix/<modulo>-<resumo>`).
- State the expected PR.
- Include acceptance criteria.
- Include mandatory tests (TDD when applicable).
- Include what is out of scope.
- Link the contract as `docs/execution/TASK-XXX.json`.
- Run Discovery/SDD collaboratively: ask the user critical questions, research
  authoritative references, consolidate decisions, then publish a
  `DISCOVERY_SDD_COMPLETED` Issue comment before requesting human approval.
- Keep validated sources in `docs/biblioteca-referencias/` and route the exact
  file/section and purpose. When UI applies, route the Design Guide, tokens,
  component library, visual references and approved mockup under `docs/design/`.
- Decompose execution into microtasks with owner skill/plugin, capability,
  preferred tool, dependencies, exact references, allowed paths, checklist,
  deliverables, completion condition and independent validator.
- Materialize the selected execution routes in the Task and equivalent JSON,
  not only in a Discovery comment. Use existing microtask owner/plugin,
  capability, preferred_tool and reference fields; put necessary auxiliary
  tool identifiers, purpose, conditions and approved fallback in list
  instructions or purpose-qualified required references. Each execution list
  resolves its microtask_ids in the same contract. Do not paste the inventory
  or full skill bodies. The executor starts from this selection plus mandatory
  canonical skill/source reads; expand discovery only for gaps, failures,
  changed availability or new needs. Return normative changes to Harness.
- Render every stage, microtask and REQUIRED-sector action checklist as Markdown
  `- [ ]` items, not semicolon-separated prose or uncheckable numbered steps.
  Split complex items into nested checkbox subitems inside the same Task.
  Give each leaf an observable completion condition; do not create new Tasks
  or Issues for these internal steps. New items start unchecked. Mark `- [x]`
  only with the responsible owner's completion evidence; a parent requires all
  applicable children completed. Blocked/unvalidated items stay unchecked with
  reasons; justified N/A is not a completed action. Human approval gates remain
  separate. Keep checkbox progress in the Human Task/evidence ledger, while
  normative actions remain equivalent in the existing JSON checklist fields,
  without adding mutable checked-state fields.
- Generate one prompt per execution checklist/list (microtask, stage or sector).
  Each prompt contains a clickable link to the single Task JSON file and the
  selected `list_id`. Put all list objects in that file's `execution_lists`,
  beside the global contract. Never embed JSON in the Human Task, attach its
  body to the prompt, or create separate JSON files per list. Use a real local
  file link or versioned repository URL. Never generate a prompt per checkbox
  or nested subitem. Preserve task identity/revision at file level and each
  list's owner, phase, complete checklist/subitems and microtask references.
  Global scope, protected paths, acceptance, tests, sources and stop conditions
  remain mandatory through that contract. Check every prompt link resolves to
  the same Task file, every list ID resolves exactly once, and list actions and
  applicable microtask checklists agree with no omitted requirements or wrong owner.
  The file is a detailed execution contract, not merely a routing index: each
  list specifies objective, scoped actions, dependencies, exact required sources
  and their purposes, allowed/protected paths, expected deliverables, observable
  completion conditions, tests, acceptance and stop conditions. Resolve relevant
  requirements/business rules and input/output, error and negative-path
  expectations from the global contract/specs. Reference IDs are acceptable only
  when they resolve to concrete instructions in the same file or required sources.
  Never require the Human Task to discover an omitted execution rule. Reuse
  global constraints without copying unrelated context into every list. Unknown
  stack, paths, commands or product decisions remain explicit blockers, never
  invented detail or empty fields presented as ready. No detail level alone
  proves quality; execution and independent validation remain required.
  Use the active Harness `references/context-routing.md` transport rules.
  Harness alone compares the full Human Task and JSON. Specialists execute
  from the supplied JSON plus mandatory skill/spec/code reads; do not require
  them to read the Human Task or its sections as execution input. Missing or
  conflicting JSON returns to Harness. A Human Task reference is provenance,
  never permission to substitute prose for missing JSON instructions.
- Make `Prompt para o executor` the Harness bootstrap for the full Task and
  its per-list prompt/JSON handoffs. Specialists verify task/list identity,
  contract revision and current Harness evidence of card/JSON equivalence, load routed
  skills/references, stops on divergence, collects receipts, publishes material
  comments, and forbids merge/deploy without explicit authorization.
- Record planned validations in the Human Task with owner skill, capability,
  and preferred tool when known. Put only those compact identifiers in the
  Execution Contract `required_validations`; never store installation state,
  official URLs, executable paths, or logs there.
- Include all ten standard sectors with REQUIRED/N/A, concrete owner,
  dependencies and a short verified N/A reason. Detail only REQUIRED sectors;
  each has objective, sources with purpose, checklist, expected evidence and
  result placeholder. No generic full OWASP/QA checklist on unrelated tasks.
- Use v2 `sectors`, normative references and microtasks in new contracts. Human
  card and JSON share `contract_revision`; any normative change updates both.
  Mutable status, receipts, logs and execution evidence do not belong in JSON.
- Separate final `depends_on` from optional `planning_depends_on`. QA, Security
  and UI planning may start early; only executed validation closes their gates.
  Check unknown IDs, owners, missing required references and cycles before handoff.
- Give the Harness the complete Human Task; give each specialist its list JSON,
  canonical JSON sector/global constraints/acceptance, necessary code and dependency
  receipts. Missing context requests expansion, not loading all sources by default.
- For behavioral changes, bugfixes, APIs, user flows, business rules, persistent
  state, payments, tenancy, imports/exports, integrations or concurrency, route
  independent QA planning to `qa-testing-standard`. It returns QA_GUARDRAILS,
  TEST_SCENARIOS, REGRESSION_TARGETS and VALIDATION_REQUIREMENTS proportionally.
  Docs/metadata-only work may record QA N/A; pure visual changes still require UI.

The Execution Contract must be valid JSON and include the v2 identity/revision,
human task link and equivalence declaration, summary/goal/discovery, current and
expected state, scope, protected and allowed paths, requirements, business
rules, references, design, microtasks, ten sectors, tests, acceptance criteria,
stop conditions, ignition prompt and reporting contract. Keep structure concise;
do not copy source bodies, conversation history, secrets or execution evidence.

Before `DISCOVERY_SDD_COMPLETED`, publication/handoff or Ready for Dev, apply
[spec consistency analysis](references/spec-consistency-analysis.md) to the
current artifacts. This refines the existing coverage/equivalence checkpoint,
not a new state, Task or approval gate. Return blocking findings to their source,
reconcile affected specs/card/JSON and recheck before claiming readiness.

Tasks live under `docs/tasks/TASK-XXX-<slug>.md` (or the repo's existing task
location, if one exists — reuse it, do not duplicate).

Execution Contracts live under `docs/execution/TASK-XXX.json` unless the
repository already has an equivalent canonical location.

For a legacy task without a contract, keep it readable. When it re-enters
execution, generate and validate its contract before implementation. Do not
mass-migrate historical tasks.

### Fase 4 - Checklist de PR/QA

Provide the delivery gates using `templates/pr-template.md`,
`templates/qa-review-template.md` and `templates/review-template.md`:

- Code review
- QA funcional (delegated to `qa-testing-standard` when behavioral triggers apply)
- QA visual (delegated to `ui-ux-standard`)
- Segurança (delegated to `security-standard`)
- Testes
- Evidências
- Aprovação / reprovação

## Integration with the other plugins

- `dev-workflow-standard` is the Engineering Harness. It owns discovery, scope,
  delegation, gates and approval. SDD Spec Factory feeds it the specs and the
  executable task; it does not replace it.
- `dev-implementation-standard` is the executor. It implements the approved task
  strictly within the scope these specs define; it consumes the task and PR
  templates produced here.
- `ui-ux-standard` owns design systems, mockups and visual QA. Page/component/UI
  specs should reference approved mockups and design tokens instead of inventing
  visuals.
- `qa-testing-standard` owns independent test strategy, functional validation,
  reproduction, regression and fix verification. It receives the QA Task slice
  and relevant sources; it neither writes product fixes nor attests UI/Security/
  DevOps PASS. Those owners return their own evidence.
- `security-standard` owns the security review and release gate. The security
  dimension of each spec and the security checklist of each PR are validated by
  it.

## Definition of done for this skill

- The needed specs exist and follow the hierarchy.
- Banco, API/Backend, Frontend/UI, Testes, Segurança, Observabilidade,
  Decisões pendentes, Riscos and Critérios de aceite are separated.
- There is one complete executable Task per module linking specs, issue, branch
  and PR, with applicable disciplines as microtasks. The module-boundary gate
  passed for the entire output set and every separation exception is justified.
- Every new executable task has a valid v2 Execution Contract with normative
  equivalence to the complete Issue/card and a copy-ready ignition prompt;
  legacy tasks have the compatibility fallback above.
- PR and QA/review checklists are provided.
- Sector matrix, microtasks, purpose-based routing, phase dependencies and
  explicit N/A reasons are consistent; legacy v1 contracts remain readable.
- Spec consistency analysis maps approved in-scope requirements to microtasks,
  acceptance and planned validation; blocking gaps/conflicts are resolved.
- No product code was implemented and no existing architecture was invented.
