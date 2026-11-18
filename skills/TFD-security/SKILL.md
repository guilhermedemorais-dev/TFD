---
name: TFD-security
description: "Assess applicable threats, permissions, data exposure and verification for the approved change."
metadata:
  version: "1.2.0"
  owner: "security"
---

# security

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md), distinguishing author and independent-review roles. Record your own canonical-source consultation and negative checks. At release review assess the exact candidate, target and recovery evidence; an earlier security PASS does not authorize a changed deployment.

Separate authentication from authorization and test denied actions at the real boundary. Use version-matched security guidance for applicable threats; verify secret handling, rate limits and dependency risks without treating a checklist as proof.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Trace assets, identities, roles and trust boundaries. Check access control, tenant isolation, input handling, secret storage, dependencies, logging and sensitive data. Assess applicable abuse cases and severity with evidence. Test scoped negative cases on authorized nonproduction targets. Record commands, exits, revision and limitations. Return unresolved findings for rework; a scanner result alone cannot prove safety.
