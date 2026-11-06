# Deployments and rollback

Identify platform, environment, service, current and proposed artifact/config,
dependency ordering, maintenance constraints and protected state. Reuse native
deployment commands and current rollout strategy; do not impose Kubernetes or
cloud migration on a Compose/Portainer/Coolify project.

Before release establish readiness criteria, baseline health, representative
service path, observation window, rollback trigger and rollback_strategy.
Database/schema compatibility may require roll-forward rather than rollback;
explicitly flag irreversible changes before approval. Backup existence does
not make a destructive migration reversible.

Run static checks and authorized staging validation first. Production deploy
requires approved PR and explicit human approval for the target/operation.
Capture resulting immutable artifact identity and verify health and service
behavior after deployment. Monitor agreed thresholds, not merely process exit.
Stop/rollback only within the approved recovery scope; otherwise escalate.
Report deployment, runtime health and rollback testing as separate outcomes.
