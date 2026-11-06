# GitOps

Use Argo CD or Flux only where the project uses or approves it. Map repository,
branch/path, reconciler, cluster, namespace, sync/prune/self-heal settings and
current revision. A Git push/merge may reconcile production immediately, so
normal Git transport does not exempt deployment from its human gate.

Validate rendered manifests/configuration and controller-version compatibility;
inspect diffs and prune consequences. Select read-only native status/diff
commands after confirming context. Sync, reconcile, suspend/resume and rollback
may mutate systems and require the approved target/operation. Do not trigger
them to check syntax. Artifact promotion uses reviewed immutable identities.

Avoid editing live resources behind an active reconciler without an approved
incident plan: the controller may undo the change. Record desired revision,
observed revision, health and drift separately. Reverting Git is not proven
recovery until reconciliation and service health are validated. Do not invent
another MCP server/catalog to drive the controller.
