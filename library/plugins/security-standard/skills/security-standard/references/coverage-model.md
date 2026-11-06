# Coverage Model

Security coverage is measured across attack surfaces, application layers, and
control families. File counts alone do not demonstrate meaningful coverage.

## Attack Surfaces

Evaluate applicability and priority for:

- public web and API entry points
- authentication, sessions, recovery, and identity federation
- authorization, tenant isolation, and privileged operations
- admin, support, impersonation, and internal tooling
- inbound webhooks, queues, events, and scheduled jobs
- outbound HTTP, callbacks, redirects, and server-side fetches
- uploads, downloads, archives, media, and object storage
- parsers, serializers, templates, expressions, and protocol handlers
- imports, exports, reports, search, and bulk operations
- payments, billing, credits, and irreversible business actions
- secrets, cryptography, signing, and key lifecycle
- logs, metrics, traces, errors, analytics, and support artifacts
- dependencies, build tooling, CI/CD, packages, and release artifacts
- containers, hosts, cloud/IAM, networks, databases, caches, and backups
- browser storage, DOM rendering, service workers, and third-party scripts

## Layers

Report coverage separately for:

- `Banco`
- `API/Backend`
- `Frontend/UI`
- `Infra/DevOps`
- `Dependencias/Supply Chain`
- `Privacidade/Observabilidade`

## Control Families

Track relevant controls:

- identity and session lifecycle
- authorization and object ownership
- tenant and environment isolation
- input constraints and canonicalization
- output encoding and content policy
- query, command, template, and expression safety
- filesystem and network destination safety
- message authenticity, replay, idempotency, and ordering
- secret and key management
- encryption and integrity protection
- resource limits and abuse resistance
- auditability, detection, and recovery
- dependency provenance and update safety
- data minimization, retention, deletion, and export controls

## Coverage Ledger

For scoped and repository audits, maintain a table:

| Surface ID | Surface | Layer | Risk | Entry Points | Controls | Files/Routes | Owner | Status | Evidence/Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed status values:

- `PENDING`
- `IN_REVIEW`
- `REVIEWED`
- `NOT_APPLICABLE`
- `DEFERRED`
- `BLOCKED`

`REVIEWED` requires evidence, not merely a search hit. `DEFERRED` and `BLOCKED`
must state impact on assurance and the exact next action.

## Change Impact Expansion

For diff review, begin with changed files and expand only when the change:

- modifies a shared guard, parser, serializer, query builder, or policy helper
- changes configuration used by multiple entry points
- alters schema or identity fields consumed elsewhere
- changes dependency versions, build scripts, permissions, or runtime defaults
- creates a new route to an existing sensitive effect

Record why each supporting file entered scope.

## Blind-Spot Register

Report unavailable or incomplete evidence, including:

- runtime not available
- production-equivalent configuration unavailable
- generated or vendored code excluded
- external service behavior not testable
- encrypted, binary, or inaccessible artifacts
- scanner failure or unsupported language
- missing architecture, ownership, or data-classification documentation

Blind spots reduce `SECURITY_STATUS` unless repository evidence proves they are
irrelevant to the requested scope.
