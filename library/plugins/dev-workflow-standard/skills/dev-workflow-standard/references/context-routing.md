# Context Routing and Sector Validation Matrix

This is a [LOCAL EXTENSION] of the existing Harness contract, not a new runtime
engine or provider standard. New tasks use `schema_version: 2`. Existing v1
contracts remain readable and are migrated only when resumed for material work.

## Sources of truth and ownership

The GitHub Issue is the complete Human Task for people. The v2 Execution
Contract is its structured LLM representation with **normative equivalence**:
the same approved requirements, business rules, references, microtasks,
constraints and acceptance criteria, under the same `contract_revision`.
Mutable progress, evidence and discussion remain in Issue comments and
receipts. Harness reads the complete Human Task and the v2 JSON, verifies
equivalence, reconciles scope and all sectors, then delegates a list.
The specialist reads the list JSON and relevant canonical JSON fields, not the
Human Task or its sections as execution input. It also reads its
entire canonical SKILL.md, routed sections and the smallest complete context
needed for its claim. Progressive disclosure never removes a mandatory rule.

Keep these invariants explicit:

- `CODE_COMPLETE != TASK_COMPLETE`
- `NO_EVIDENCE != PASS`
- `SECTOR_REQUIRED != OPTIONAL`
- `OUTSIDE_OWNER != AUTHORIZED_TO_PASS`
- `CONTEXT_AVAILABLE != CONTEXT_REQUIRED`

Only the sector owner attests its result. Another specialist can request
`REWORK_REQUESTED`, provide evidence or block its own dependent checkpoint; it
cannot mark another sector PASS or fabricate another skill's receipt. The
Harness records the owner's returned evidence and reconciles the final gate.

Context retrieval is an auxiliary step after normative routing. The Harness or
specialist may use `context-retriever.py` to discover additional relevant code
or engineering context, preferably through Potpie when healthy. Every
`required_source` remains mandatory regardless of retrieval ranking. Retrieved
material never changes `allowed_paths`, protected paths, owner, applicability,
acceptance criteria or stop conditions. Conflicts return
`source_of_truth_conflict`.

## v2 task contract and v1 compatibility

In v2, `acceptance_criteria` contains the normative criteria. `references`
resolves source IDs to `project_path`, `section` and `purpose`. `sectors` maps
stable IDs to routing objects:

| ID | Human sector | Default owner |
| --- | --- | --- |
| database | Banco | dev-implementation-standard |
| backend | API / Backend | dev-implementation-standard |
| frontend | Frontend | dev-implementation-standard |
| ui_ux | UI / UX | ui-ux-standard |
| qa | QA / Testes | qa-testing-standard |
| security | Segurança | security-standard |
| devops | DevOps / Infraestrutura | devops-standard |
| observability | Observabilidade | Explicit owner for application instrumentation or operations |
| documentation | Documentação | Explicit scoped executor, normally dev-implementation-standard |
| harness | Gate Final do Harness | dev-workflow-standard |

All ten IDs appear in new routed contracts and in the human matrix. Resolve a
single concrete owner, including N/A rows. Additional material domains require
an explicit ID, owner and rationale in the Task, not a guessed specialist.

Every v2 sector has `owner`, `applicability`, `depends_on`, `microtasks`,
`required_sources` and `required_validations`. A microtask carries its concrete
owner skill/plugin, capability, preferred tool, dependencies, exact reference
IDs, allowed paths, checklist, deliverables and completion condition.
`applicability` is `REQUIRED` or `N/A`; N/A also requires a nonempty `reason`.
N/A needs no detailed Task section, sources, validations or dependencies.
REQUIRED needs objective, checklist and expected evidence in the Human Task and
the equivalent v2 JSON representation. Validation entries remain capability
IDs; exact reference records resolve project file and section plus purpose.

Persist the Discovery tool/skill selection in these existing routing fields,
with auxiliary tools, purpose, conditions and approved fallback in execution
list instructions or purpose-qualified required references. The list resolves
its microtask_ids in the same JSON; the executor need not rediscover the whole
inventory for each list. Read the selected canonical skill and required sources;
expand discovery for missing context, failures, changed availability or new
needs. Return contract changes to Harness. Keep runtime availability and tool
receipts in evidence, not normative JSON; never copy catalog or skill bodies.

V2 uses `required_sources` as reference ID arrays. Optional
`conditional_sources` entries contain `reference_id` and `condition`;
`optional_sources` is an optional reference ID array. Unknown IDs block.
The following path-object fields describe legacy v1 only:

- `global_acceptance_refs`: anchored references to global acceptance criteria.

