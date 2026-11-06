---
name: TFD-database
description: "Specify and implement approved schema, migrations, and data invariants."
metadata:
  version: "1.0.0"
  owner: "database"
---

# database

Inspect the current schema and transaction behavior. Specify ownership, constraints, retention, indexes, isolation, migrations and recovery. At G6, return the data contract and test plan. At G7, require approved scope, test the migration and rollback on representative disposable data, and test integrity and concurrent access. Report commands, exit codes, revision and limitations. Require separate authorization for production or destructive data changes. Hand off to backend QA.
