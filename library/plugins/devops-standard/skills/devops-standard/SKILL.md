---
name: devops-standard
description: "Operate and review GitHub repository governance, CI/CD, containers, infrastructure, releases, servers, cloud, observability and recovery under an approved Engineering Harness task. Use for operational changes, not ordinary application coding or routine Git status, commits and PRs."
---

# DevOps Standard

Receive one prompt per execution list, linking the Task's single JSON file
and selecting its `execution_lists` entry by `list_id`, never per item/subitem.
All lists live in that file; do not expect JSON inside the Human Task/prompt.
Read the list JSON and relevant canonical JSON fields, not Human Task sections
as execution input. Require current Harness evidence of full card/JSON normative
equivalence, tied to the contract revision and observed Issue update time.
Missing/stale evidence or divergence returns to Harness before execution.

Specialist companion to `dev-workflow-standard`, not a second Harness. Read
this skill completely, emit `SKILL_RECEIPT`, validate the approved task and
Execution Contract, then load only the references needed for that checkpoint.
Source adaptation and local extensions are documented in [ORIGIN](references/ORIGIN.md).
For v2, validation includes task identity, contract revision and **normative equivalence**
of the routed operational slice using the current Harness comparison receipt. Execute only routed
DevOps/observability microtasks; any divergence returns to the Harness.

## Responsibility boundaries

- `qa-testing-standard` validates functional product behavior; DevOps validates
  operational runtime, health, CI/CD, rollback and reliability. A service health
  check is not functional QA. Environment prepares missing tools, not production
  infrastructure. Preserve shared tool owners and return only your own PASS.
- For sector routing, load the list JSON, relevant canonical JSON global constraints,
  required sources with purpose, triggered conditionals and material receipts.
  Do not load the Human Task as execution input or optional sources by default. Read this SKILL.md
  and the active operational references fully. Resolve context-routing from the
  active Harness or explicit canonical checkout; missing required sources or
  source conflicts block. Planning may precede the final runtime artifact, but
  cannot fulfill its dependent validation gate or authorize production changes.

- Harness owns scope, delegation, lifecycle, review and human gates.
- DevOps owns operational design, bounded execution and validation of CI/CD,
  infrastructure, servers, release and recovery procedures, including GitHub
  repository settings, Projects, labels, rulesets and repository readiness.
- `dev-implementation-standard` owns application code and ordinary executor
  validation. Routine Git status/diff/fetch/commit/PR stays with Harness/executor;
  release policy, tags, advanced history operations and GitOps route here.
- `security-standard` retains AppSec, SAST/DAST and security scanners. Mandatory
  handoff for IAM, secrets, TLS, firewall, public ports, privilege, authentication,
  sensitive storage and cloud permissions; do not self-certify security findings.
- `ui-ux-standard` owns visual work, never infrastructure operations.
- `dev-environment-standard` (Environment Bootstrap), when actually available in the selected base/runtime,
  detects/prepares tools and MCPs, never operates production. Both plugins are
  included in this repository; host preparation and authentication remain
  **NOT VALIDATED** until evidenced in the target runtime. Do not
  recreate it, its MCP Library, or claim preparation proves authentication.
  When available, route missing/broken prerequisites to selective prepare/repair,
  then resume the original DevOps checkpoint; do not run full doctor per task.

## Operational contract

1. Identify project-native commands, architecture, target environment/account,
   exact resource and protected data. Preserve existing Coolify, Portainer,
   Compose, VPS or cloud choices unless migration was approved.
2. Classify capability and risk. Choose the smallest viable toolchain; a cloud,
   Kubernetes, GitOps, Terraform or a new platform is never mandatory by default.
3. Read [operating model](references/devops-operating-model.md) and the relevant
   domain reference. Record baseline, bounded plan, required validations,
   `rollback_strategy`, health criteria and explicit authorization when needed.
4. Resolve available tooling through [tool-registry.json](references/tool-registry.json)
   and the existing Harness `skill-owned-tools.md` protocol. Use its
   `scripts/tool-state.py` helper, never a parallel installer. Registry entries
   are candidates, not a bulk installation request. Use Terraform **or** OpenTofu
   according to the project; `act` is optional.
5. Execute only approved scope. Validate static configuration, then authorized
   target behavior and representative service health separately. A successful
   lint/build/plan is not evidence of deployment or runtime health.
6. On FAIL: inspect output, confirm context and cause, correct within scope,
   revalidate and retain initial/final evidence. Escalate persistent failures,
   credentials, privileges or scope changes; never manufacture PASS.
