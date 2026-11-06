# Containers

Preserve the current Docker/Compose/Coolify/Portainer architecture. Identify
Docker context/daemon and exact containers/images/volumes before any operation;
local CLI does not imply a local daemon. Never delete persistent volumes or
prune the host to fix a build without separate target-specific authorization.

Validation sequence: inspect Dockerfile/Compose, `hadolint Dockerfile`, approved
`docker build`, `docker compose config --quiet`, then isolated smoke/health.
Build steps execute code and can access network/secrets; review inputs first.
Use disposable synthetic data, bounded resources and loopback ports when a
local runtime test is authorized. Avoid privileged containers and host mounts.
Compose config may interpolate secrets; prefer quiet validation and sanitize
any diagnostic output. Build/config success does not prove service health.

Verify entrypoint, non-root compatibility, actual health endpoint, resource
limits, image digest and mounted storage permissions. Route image scanning,
secrets and security hardening to security-standard; do not duplicate its tools.
Push/recreate/restart/deploy are mutations, not validation defaults. Plan
rollback with the previous artifact/config and data compatibility beforehand.
