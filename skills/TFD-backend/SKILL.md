---
name: TFD-backend
description: "Implement approved API and domain behavior with reproducible self-tests."
metadata:
  version: "1.1.0"
  owner: "backend"
---

# backend

Use intention-revealing names, cohesive functions, explicit errors and stable API contracts. Apply DRY/SOLID where they simplify this change; avoid speculative abstractions. Test observable regressions, integration boundaries and relevant idempotency/races; coverage alone is insufficient.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Load the approved phase, relevant contracts and exact reference sections. Check allowed and protected paths. Add a failing regression where practical, implement the smallest complete change, and test normal, error, permission and relevant retry or concurrency paths. Preserve public contracts and version changes explicitly. Record actual commands, exits, revision, changed paths and unresolved limits. Send the result to independent backend QA; correct only scoped findings and resubmit the new revision.