- `task_sections`: explicit `task:#anchor` references, resolved against
  `task_path`; use unique headings or explicit HTML anchors in the Human Task.
- `required_sources`: objects with `path` and nonempty `purpose`.
- `conditional_sources`: objects with `path`, `purpose` and an explicit
  `condition`; evaluate that condition before loading the source.
- `optional_sources`: optional list of `path`/`purpose`; do not load OPTIONAL
  automatically. Record the reason if consulting one becomes useful.
- `depends_on`: sector IDs whose final validation receipts are prerequisites.
- `planning_depends_on`: optional separate IDs required only for planning;
  absent means no sector completion prerequisites for planning, not no scope
  or mandatory-source prerequisites.

Paths are repository-root relative; a `#anchor` narrows the requested section.
Global goal, allowed paths, exclusions, stop conditions and relevant acceptance
criteria always constrain the slice. Routed contracts do not automatically load
all legacy `specs`/`docs`/`required_skills` arrays: they remain compatible indexes,
while the Harness routes the necessary entries to each owner. A globally
mandatory rule cannot be omitted by omitting it from a sector source list.

Do not store mutable result, logs, receipts, execution evidence, copied source
bodies or runtime installation state in the contract. V2 does store normative
checklists and preferred tool identifiers because they are part of the approved
execution instruction. Progress and receipt references live in the Human Task
Issue/comments and evidence ledger.

## Resolve and load a slice

### One linked prompt per list, one JSON file per Task

Every execution checklist/list has one prompt containing a clickable link to
the single Task JSON file and the selected `list_id`. Store every list object
under `execution_lists` in that file, alongside shared scope and constraints.
No JSON body belongs in the Human Task or prompt, and no per-list JSON files
are generated. Use actual local-file links or versioned repository-file URLs.
Items and nested subitems do not receive separate prompts. Microtask, stage and sector lists use stable
`list_id` values; a repeated view of the same list reuses its ID and does not
authorize executing it twice. Approval lists remain human gates, not agent
permission to approve them.

The canonical Task JSON has shared `task_id`, `contract_revision`, global
constraints and an `execution_lists` collection. Each entry contains `list_id`,
`owner_skill`, `phase`, applicable `microtask_ids` and the entire `checklist`.
Include objective, dependencies, references with resolvable purposes,
allowed/protected paths, deliverables, completion condition, required tests,
acceptance criteria and stop conditions. Relevant business rules and boundary,
input/output and error cases resolve through the global contract/specs. A list
must be executable from this JSON and its declared technical sources without
needing Human Task prose to fill missing requirements. Unknown decisions,
paths or commands are explicit planning blockers, not invented instructions.
Preserve nested items
as objects with `instruction` and optional `children`; do not include mutable
checked state in the normative instructions. Keep actionable text equivalent
to the canonical contract. All inherited scope, allowed/protected paths,
criteria, tests, required sources, dependencies and stop conditions still
apply. Resolve them from the same JSON file before execution; never treat a small list as
permission to omit global restrictions. Linked source documents and code are
still read when required; JSON replaces the Human Task as specialist input,
not the technical evidence needed for implementation or review.

Harness validates link resolution, unique list identity and revision, owner,
all checklist items/subitems and normative equivalence before handoff. Attach or
link its current comparison receipt and relevant dependency receipts outside
the normative Task JSON. A stale/missing receipt, missing canonical contract,
unknown/duplicate list ID, changed checklist or wrong owner blocks execution.
Ask Harness to correct the shared JSON file, not to supply the Human Task.
Update card and file revision together after normative edits; a checkbox
progress change alone is not a new contract. Existing v2 files without
`execution_lists` remain readable; Harness adds this collection when routing
new list prompts, rather than silently treating missing lists as executable.
Legacy contracts must be normalized/routed by Harness before this handoff;
historical `task_sections` remain provenance, not required specialist reading.

Handoff contains `task_id`, `list_id`, `execution_contract_path`, `sector`, `phase`
(`planning` or `validation`), revision and relevant `dependency_receipts` paths.
No Task/spec bodies are pasted into it.

1. Validate the schema. For v2, Harness compares all normative content with the
   linked Issue, records its revision and observed Issue update time in the
   existing receipt, and routes a list prompt linking the shared JSON file.
   Each specialist checks list identity, revision, canonical JSON and Harness
   comparison evidence without reading the human card. Missing comparison evidence, changed Issue content or
   divergence stops the checkpoint with `human_task_json_divergence`; request
   a fresh Harness comparison. Do not add verification state to the JSON.
2. Check all ten applicability decisions, N/A reasons, known dependency IDs,
   no self-dependencies or cycles in either phase graph, and that final Harness
   dependencies include every other REQUIRED sector.
