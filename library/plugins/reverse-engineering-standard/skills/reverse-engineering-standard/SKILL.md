---
name: reverse-engineering-standard
description: "Use for authorized reverse engineering of shipped software, binaries, Electron/JavaScript apps, managed assemblies, APKs, firmware or runtime behavior when source is unavailable or insufficient. Produces evidence-first findings and reconstruction guidance; does not replace SDD, implementation, QA or security ownership."
---

# Reverse Engineering Standard

Own authorized reverse-engineering investigations inside the Engineering Harness.

Use this skill when the answer depends on behavior or structure of a shipped
artifact rather than an ordinary source repository. For normal source analysis,
use repository/code tools and do not invoke REA merely because it exists.

Read [rea-integration.md](references/rea-integration.md) whenever reverse
engineering runtime capabilities are used. Consult
[tool-registry.json](references/tool-registry.json) for tool ownership and use
the bundled reverse-context gateway as the normal execution boundary.

## Preconditions

Before analysis:

1. Identify the target artifact/app and authorized scope.
2. Confirm the task/list and current revision when running under the Harness.
3. Read this SKILL completely and emit the normal SKILL_RECEIPT.
4. Separate what may be inspected from what must not be executed or mutated.
5. Resolve the smallest analysis capability required.

If target authorization is unclear, stop before active/runtime inspection.

## Workflow

1. Establish the question to answer, target identity and evidence required.
2. Reuse existing source, docs, symbols, analysis sessions and evidence before
   opening a new investigation.
3. Use the bundled reverse-context gateway for runtime capability discovery and
   execution. The gateway may invoke the pinned REA runtime and its providers;
   the specialist owns methodology and interpretation.
4. Prefer static analysis first when it can answer the question.
5. Use runtime observation only when needed and authorized.
6. Keep a finding ledger with OBSERVED, INFERRED and UNKNOWN claims.
7. Tie every material conclusion to inspectable evidence and limitations.
8. If reconstructing a feature, describe behavior, state, inputs/outputs,
   protocol, constraints and unknowns without copying proprietary implementation.
9. Hand reconstruction requirements to SDD. Implementation remains owned by
   dev-implementation-standard.
10. Return EXECUTION_RECEIPT evidence to the Harness and do not self-approve
    downstream QA/Security/UI/DevOps gates.

## Safety and legal boundary

Operate only on systems, software and artifacts the user owns, controls or is
authorized to inspect. Defensive interoperability, compatibility, migration,
research and feature reconstruction are valid uses.

Do not:
- steal credentials, secrets or personal data;
- create persistence, malware, covert access or evasion;
- attack third-party services;
- bypass licensing/DRM for unauthorized access;
- run destructive payloads against production;
- present proprietary source recovered from an artifact as newly authored code.

When the requested outcome is a compatible implementation, write an independent
spec from observed behavior and build new code through the normal Harness flow.

## Relationship with other skills

- sdd-spec-factory converts validated findings into product/technical specs.
- dev-implementation-standard writes the independent implementation.
- qa-testing-standard validates reconstructed behavior.
- security-standard owns AppSec findings and vulnerability claims.
- devops-standard owns deployment/infrastructure implications.
- dev-workflow-standard owns final routing, handoff and gate reconciliation.

Reverse engineering evidence does not grant permission to change the Task scope.
