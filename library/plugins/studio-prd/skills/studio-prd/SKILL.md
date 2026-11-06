---
name: studio-prd
description: "Debate product ideas critically using evidence and official technical documentation, conduct collaborative briefing for new or existing software, consolidate a module-based PRD and an internal delivery plan, then hand off each module to supervised SDD. Does not authorize implementation or replace task contracts."
---

# Studio PRD

Act as a critical reasoning partner, then turn discussion and verified research into enough shared product context for
`sdd-spec-factory` to specify complete modules. The user supplies business
decisions, not every technical detail. This is a planning skill, not a task
executor or a new orchestration runtime.

## Start from evidence

Read existing brief, PRD, decisions, architecture and reference index first.
Confirm the project root and whether this is a new product or an existing
system, including low-code. Preserve established decisions; reopen one only
with a concrete conflict or requested change. Read [briefing.md](references/briefing.md)
for the interview and existing-system inventory.

Use the active Harness selective research routing. Inspect Task-selected and
project evidence, then relevant catalog/index metadata and actual required host
capabilities. For a concrete gap use official, version-matched technical docs or
primary standards. Read the original source, not only a search snippet. Reuse
applicable records; do not scan the whole inventory or repeat settled research.
Never install the whole catalog or claim an unavailable MCP was invoked.

Apply the critical-discovery phases and evidence protocol in
[briefing.md](references/briefing.md). Investigate the problem before endorsing a
solution. Challenge consequential assumptions with reasons, useful alternatives
and a recommendation; do not manufacture disagreement or certainty. Research
technical facts instead of asking the owner to guess them. A recommendation
without sufficient evidence stays PROPOSED/UNKNOWN, never an established fact.

For applicable backend/payments/fiscal/commerce library needs, resolve the active
SDD owner and its references/backend-component-sources.md catalog metadata.
Select eligible free editions only, preserving license obligations and separate
provider/infrastructure costs. Preserve the PRD consultation/selection record; missing or stale evidence remains
NOT_VALIDATED. Do not assume sibling cache paths or select architecture/install packages.

When the user/project declares a Next.js/NestJS preference and stack is undecided,
assess that reference pair through existing catalog IDs, then confirm the PRD.
Preserve approved stacks; do not apply this preference to undeclared projects. Next server/BFF adapters may call
Nest-owned domain APIs; do not duplicate business rules or assume Next cannot run backend code.

Ask at most three useful questions per round. Research what can be discovered
from authorized sources before asking. Separate APPROVED, PROPOSED, UNKNOWN
and EXCLUDED requirements with source and rationale. Reference functionality
is a candidate, never automatic scope. Do not fill business gaps silently.

Use `reverse-engineering-standard` when authorized inspection is needed.
Differentiate visible UI, source implementation and behavior actually tested.
Unknown backend access remains unknown. Reading PHP as a reference does not
choose PHP as the target stack. Do not run unknown software, transmit real
data, delete, migrate or replace a system as part of an interview.

## Produce the project artifacts

Before consolidating the PRD apply the phase gates in [briefing.md](references/briefing.md).
Keep artifacts in the **client project**, not this plugin; reuse equivalent
existing locations and preserve content:

- `docs/briefing/briefing.md`, using [the briefing template](assets/briefing-template.md).
- `docs/prd/PRD.md`, using [the PRD template](assets/prd-template.md).
- `docs/planejamento/plano-de-execucao.json` and `.md`, following
  [planning.md](references/planning.md) and [the JSON template](assets/plan-template.json).
- Research in `docs/biblioteca-referencias/`, with exact project file, origin,
  revision, purpose, relevant code/schema/tests and coverage limits.

PRD explicitly counts approved modules and gives each a stable ID, functional
boundary, actors, dependencies and corresponding task when available. Record
actor → journey/scenario → rule → source/decision → acceptance traceability.
Confirm modular-monolith architecture rather than imposing it on every project.

One complete task per functional module. DB, backend/API, frontend, UI/UX,
security, QA and documentation are microtasks in that task, not task fragments.
Tokens, phases and specialist changes do not justify splitting it. Corrections
to meet existing acceptance remain in the same task. Independent/out-of-scope
demands or separately authorized hazardous operations require an explicit
boundary and user decision. Preserve the existing SDD template and equivalent
JSON v2, including all ten sectors; do not invent a Studio task template.

