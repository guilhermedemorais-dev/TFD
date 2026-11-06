# DevOps operating model

Local Engineering Harness extension. Preserve the task/spec as authority and
the existing SKILL_RECEIPT, EXECUTION_RECEIPT and EXECUTION_REPORT_COMMENT.

Before mutation identify target, environment, account/context, resource IDs,
current artifact/config, protected persistent data and the allowed change.
Inspect existing repository commands and platform configuration before choosing
a tool. Discovery of infrastructure is not permission to operate it.

Prepare a change using [operational-change](../templates/operational-change.md).
Describe blast radius, backup need, rollback trigger, rollback limitations,
health criterion and observation window. Separate validation commands from
mutation commands; no apply, destroy, sync, deploy or restore disguised as a
syntax check. If safe rollback is unavailable, escalate explicitly.

Human authorization must identify operation and exact target, including
production deploy, destructive migration, firewall, destructive DNS, IaC
apply/destroy, force push, destructive reset, production DB restore, cluster
deletion, reboot and secret rotation. Check authorization immediately before
the operation, not merely once when starting the task.

Use the shared helper's compatible cached state; detect/verify when missing or
stale. Install only the selected necessary tool via approved official method,
with reviewed scope/privileges. Never install the whole registry or silently
use sudo. Record failed installation without identical retry loops. Missing
Environment Bootstrap in the active runtime means preparation through the
current supported helper only. When available, delegate selective prepare/repair
to Environment, then resume DevOps; do not duplicate its bootstrap layer.

Review infrastructure trust boundaries with security-standard. Keep scanners
and their findings with that owner. MCP discovery/configuration is not connected
or authenticated status. Select an authorized CLI/API fallback only if it
satisfies the same contract; otherwise return an actionable blocker.

FAIL → analyze → fix in scope → revalidate → evidence. Stop for new authority,
architecture/scope conflict, persistent tool failure or missing mandatory skill.
Do not turn a static pass into a runtime or production claim. Templates and
examples do not constitute execution evidence.
