# Architecture and implementation decisions

## When to consult
Use for changing module boundaries, introducing abstractions, replacing legacy
code, algorithms, or performance work. This is a consultative checklist, not a
mandatory architecture. SDD owns the decision record; implementation owns code.

## Repository evidence first
- Locate callers, public contracts, dependency direction, existing ADRs,
  language/framework versions, tests and deployment topology.
- Record concrete reuse candidates and constraints in REUSE_INVENTORY. A new
  interface, service or helper needs the existing minimal-code gate, not a
  fashionable pattern name.
- Identify the invariant and failure before proposing SOLID, DRY, CQRS,
  event sourcing, a modular monolith or microservices. None is a default.

## Questions and alternatives
- Can a local function/module extension satisfy the current consumers? Compare
  it with a new abstraction using actual coupling and change frequency.
- Is a boundary logical or independently deployed? Compare ownership, release
  cadence, data transactions, latency, operational cost and failure isolation.
- What input sizes and latency/memory budgets are observed? Evaluate complexity,
  indexes, pagination or caching against measured workloads before optimizing.
- Where do validation and errors belong? Trace boundary validation, internal
  invariants, typed errors and user-visible failure contracts through callers.
- For caches, specify source of truth, key scope, invalidation, staleness budget
  and behavior on cache failure. Never use cache consistency as inventory truth.
- Preserve compatibility during refactors. Prefer a bounded replacement with
  characterization tests over an unrelated rewrite.

## Verification to put in existing specs
Require a positive normal-input case, malformed/boundary inputs, compatibility
tests for actual callers, and representative performance checks when a budget
is approved. Record measurement environment and baseline. Tests passing cannot
prove unmeasured scalability. Define rollback and telemetry for risky changes.

## Sources and ownership
Read the actual language/framework documentation at the lockfile version and
the project's ADRs. No stack is assumed here. Reuse the active Harness
`references/minimal-code-gate.md` and implementation SKILL, resolved from their
active bundles or an explicit canonical checkout, never guessed cache paths.
The checklist and tradeoff record are LOCAL DECISIONS extending existing SDD;
pattern adoption requires evidence for this project, not citation by name.
