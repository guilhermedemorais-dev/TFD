# Workflow Pipeline

End-to-end delivery pipeline across the independent specialist skills. The LLM using
`dev-workflow-standard` is the engineering harness and is the only role that approves moving from one gate to
the next. It never writes product code itself; it routes work to executable capabilities and requires invocation plus validation evidence before advancing.

## Skills and roles

| Skill | Role |
| --- | --- |
| `dev-workflow-standard` | Engineering harness / final reviewer |
| `dev-environment-standard` | Environment bootstrap / plugin health |
| `studio-prd` | Collaborative briefing, PRD and internal MD/JSON delivery plan |
| `sdd-spec-factory` | Requirements LLM / executable task |
| `dev-implementation-standard` | Executor agent / coder |
| `ui-ux-standard` | UI/UX specialist LLM |
| `qa-testing-standard` | Independent functional QA / Test Engineering |
| `security-standard` | Security specialist LLM |
| `devops-standard` | Operational infrastructure, CI/CD, releases and recovery |

## Pipeline

For new products or existing-system reassessment, Studio PRD first researches
authorized sources and interviews the user in bounded rounds. Record actors,
journeys, module count/IDs, production scope, urgency and real dependencies.
Store the internal plan separately from the PRD, with the same normative
decisions/revision in MD and JSON. Effort hours differ from calendar duration;
capacity, ranges, risks and unknowns remain explicit. A short contextual prompt
per task helps the user start separate chats without duplicating task contracts.

After approval of PRD and ordering, ask before the first module specification.
SDD retains the complete existing task/card/JSON model, including backend and
all required validation sectors. Pause for material business gaps and review
each module before advancing, not an unattended batch. For UI, build the
project's live HTML catalogue alongside the Markdown guide while specifying,
then reuse component IDs/revisions during implementation and independent QA.
This does not require rebuilding a briefing for an already specified bounded task.

First project onboarding, when remote governance is required:

```text
Environment available -> Git/gh prepared -> human auth handoff if required
  -> repository access/admin/Project capability diagnosis
  -> DevOps diagnose -> propose -> explicit human confirmation -> apply
  -> verify -> readiness evidence -> Harness gate -> first Task
```

DevOps owns this repository readiness bootstrap; it is not a new skill.
Environment prepares prerequisites only. Reuse compatible evidence for normal
Tasks, rechecking on drift, relevant change, real failure or explicit request.
Do not run the full bootstrap before every Task. Three read-only operations
(diagnose/propose/verify) cannot mutate GitHub or the checkout. Apply is scoped
to a reviewed proposal, never permission for push/merge/deploy. See the
[DevOps reference](../plugins/devops-standard/skills/devops-standard/references/github-governance.md).

Readiness requires Environment, applicable authentication, repository access,
required files/governance, Project and CI evidence (or explicit justified N/A),
human gates and executed verification. A sufficient approved fallback may yield
READY_WITH_LIMITATIONS; unknown mandatory evidence cannot. Governance readiness
does not replace Harness execution states. PROJECT READY != PRODUCTION AUTHORIZED.

```text
Idea / demand
  -> dev-workflow-standard: diagnose (critical questions, risks)
  -> Discovery / SDD colaborativo: perguntas ao usuário + pesquisa + referências
  -> sdd-spec-factory: consolidate specs, Design Guide and exact reference routes
  -> module-boundary gate: one complete Task per functional module; reject layer/phase/specialist fragments
  -> sdd-spec-factory: generate complete GitHub Issue + equivalent JSON v2 per module
  -> validate generated Task set: consolidate fragments; justify authorization/rollback exceptions
  -> microtasks: skill/plugin/capability/tool/references/paths/checklist/deliverables
  -> Sector Validation Matrix: ten REQUIRED/N/A sectors, owners and dependencies
  -> existing SDD coverage/equivalence check: requirement-to-microtask mapping, orphan actions, ambiguities and contradictions
  -> Context Routing: Harness reconciles Human Task/JSON; one prompt linking the single Task JSON file + list_id per execution list
  -> publish DISCOVERY_SDD_COMPLETED comment and capture returned identifier
  -> HUMAN APPROVAL
  -> Ready for Dev
  -> list bootstrap: task_id + list_id + shared JSON link + execution_contract_path + sector + revision + relevant receipts
  -> contract validation + progressive disclosure of mandatory references
  -> required skills read + SKILL_RECEIPT
  -> environment status: compatible fast path for required capabilities
  -> dev-environment-standard prepare/repair only if a prerequisite is missing
  -> capability resolution + runtime availability check
  -> owner skill resolves tool registry + compatible local runtime state
  -> cached fast path or detect/install/verify/persist slow path
  -> selected capability invoked; state RUNNING
  -> REUSE_INVENTORY + MINIMAL_CODE_GATE
  -> dev-implementation-standard: implement DB/backend/frontend/docs microtasks
  -> developer TDD and executor tests
  -> execution result: diff / files / commands / artifacts
  -> completed EXECUTION_RECEIPT
  -> Human Task updated
  -> EXECUTION_REPORT_COMMENT -> linked GitHub Issue when available
  -> dev-workflow-standard: VALIDATING
  -> independent functional QA / Security QA / UI-UX QA / DevOps-observability as REQUIRED
  -> owner skill corrects failures; the same validator retests the new revision
  -> Sector Reconciliation: owner receipts, evidence and current revision
  -> PR Gate: review package links task, issue, branch, specs followed
  -> Pull Request when authorized; no fabricated remote publication
  -> Harness Final Gate and Human Review
  -> dev-workflow-standard: approve or request rework
  -> human approval and human merge (Done only after observed merge)
  -> deploy (separate explicit authorization after PR approval)
```

