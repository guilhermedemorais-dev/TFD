# Incident response

Operate within explicit incident scope: observe → contain → restore service →
investigate → correct root cause. Record timeline, impact, current artifact,
signals and confidence before changes; preserve logs and other evidence.
Do not delete logs, disable alerting or execute destructive probes to make the
symptom disappear. Suspected security incidents require security-standard.

Choose the smallest authorized containment with known blast radius/recovery
path. Incident urgency does not automatically authorize reboot, firewall/DNS
changes, production deployment, secret rotation or destructive restoration.
Escalate when those gates have not been approved.

After service recovery verify representative behavior and monitoring over an
agreed observation window. Mark mitigation separately from a confirmed root
cause and permanent fix. Reproduce safely with fixtures/staging when possible,
add regression checks and assign follow-up owners. Preserve uncertain causes
as hypotheses; do not close the incident's engineering follow-up from a green
health endpoint alone.