7. Review candidates using [review](references/review.md). Return the existing
   `EXECUTION_RECEIPT`, update the Human Task and supply a factual
   `EXECUTION_REPORT_COMMENT` for the Harness. No new receipt type or state machine.

Existing states remain PENDING → READY → RUNNING → VALIDATING → COMPLETED,
with REWORK or BLOCKED when appropriate. Completion needs observed results and
required validation, not assignment, installed tooling or generated commands.
Record unavailable/unexecuted validation as **NOT VALIDATED**.

## Human safety gates

Explicit human approval is required before production deploy, destructive
migration, firewall change, destructive DNS change, IaC apply/destroy, force push,
destructive reset, production database restore, cluster deletion, reboot or
secret rotation. Task approval to create/edit configuration does not authorize
those operations. A merge into a reconciled GitOps branch may itself deploy.

Before any material-risk operation, record target/environment, impact, protected
data, `rollback_strategy`, trigger and post-change validation. If safe rollback
is impossible, say so and escalate before execution. Rollback is itself an
operation, not blanket authorization for unapproved destructive restoration.
Preserve backups, evidence and logs; never expose credentials/customer data in
templates, API tests, remote tools, command output or receipts.

## Progressive domain routing

For client portal onboarding or Pages preparation, read the active Harness
`references/client-portal.md` (in this monorepo:
`plugins/dev-workflow-standard/skills/dev-workflow-standard/references/client-portal.md`).
Resolve the active bundle or explicit canonical checkout, not a guessed sibling
cache path. Prepare `docs/portal/` in the client project from the separately
supplied template only when available; an absent future repository is a portal
dependency, not a global onboarding blocker. Do not invent the template or a
deploy workflow. Preserve existing files, use the client's database via its
authorized backend, and distinguish static Pages output from private services.
Follow the existing human gates before publication or remote configuration.

| Active need | Read |
| --- | --- |
| repository governance/bootstrap, GitHub settings, Rulesets, Project, labels, Issue/PR templates or readiness | [GitHub governance](references/github-governance.md) |
| advanced Git, release policy, tags | [git-release](references/git-release.md) |
| pipeline configuration and validation | [ci-cd](references/ci-cd.md) |
| Dockerfile, image, Compose, container health | [containers](references/containers.md) |
| rollout, promotion, rollback | [deployments](references/deployments.md) |
| host configuration and Ansible | [server-operations](references/server-operations.md) |
| Terraform/OpenTofu lifecycle | [infrastructure-as-code](references/infrastructure-as-code.md) |
| Kubernetes, Helm, Kustomize | [kubernetes](references/kubernetes.md) |
| Argo CD / Flux reconciliation | [gitops](references/gitops.md) |
| account, region, cost and cloud controls | [cloud](references/cloud.md) |
| metrics, logs, traces, alerting | [observability](references/observability.md) |
| backup integrity and restore drill | [backup-disaster-recovery](references/backup-disaster-recovery.md) |
| containment, recovery and root cause | [incident-response](references/incident-response.md) |

Reusable task artifacts: [operational change](templates/operational-change.md),
[CI/CD plan](templates/ci-cd-plan.md), [backup/restore plan](templates/backup-restore-plan.md)
and [finding](templates/finding.md). Templates are planning aids, not executable
permission. Copy only the applicable fields into the project's existing docs.

## Evidence handoff

Include capability, target environment, artifact/revision, planned/used tool,
official repository, observed version, state source, installation performed,
commands and exact exit codes, initial result, confirmed/rejected findings,
corrections, final result and validation evidence. Link sanitized artifacts,
rollback status, blockers and next safe action. Distinguish static validation,
target reconciliation, runtime health and restore/rollback evidence.

Resolve shared Harness references/helper from the active installed Harness
bundle or this repository, not an assumed sibling plugin cache. Keep local
`runtime-state/tool-state.json` ignored. A read-only bundle uses the helper's
paired `TOOL_REGISTRY_PATH` and `TOOL_STATE_PATH` overrides to a writable runtime
location. No runtime paths, secrets or machine state belong in the task contract.

For repository onboarding, use the governance helper's diagnose → propose →
human confirmation → apply → verify flow. Diagnose/propose/verify are read-only;
apply requires the reviewed proposal and explicit confirmation for its exact
target. Environment prepares missing git/gh; the developer authenticates through
gh's secure flow, never tokens in chat. Resume that checkpoint after auth.
Recheck for drift or a material change, not full bootstrap before every Task.
PROJECT READY != PRODUCTION AUTHORIZED; configured != enforced.