## Gates (must pass before advancing)

1. **Scope gate** — critical questions answered; scope consolidated. Owned by
   `dev-workflow-standard`.
2. **Spec gate** — required specs exist and follow the hierarchy
   (Product → Module → Page → Component), with Banco / API/Backend / Frontend/UI
   / Testes / Segurança / Observabilidade / Decisões / Riscos / Critérios de
   aceite separated. Owned by `sdd-spec-factory`, approved by the orchestrator.
3. **Task gate** — one complete Task per functional module, with disciplines
   as internal microtasks. Stop generation/handoff for same-module fragments
   split only by spec, layer, phase or specialist; require consolidation.
   Separate only production migration, cutover, destructive operation or a
   genuinely independent delivery requiring its own authorization and rollback,
   with documented boundary, acceptance criteria, dependencies and gates.
   Preserve the human template structure; store all execution_lists in one JSON file. Action checklists use `- [ ]`,
   with nested steps for complex work within the same Task; `- [x]` requires
   owner evidence and completed applicable children, not automatic approval.
   The complete GitHub Issue and JSON v2 have the same
   `contract_revision` and normative equivalence for scope, rules, references,
   microtasks, acceptance criteria, tests and stop conditions. The published
   `DISCOVERY_SDD_COMPLETED` comment precedes HUMAN APPROVAL and Ready for Dev.
4. **Implementation gate** — task implemented within scope; required commands run;
   tests pass; task result updated; skill receipt and reuse evidence exist. Owned
   by the executor agent using `dev-implementation-standard`.
5. **Review gate** — PR links task, issue, branch and specs; UI validated by
   `ui-ux-standard` when there is UI; security validated by `security-standard`
   when triggers apply; independent QA passed when REQUIRED. All required sectors
   reconciled with their own owners' evidence; N/A justified. Approved or sent to
   rework by the orchestrator. A local package is not a published PR.
6. **Release gate** — no deploy without an approved PR.

## Mandatory triggers

- `qa-testing-standard`: behavioral changes, bugfixes, user/API flows, business
  rules, persistence, payments, tenants, import/export, integration, concurrency,
  state transitions and reported regressions. Docs/metadata without behavioral
  impact may be N/A with reason. Pure visual changes still require UI review.
  QA planning can precede implementation; final validation needs the relevant
  implemented dependencies. No silent substitution by the product implementer.

- `devops-standard`: CI/CD, containers, IaC, Kubernetes/GitOps, deployments,
  servers/cloud, observability, backup/restore, incidents and advanced Git/release
  work. Ordinary Git operations remain Harness/executor. Use conditional SDD
  validations with owner/capability/preferred_tool, not installation state.
  Operational approval requires target, impact, rollback and explicit human
  gates for production/destructive changes. Security retains IAM/secrets/TLS/
  firewall/public-port/privilege review and its scanners. If Environment is
  available in the runtime, it prepares prerequisites only. Both plugins are
  included in this repository; runtime availability/authentication must be
  checked separately, remaining NOT VALIDATED until evidenced. The bootstrap
  layer must not be duplicated.

- `sdd-spec-factory`: for COMPLEX work and NORMAL work whose behavior is not
  already specified. TRIVIAL work uses an inline intent contract.
- `ui-ux-standard`: whenever there is UI (screens, components, visual states,
  responsiveness, accessibility, design-system adherence).
