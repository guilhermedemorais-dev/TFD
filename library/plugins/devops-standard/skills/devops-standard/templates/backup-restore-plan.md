# Backup and restore plan

Adapted from Vasiliy Uvarov's MIT HA/DR Template. See
[ORIGIN](../references/ORIGIN.md) and the bundle's THIRD_PARTY_NOTICES.md.
No failover, production restore or traffic changes are authorized by this form.

## Overview and continuity objectives

- System/service / owner / environment / protected data:
- Business impact and criticality:
- RTO, maximum recovery duration:
- RPO, maximum acceptable recovery-point loss:
- Last observed restore test and evidence, or NOT VALIDATED:

## Recovery design

| Component | Backup/replication method | Recovery destination | Owner |
| --- | --- | --- | --- |
| Application | | | |
| Database | | | |
| Storage/configuration | | | |

Document only the existing/approved topology. Multi-region or Kubernetes is not
required. Record backup type/frequency, retention, encryption/access and offsite
or independent recovery copy where applicable. Replication alone is not proof
of recoverability after corruption/deletion.

## Isolated restore procedure

1. Identify and verify the backup artifact; preserve its original copy.
2. Confirm isolated destination, authorization, capacity and protected data rules.
3. Restore the selected artifact; replay logs/PITR only if scoped and supported.
4. Validate integrity, schema, expected records and representative application behavior.
5. Measure elapsed recovery time and recovered data point against RTO/RPO.
6. Preserve sanitized evidence and document gaps/remediation owners.

Do not promote to primary, overwrite production, redirect DNS/traffic, disable
production alerts or delete backups as an automatic drill step. Those operations
need their own explicit approval and recovery plan.

## Post-restore verification

- [ ] Data integrity checks match the intended recovery point.
- [ ] Application health and representative service path verified.
- [ ] Relevant background jobs/dependencies assessed without unintended effects.
- [ ] Monitoring remains active and evidence is retained.
- [ ] Recovery objectives measured; failed checks analyzed and revalidated.

## Evidence status

- BACKUP_CREATED, creation and integrity evidence:
- RESTORE_NOT_VALIDATED, outstanding restore/application checks:
- RESTORE_VALIDATED, observed restore plus integrity and application evidence:
- Production restore approval: absent unless specifically recorded.
- rollback_strategy and irreversible limitations:
- Next safe action / owner:

Select statuses from evidence, not intention. A backup creation result cannot
be presented as a validated restoration.
