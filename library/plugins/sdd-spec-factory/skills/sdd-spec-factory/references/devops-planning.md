# Conditional DevOps planning

Read only for operational work: CI/CD, containers, IaC, Kubernetes, GitOps,
deploy, servers, cloud, observability, backup/restore, incidents or advanced
release strategy. The Harness invokes `devops-standard`; SDD does not perform
the operation. Ordinary application code, UI copy and a normal commit/PR do
not require DevOps unless an operational surface actually changes.

## Intent before commands

In the existing spec and Human Task identify the current platform, target
environment, protected resources/data, desired change, impact/blast radius,
owner, validation plan, rollback_strategy and human approval checkpoints.
Use the project's native platform, including Compose, Coolify, Portainer or
managed hosting when present. Do not add a cloud or Kubernetes requirement.
If the target is unknown, planning can proceed but execution is blocked.
If rollback is impossible, record why and the recovery/forward-fix alternative;
do not pretend a database restore is always a safe rollback.

Required validations belong to domain owners. Examples below are conditional,
not entries to insert into every contract:

| Changed surface | Owner | Capability | Preferred tool |
| --- | --- | --- | --- |
| GitHub Actions workflow | devops-standard | github-actions-validation | actionlint |
| Compose configuration | devops-standard | compose-validation | docker-compose |
| Terraform config | devops-standard | infrastructure-validation | terraform |
| OpenTofu config | devops-standard | infrastructure-validation | tofu |
| Kubernetes manifests | devops-standard | kubernetes-schema-validation | kubeconform |
| Ansible playbook | devops-standard | ansible-validation | ansible-lint |
| Prometheus rules | devops-standard | prometheus-rule-validation | promtool |
| IAM/secrets/TLS/public network/privileges | security-standard | security-review | project-approved scanner if applicable |

Reuse `required_validations` entries shaped as
`{"owner":"devops-standard","capability":"github-actions-validation","preferred_tool":"actionlint"}`.
Resolve the actual IDs from the current owner registry before emitting a
tool-backed contract entry. A specialist review capability such as
`security-review` can omit `preferred_tool`: it is not an invented scanner ID.
The initial catalog is not closed. Database restore and other uncovered needs
must resolve the actual project-native tool and verify it before execution;
do not substitute an unrelated catalog tool or invent availability.
No install commands, executable paths, URLs or runtime state in JSON.
Keep detailed commands, expected results, conditional steps and evidence in
spec/task; do not invent another contract schema or receipt.

For production/destructive changes require explicit human approval of exact
target, operation and rollback. Production deploy, destructive migrations,
firewall, destructive DNS, IaC apply/destroy, force push/reset, production DB
restore, deleting clusters, reboot and secret rotation cannot be validation
defaults. Separate static checks, read-only target checks, isolated runtime
tests and approved mutations. A saved plan or CLI exit 0 is not deploy health.

## Environment dependency

Resolve `dev-environment-standard` only when actually present. If present,
delegate missing/broken prerequisites to selective prepare/repair; DevOps
retains operational responsibility. Both plugins are included in this repository,
but runtime availability must be checked; the existing tool-state helper is the
fallback when Environment is unavailable.
Do not duplicate Environment, a MCP Library or installation state. Installation
is not proof of connection/authentication or a successful target operation.

## Planning examples

- Request: change button wording. Outcome: implementation/UI only; DevOps N/A.
- Request: commit an approved change. Outcome: Harness/executor Git; DevOps N/A.
- Request: add a GitHub Actions workflow. Outcome: DevOps github-actions-validation plus
  security when permissions/secrets/external actions are affected.
- Request: restore production database. Outcome: DevOps + security, target and
  explicit approval required; isolated restore verification planned first.
