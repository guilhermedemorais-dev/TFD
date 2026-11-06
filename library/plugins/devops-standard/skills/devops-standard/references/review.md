# Operational review, independently authored

This process derives from the approved user requirements and local Harness
contracts, not from the restricted upstream devops-review material.

Scope the exact diff/revision, target, environment and requested review. Trace
trigger → credentials/context → command/action → affected resource → validation
and recovery. Read upstream/downstream controls before treating a suspicious
line as a defect. Do not expand a bounded review into unrelated operations.

Each candidate needs affected location/revision, observation/evidence,
preconditions, impact, recommended action, owner and validation method. Use
[finding](../templates/finding.md). Severity: CRITICAL, HIGH, MEDIUM, LOW, INFO.
Categories: Reliability, Security, Performance, Cost, Maintainability,
Operations, Compliance. Rate severity from actual impact/reachability; report
confidence separately. Scanner output is not confirmation.

Disposition every candidate: CONFIRMED, REJECTED or NOT_APPLICABLE with reason;
unresolved evidence remains NEEDS_VALIDATION. A confirmed fix retains initial
evidence and subsequent validation, not merely a changed checklist. Security
candidates go to security-standard, including its false-positive and external
publication rules. Do not publish unconfirmed vulnerabilities/counts.

On validation failure inspect output, identify cause, fix within approved scope,
rerun and compare initial/final evidence. Escalate external authority or scope
conflicts; do not suppress failing checks to claim PASS. Review output reports
coverage, findings/dispositions, command/exit evidence, unavailable checks and
remaining risk. Missing runtime evidence stays NOT VALIDATED. Harness owns
final gate review; this specialist cannot approve its own production change.