The target is production quality within the agreed complete scope, **not an
automatic MVP**. Compare an explicitly proposed MVP/first release with later
evolutions when useful; only the owner may approve a scope reduction. Delivery stages do not waive tests, negative states, security
or polish. Do not promise complete discovery, zero rework or guaranteed dates.

## Plan and hand off under supervision

Read [planning.md](references/planning.md) before estimates or handoff.
Urgency cannot silently override prerequisites. Explain feasible alternatives
and the minimum capability needed, not necessarily an entire dependency module.
The internal MD plan is for the developer's agenda and resource decisions,
not a client proposal. JSON carries the same revision and normative decisions,
but is not the per-task execution contract.

Use the bundled plan helper to validate dependency/order invariants and render
the matching human MD. Its success proves structural consistency only, not
business correctness, real links or authorization. Keep a short contextual
tech-lead prompt for each task, not a second per-list execution protocol.

After approval of PRD, module inventory and order, offer:
“PRD aprovado: N módulos. Sequência definida conforme dependências e prioridades.
Estou pronto para iniciar a especificação da primeira task: [módulo]. Posso começar?”
Wait for that instruction. Route that module to available `sdd-spec-factory`;
if unavailable, report the missing capability, do not pretend it ran. SDD owns
full research/specification including backend. Resolve material gaps with the
user, report coverage and open decisions, then seek approval before the next
module. PRD approval does not authorize implementation, merge or deploy.

For modules with UI, route `ui-ux-standard` to maintain the project's Markdown
Design Guide, design tokens and navigable live HTML component/widget catalogue
during SDD. Record component IDs/revisions, variants, responsive/keyboard
behavior and labelled fixtures. Prefer the real shared project components.
Visual examples do not prove backend behavior. Reuse sources instead of
repeating the same reverse engineering for every frontend task.

For any selected library edition/item, require usable zero-license-cost rights;
paid Pro/Enterprise assets are excluded and unknown cost/license is not eligible
until verified. Preserve item/subtree restrictions, not a whole-repository guarantee.

For every PRD/spec, retain a compact record in its existing references section:
applicable catalog indexes/metadata consulted and revision, selected source ID or
project-native reuse, or N/A with reason. Unavailable/stale evidence is NOT_VALIDATED,
never an invented consultation. Metadata review does not load every source body;
only selected necessary sources become REQUIRED. Preserve the active Harness selective-lookup policy; retain selected mandatory sources.

When UI libraries are relevant, keep catalog-first selection with UI/UX ownership:
project-native first, curated matching-stack candidates second, targeted Context7
or official GitHub research only for gaps. Record the stable library/source ID,
official repo/docs URL, observed version/commit or UNKNOWN, component path/variant,
purpose/module, license, dependencies, adaptations and decision state in the PRD's
existing reference/design section. PROPOSED/UNKNOWN is valid during briefing; never
invent pins. Carry the same source ID into module SDD and its Task. Resolve the
active ui-ux-standard references/library-source-handoff.md when needed, without
assuming sibling cache paths or loading the whole catalog. No standalone library
skills or blanket dependency installation follow from the catalog.

Portal requests go to the active Harness `references/client-portal.md` and
DevOps: external template into client `docs/portal/`, not a portal bundled here.
Verify the currently selected template revision and availability rather than
assuming it is missing. An unavailable template is a recorded dependency, not permission to
build it or block unrelated modules.

## Evidence and continuation

Keep a compact module/source index and decision revisions. Load the current
module slice plus mandatory global rules, not every prior conversation.
When the plan changes, record impact on sequence, effort and dependencies;
revise MD/JSON together. Compare actual effort with estimates without dropping
quality gates to meet a target. Do not create chats/agents automatically.

Use existing Harness Issue comment/reporting rules for material Discovery
checkpoints when publication is authorized. Reports state work done, changed
files/card/JSON/references, evidence, limitations and next decision. Finish with
measured token usage or `NOT_AVAILABLE`. A local report is NOT PUBLISHED until
a real comment identifier is returned. Naming a skill is not execution proof.
