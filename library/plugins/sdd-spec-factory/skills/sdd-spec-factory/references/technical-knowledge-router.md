# Technical Knowledge Router (consultative engineering references)

## Purpose and loading policy
Use this index only for NORMAL/COMPLEX tasks where a technical decision, affected boundary, or failure mode merits investigation. Never load every domain indiscriminately. Inspect the actual project, approved PRD, architecture, lockfile, ADRs, tests, and versioned documentation first. Reuse existing routing, security-standard, QA, DevOps and tool registry; this reference supplements, never overrides their ownership.

For applicable backend/library, payments/fiscal or commerce choices, consult
[Backend component sources](backend-component-sources.md) candidate metadata.
This supplements source selection; it is not another technical domain/topic.

For applicable blockchain/client/contract-development choices, consult
[Web3 component sources](web3-component-sources.md) candidate metadata.
This is source selection outside the unchanged technical-domain table.

## Evidence precedence
1. Existing application source, deployed behavior and explicit accepted project contracts (note conflict between code and docs).
2. Official version-matched specs and vendor documentation, official standards and maintained implementations.
3. Reputable implementations and technical literature, verified against first-party references.
4. Explicitly identified local decision or hypothesis.

For each material technical decision capture: question; affected code/contract; alternatives and tradeoffs; chosen approach; source URL + version/revision/date where available; concrete negative/positive test; rollback/observability where relevant; confidence (VERIFIED / ASSUMPTION / OPEN); owner and approval gate. Missing evidence NEVER becomes a made-up guarantee. Escalate blocking domain requirements to the owner. Cite short source pointers, not giant copied excerpts. Don't ingest secrets.

## Domain routing (activate only matched rows)
The files below are the canonical consultative library in this SDD bundle.
Load only matched references. Each carries decision questions, failure cases,
source pointers and owner boundaries; none establishes application facts.

| Trigger | Investigate | Consultative reference |
| --- | --- | --- |
| Algorithm, refactor, APIs, abstraction | complexity, immutability, coupling/cohesion, DRY/KISS/SOLID applicability, maintainability, error semantics, version compatibility | [Architecture](technical-architecture.md) |
| Service boundaries or changing modules | domain boundaries, modular monolith vs services, ADR, failure isolation, observability, compatibility, migrations | [Architecture](technical-architecture.md) |
| Persistence, inventory, checkout, payment | transactions, ACID, isolation level, atomic conditional updates, locks, idempotency, uniqueness, deadlocks, retries, reconciliation, data migrations | [Data and concurrency](technical-data-concurrency.md) |
| Auth, sessions, tokens, access | authentication vs authorization, OAuth/OIDC scopes, token lifetimes/rotation, secure cookie, race on refresh, CSRF, session invalidation, threat model, negative tests | [Auth and sessions](technical-auth-sessions.md) |
| Integration, API or webhook | HTTP semantics, schemas, pagination, timeouts, signatures, backoff+jitter, deduplication, idempotency, partial failures, compatibility | [APIs and jobs](technical-apis-jobs.md) |
| Queues, concurrent jobs, distributed state | at-least-once delivery, retries, ordering, poison messages, outbox, compensating actions, eventual consistency | [APIs and jobs](technical-apis-jobs.md) |
| AppSec, sensitive data, dependency change | threat model, validation, access control, secrets, dependency advisories, versioned ASVS controls, OSV and security-standard gating | [Quality and operations](technical-quality-operations.md) |
| Testing or bug fixing | reproducible failure, risk-based unit/integration/e2e, regression, property/negative test, flaky tests, evidence and independent QA | [Quality and operations](technical-quality-operations.md) |
| CI/CD, infrastructure, production release | least privilege, artifacts, rollout, rollback, backups, DR, logging, SLO, alerting, supply chain | [Quality and operations](technical-quality-operations.md) |
| Fiscal/legal regulated business logic | jurisdiction, product classification, tax parameters, official schemas, signature/certificates, rejection flows, homologation, audit trail | [Fiscal](technical-fiscal.md) |

## Integration with existing execution contracts
Resolve the active SDD bundle by runtime discovery or this explicit canonical
checkout. Harness routes to this single index; do not clone the library into
Harness, QA, Security or DevOps. A source path in this monorepo is not proof that
an installed host resolves it. Missing mandatory references stop the checkpoint.