- `security-standard`: whenever the change touches authentication, authorization,
  tokens, session, sensitive data, uploads, payments, or external integrations
  (also parsers, webhooks, infrastructure, privileged operations, tenant
  boundaries, secrets).

## Invariants

Kanban policy: Backlog -> Discovery / SDD -> Ready for Dev -> In Progress ->
Validation -> In Review -> Awaiting Final Approval -> Done. Validation is the
technical checkpoint; In Review requires a PR; the final column requires human
merge, not just a closed Issue or local COMPLETED receipt. Blocked is a label,
not a column. Preserve existing Project option IDs and values when adding stages.
At most three automatic rework cycles by default; then diagnosis and BLOCKED.

- CODE_COMPLETE != TASK_COMPLETE; NO_EVIDENCE != PASS.
- SECTOR_REQUIRED != OPTIONAL; OUTSIDE_OWNER != AUTHORIZED_TO_PASS.
- CONTEXT_AVAILABLE != CONTEXT_REQUIRED: every loaded source has a purpose.
- Harness reads the complete Task; specialists load their list/canonical JSON and
  REQUIRED sources, triggered CONDITIONAL sources, relevant code and receipts.
  OPTIONAL is never loaded automatically. The active SKILL.md remains mandatory.
- Missing REQUIRED source or source_of_truth_conflict blocks the checkpoint.
- Owners attest only their own sectors. Harness transcribes/reconciles evidence,
  never fabricates another skill's PASS. Required PENDING/BLOCKED/NOT_VALIDATED
  or PARTIAL sectors prevent completion; justified N/A does not block.
- Use the existing states/receipts; PASS maps to evidenced COMPLETED. Planning
  does not close final validation; materially stale evidence requires retest.

- `dev-workflow-standard` never writes product code and never skips the intent
  contract required by the change-complexity tier.
- `dev-implementation-standard` never implements without an approved task, and
  never changes anything out of scope without a recorded justification.
- Every new executable task points to a valid v2 Execution Contract normatively
  equivalent to its GitHub Issue. Legacy v1 tasks are normalized on demand.
- Every PR points to task, issue, branch and the specs it followed.
- Naming a skill never counts as applying it; every mandatory skill has a receipt.
- Assigning a task never counts as executing it; every delegated checkpoint has an `EXECUTION_RECEIPT`.
- A human Issue report communicates material progress but never replaces the
  receipt or validation. Every material comment records token usage and changed
  surface. Publication requires a returned comment URL/identifier.
- Consolidate small operations and never post an identical checkpoint report twice.
- `COMPLETED` requires inspectable result plus validation evidence.
- No new code unit is accepted without a reuse inventory and minimal-code gate.
- An unavailable LLM is replaced through `EXECUTION_HANDOFF`; the task is not restarted.
- No deploy is approved without an approved PR.

## Change-complexity tiers

The tiers control artifact depth, not validation quality:

| Tier | Typical scope | Minimum contract |
| --- | --- | --- |
| `TRIVIAL` | localized, low-risk, no behavior or contract change | inline scope, acceptance criterion, compact sector matrix with N/A reasons, validation and evidence |
| `NORMAL` | bounded behavior or multi-file change in known architecture | complete Issue/card plus equivalent v2 JSON; focused spec only for unspecified behavior |
| `COMPLEX` | architecture, migrations, security boundaries, substantial UI, integrations, unresolved decisions | collaborative SDD, reference/design libraries, complete Issue, equivalent v2 JSON, traceability, specialists, review gates |

Escalate when uncertain. Security and UI gates remain surface- and risk-based.

## Context compatibility

The GitHub Issue is the complete human card; JSON v2 is the equivalent normative
LLM contract. Mutable progress, evidence, logs and receipts remain in Issue
comments and ledgers. Legacy v1 contracts remain readable and are normalized
only when needed for resumed work. Exact schema and compatibility rules live in
the Harness [context-routing reference](../plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md).
This is a local documented agent protocol, not a new runtime policy engine.

## Provenance

Repository-first knowledge, progressive disclosure, real tool execution,
feedback loops, validation, and mechanical enforcement are consolidated
practices. The exact state names, receipts, specialist topology, Kanban columns,
and human gates are local Engineering Harness decisions or extensions.

## Platforms

The same pipeline runs on Codex Desktop, Claude Code and Antigravity. Each skill
ships the platform adapters (`.codex-plugin/`, `.claude-plugin/`, root
`plugin.json`) and a single canonical `skills/<name>/SKILL.md`. See the README
for installation per platform.
