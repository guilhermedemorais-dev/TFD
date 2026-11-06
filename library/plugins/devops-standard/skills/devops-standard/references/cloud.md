# Cloud operations

No provider is mandatory. Detect the existing account/project, region, resource
IDs, tenancy, identity and cost boundaries before selecting native tooling.
Confirm official version-sensitive documentation, pricing/limits and supported
operations when needed; never infer authority from credentials being present.

Prefer bounded read-only inventory and plans. Mutations require task scope,
resource-specific impact and recovery plan; production and destructive gates
still apply. Route IAM, keys/secrets, public exposure, TLS, firewall and sensitive
storage to security-standard. Do not print credential values or upload customer
data to an API/MCP for testing. Use synthetic fixtures and approved sandboxes.

Record ownership, budget/quotas, backups, egress exposure, lifecycle and cost
impact. Do not buy capacity, migrate providers or delete resources merely to
optimize an estimate. Cloud/MCP availability must be verified in the actual
runtime. Environment Bootstrap owns the Hostinger/AWS/WordPress catalog;
resolve that skill when available, without recreating its catalog here.
Repository integration is not evidence of a connected/authenticated provider.
