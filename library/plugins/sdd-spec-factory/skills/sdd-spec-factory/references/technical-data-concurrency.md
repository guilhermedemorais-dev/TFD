# Data integrity and concurrency

## When to consult
Use for persistence, stock, checkout, payments, migrations, imports, or concurrent
updates. SDD specifies invariants; implementation owns DB/backend; QA independently
verifies behavior. Route sensitive/payment surfaces to Security as already required.

## Inspect and decide
- Read schema, constraints, money representation, tenant keys, transaction
  boundaries, DB/driver versions and existing reconciliation jobs.
- Define authoritative state and invariants: available versus reserved versus
  paid stock, nonnegative quantities, unique provider events, currency/rounding,
  and which transitions are legal. Ask the product owner for unknown rules.
- Compare atomic conditional updates, row locks, optimistic version checks and
  serializable transactions against the actual invariant and DB semantics.
  A read followed by an unchecked write is not a concurrency strategy.
- State isolation level, conflicts, deadlock/serialization failure handling,
  retry bounds and transaction scope. Never hold a DB lock during a remote
  payment call without an explicitly justified design.
- Specify idempotency key scope, request fingerprint, durable result, concurrent
  duplicate behavior, retention and changed-payload rejection. Check existing
  provider semantics; an HTTP retry does not imply duplicate safety.
- For query work examine actual plans/cardinality and N+1 access before adding
  indexes. Specify uniqueness/null semantics and validate tenant isolation.
- For migrations define compatibility window, backfill/checks, lock impact,
  restore or forward repair, and handling of irreversible transformations.

## Verification example: last-unit checkout
Given approved no-backorder semantics and stock=1, start two independent DB
transactions with a synchronized race, not two sequential mock calls. Assert
exactly one committed reservation, no negative stock and one rejected purchase.
Replay the winning request; assert no second reservation. Simulate payment
timeout and late success, then cancellation/reconciliation using approved
transitions. An unknown provider result stays unresolved until queried, not
automatically failed or refunded. Test a crash after commit but before response.
Record which DB/version and isolation level ran; SQLite/in-memory substitutes
do not prove the production DB's locking behavior.

## Verification and recovery
Test rollback after partial writes, duplicate imports/events, deadlock retry,
cross-tenant IDs and migration on representative synthetic data. Define audit
events and reconciliation metrics without credentials/customer payloads. Restore
checks belong to DevOps, not a promised reversible migration by assumption.

## Primary sources
- [PostgreSQL 18 transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html)
- [PostgreSQL 18 locking](https://www.postgresql.org/docs/18/explicit-locking.html)

Checked 2026-10-11. PostgreSQL is an example, not the prescribed engine: its
Read Committed updates recheck predicates after concurrent modification; higher
isolation can require retrying the whole transaction. Verify the selected DB's
versioned documentation before transferring that behavior to another engine.
The checkout scenario is a LOCAL TEST DESIGN, not application execution evidence.
