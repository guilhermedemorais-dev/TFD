---
name: TFD-database
description: "Specify and implement approved schema, migrations, and data invariants."
metadata:
  version: "1.2.0"
  owner: "database"
---

# database

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md) to data contracts, migrations and scoped rework. Record consultation and disposable-data checks; independent backend QA verifies the current revision before its phase approval.

Model invariants with constraints and explicit transaction boundaries. Choose isolation and indexes from actual access patterns; inspect query plans before tuning. Check migration compatibility, concurrent writes and restore evidence where affected.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Inspect the current schema and transaction behavior. Specify ownership, constraints, retention, indexes, isolation, migrations and recovery. At G6, return the data contract and test plan. At G7, require approved scope, test the migration and rollback on representative disposable data, and test integrity and concurrent access. Report commands, exit codes, revision and limitations. Require separate authorization for production or destructive data changes. Hand off to backend QA.
