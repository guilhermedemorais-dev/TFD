# Advanced Git and release

Routine status, diff, fetch, normal commit and PR handling remain Harness/executor
operations. Invoke DevOps for release branches/policies, tags/artifact promotion,
history rewriting, recovery and GitOps consequences.

Inspect branch, HEAD, upstream, dirty state and remote references. Preserve
uncommitted changes; do not auto-stash or overwrite them. Record source commit,
immutable artifact identity, version/tag policy and release notes. Verify tag
target and existing remote tag before a proposed publication.

History rewriting needs a precise affected-ref inventory and recovery reference.
Force push and destructive reset require explicit human approval, even with
force-with-lease. Do not retag a published release without an approved policy.
Revert is often safer for shared history but may trigger deployment: inspect
automation before pushing. Tag/release creation is an external mutation and
must be in scope. Validate release checks and post-publication remote identity;
successful push alone does not prove deployment health.