SDD selects topics while specifying, then records project-specific, validated
sources under the existing `docs/biblioteca-referencias/` or module research
record. Use existing `references` IDs with `project_path`, `section`, `purpose`
and `applies_to`; route them through microtask `references`, sector
`required_sources`/`conditional_sources` and `execution_lists`. Do not add a
knowledge schema, registry, receipt type or installer. Preserve v1 compatibility.
Harness reads the complete Human Task and canonical v2 JSON; specialists read
their selected list, required canonical context and sources. Maintain normative
equivalence and contract_revision; mutable evidence stays in existing receipts
and Issue comments. Consult the active context-routing reference for transport.

Apply existing spec-consistency analysis to requirement -> microtask -> acceptance
-> verification/owner. A reference or test plan is not execution evidence.
In Review, Harness checks the Engineering Explanation against executed receipts,
current source revisions and each REQUIRED owner's result before human acceptance.

## Minimum impact-oriented contract
For each affected sector of the existing Human Task and equivalent JSON: link discovered source, identify applicable controls, acceptance criteria and explicitly executable positive/negative tests. Keep N/A with reason. Map requirement -> implementation microtask -> verification evidence. For the PR, include a concise human-readable Engineering Explanation: why this approach; what alternatives were considered; what might fail; what was actually tested; known limitations and pending human decisions. This is a report section, not a new mandatory competing Task/schema.

## Knowledge gaps and durable library updates
When a selected topic lacks a relevant pattern, has stale version evidence or
does not answer the current question, research and update the owning reference
as part of the authorized task. Do not repeatedly rediscover the same verified
information, or invent a pattern to finish a spec.

1. Search the existing project library and these conditional references first.
   State the unanswered question, affected version/boundary and why current
   evidence is insufficient. Check freshness against actual stack/API version,
   effective regulatory date or conflicting new evidence, not a made-up TTL.
2. Follow the existing Harness capability-registry research routing: discover
   suitable available documentation/code/extraction tools, then use the bounded
   official-source fallback when unavailable or insufficient. Record actual
   invocation and fallback reason. No tool installation is implied by research.
3. Read the original version-matched documentation/spec/source, not search
   snippets alone. Compare current code/contracts and alternatives. Classify
   established source behavior, LOCAL DECISION and ASSUMPTION separately. A
   researched example is not an approved architecture or proven runtime result.
4. Extend the existing topic record in `docs/biblioteca-referencias/` or module
   research file, avoiding duplicate entries. Include question/trigger, source
   URL and section, revision/version, checked date, purpose, applicability,
   supported claim, limitations and planned/executed validation distinction.
   Save bounded summaries, not copied manuals, secrets or customer data.
5. Link the exact updated record through the existing Task/JSON reference fields
   and revision rules. On subsequent tasks, reuse compatible evidence after a
   freshness/applicability check and load only that topic/section. Changed
   normative requirements need the existing approval/equivalence gate; a factual
   reference refresh does not itself expand scope or create another task.
6. For reusable cross-project learning, update/propose the owning plugin source
   under its existing review/release process. Reuse the active Harness
   `references/continuous-improvement.md` ownership/promotion rules; do not modify
   installed caches, export client-specific rules, or install new capabilities
   as a side effect. Pure factual research uses the reference library, not a new
   skill/registry/evaluation ceremony. Human merge gates remain intact.

If evidence conflicts, preserve the old provenance and record the conflict;
stop the affected decision rather than silently replacing approved rules. If
sources are unavailable, save the gap as NOT VERIFIED and block only decisions
whose correctness depends on it. A pending search is never learned knowledge.

## Stop conditions
- Unverified regulatory/business logic, critical authorization gap, destructive migration without rollback, or unresolved architecture conflict: BLOCKED until decision.
- Unavailable docs/tool or inconclusive advisory: mark NOT VERIFIED and use safest non-invented fallback or block based on impact.
- Scanner PASS or AI code review is not proof of security. Human acceptance and existing Harness gates remain intact.
- Do not prescribe an exhaustive pattern catalog as mandatory. Applying every concept by default increases cost and introduces accidental complexity.

## Verification examples
- Concurrent last-unit checkout: test two parallel purchases and assert exactly one inventory reservation; distinguish paid from reserved, verify rollback/idempotency on timeout.
- Login and token refresh: test expiry, rotation, revocation, concurrent refresh, authz cross-user denial, secret storage and audit behavior.
- Fiscal integration: test schema reject, transport retry, duplicate document, cancellation, reconciliation and jurisdiction-specific rules with approved expert input.
