# Infrastructure as code

Use the project's Terraform or OpenTofu choice, not both by default. Inspect
root module, locked providers/modules, backend, workspace/state, account/region
and credential scope. IaC state and plan artifacts can contain secrets; keep
them private and out of Git, Issue comments and external tools.

Validation sequence: `terraform fmt -check -recursive` (or project OpenTofu
equivalent), initialization only after safety review, `terraform validate`,
then an authorized `terraform plan -detailed-exitcode`. `tflint` complements,
not replaces native validation. With detailed exit codes: 0 means no changes,
1 means error, 2 means changes proposed, not a failed command to conceal.
Review replacements, deletions, permissions, cost and unexpected drift.

`terraform init -backend=false` avoids backend initialization but is not a
sandbox or unconditional safe command. Initialization downloads modules/plugins;
provider execution and data sources can access APIs or run code. Review sources,
lockfiles, network scope and credentials first. Plan normally refreshes remote
state; only run against approved targets. Disabling refresh may hide drift.

Apply and destroy are NEVER default validation steps. Both require explicit
human approval of exact target and reviewed plan plus rollback_strategy.
Never add auto-approve as a workaround. State migration/import/recovery and
unlock operations also require bounded authorization; do not force-unlock an
unidentified active operation. Native fmt/validate success does not validate
production permissions, capacity, drift or a deployment.

Source: [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan).
