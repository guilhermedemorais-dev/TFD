# Backup and disaster recovery

Use [backup/restore plan](../templates/backup-restore-plan.md), adapted from the
audited MIT HA/DR template. Define protected data, owner, RPO/RTO, retention,
encryption/access, backup location and exact restore destination before acting.
Do not assume replication replaces a recoverable independent backup.

Distinguish evidence states: BACKUP_CREATED means creation/integrity evidence
exists; RESTORE_NOT_VALIDATED means restoration/application behavior has not
been tested; RESTORE_VALIDATED requires an observed isolated restore with data
integrity and representative application checks. These are evidence labels,
not new Harness lifecycle states. Never equate a successful archive command or
snapshot listing with restore validation.

Prefer isolated restore using synthetic or properly authorized protected data.
Measure actual recovery time and recovered point; verify schema, integrity,
application behavior and backup-specific checks. Do not promote replicas,
overwrite production, redirect traffic or delete old backups during a drill
without separate explicit approval. Production database restore requires its
human gate and recovery/rollback limitations stated in advance.

Preserve original backup/evidence and active monitoring. Redact private data
from reports, retaining only identifiers/check results appropriate to the task.