3. Resolve the sector's canonical SKILL.md and read it completely. Read its
   mandatory active-phase references and emit SKILL_RECEIPT.
4. Read the minimal global summary/constraints, routed microtasks and relevant
   acceptance criteria from JSON. Harness owns Human Task reconciliation;
   specialists do not substitute its prose for missing JSON instructions.
5. Read REQUIRED sources for their stated purpose. Evaluate each CONDITIONAL
   source against observed scope and record activated/not activated with reason.
   OPTIONAL sources are not loaded by default. Inspect only relevant code.
   After required sources are loaded, context retrieval may add bounded
   supplemental paths/snippets under `context-retrieval.md`; record the backend
   and returned evidence and never treat retrieval as authorization.
6. Check the phase's dependency receipts for owner, validation scope, artifact
   and revision. Unavailable, incomplete or stale evidence is not a passed
   prerequisite. Revalidate after material artifact changes; a new revision
   needs an explicit applicability check before prior evidence can be reused.
7. Execute the bounded checkpoint and return the existing EXECUTION_RECEIPT
   with sector, phase, revision, sources_loaded, conditional_sources_loaded and
   validation_scope. Keep results in the Task, not in the router JSON.

Missing REQUIRED source/anchor/skill uses `mandatory_reference_missing` and
stops that checkpoint. Unknown sectors, owners, dependencies, cycles or
contradictory applicability stop contract resolution. Conflicts between
Task/spec/code use `source_of_truth_conflict`; do not silently pick one.
An active conditional source becomes mandatory. If its condition cannot be
determined and affects a required claim, request context before proceeding.

For insufficient context, send `CONTEXT_EXPANSION` using the existing handoff:
`reason`, `required_source`, `blocking_claim`. The Harness resolves the request.
Harness resolves Human Task conflicts and supplies corrected JSON. Specialists
read the human card only if the user explicitly requests a card audit or edit,
not as an automatic execution/context-expansion fallback.

## Phases, states and final gate

Planning QA/Security/UI may proceed before implementation when their own
prerequisites are met. Planning completion never satisfies final validation
`depends_on` and never closes the sector's final result. Do not union the two
graphs: phase ordering can differ without requiring a second state engine.

Reuse PENDING, READY, RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
PASS is a validation outcome mapped to COMPLETED only with owner evidence.
PARTIAL and NOT_VALIDATED cannot complete REQUIRED work; FAILED maps to REWORK
or BLOCKED with cause. N/A is applicability, not a successful test, and a
justified N/A does not block or become a required dependency.

The final Harness gate requires every other REQUIRED sector to have current,
scope-matching owner SKILL_RECEIPT and EXECUTION_RECEIPT, executed mandatory
validation, satisfied acceptance criteria, and no unresolved blocker. Only
then may the Harness close its own gate with reconciliation evidence. PENDING,
REWORK, BLOCKED, PARTIAL or NOT_VALIDATED in any REQUIRED sector prevents Task
COMPLETED. PR consistency, required documentation and human acceptance gates
remain mandatory. Code completion alone cannot bypass QA or another owner.

## Compatibility and installed hosts

Without `sectors`, v1 is valid legacy input. Harness derives a bounded handoff from existing
scope/specs, records the routing decision in the Task when work resumes and
does not bulk-migrate inactive contracts. A resumed task requiring material
specification changes should be upgraded deliberately to v2, with card/JSON
revision and equivalence review. Never assume unknown sector fields were
consumed by an older installed plugin; verify support.

Resolve this reference from the active `dev-workflow-standard` skill's
`references/context-routing.md`. Monorepo paths in documentation are source
locations, not assumptions about sibling versioned plugin caches. If the active
bundle lacks it, use an explicitly available canonical checkout or return the
missing capability to the Harness. Do not silently install or imitate it.

| Previous responsibility | Location after extension |
| --- | --- |
| Flat required skills/specs/docs | Preserved for v1; v2 uses equivalent structured references and microtasks |
| Banco/API/Frontend task sections | Ten-row matrix plus details only for REQUIRED sectors |
| Generic QA checklist | QA sector and qa-testing-standard; UI/Security retain their own evidence |
| Large task handoffs | Identifiers, phase, sector, revision and dependency receipt paths |
| Mutable progress | Human Task ledger and existing receipts, never contract JSON |

Structural tests and scenario reviews validate these documents and fixtures;
they are not an automated runtime enforcement engine or proof of future LLM
behavior. Context economy is qualitative unless measured: Harness reads the
whole Task; a specialist omits unrelated sectors, sources and receipts.
