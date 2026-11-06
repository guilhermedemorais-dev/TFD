# CI/CD

Use [CI/CD plan](../templates/ci-cd-plan.md), adapted from the audited MIT source.
Inspect native workflow configuration, triggers, permissions, protected
environments, runners and secrets before changing a pipeline.

Validate YAML and provider-specific configuration; for GitHub Actions use
`actionlint`. Check repository-native build/tests separately. `act` is optional,
not equivalent to hosted runners, and executes workflow code/containers: review
steps and use isolated synthetic inputs with no production credentials. Never
trigger a production workflow merely to validate syntax.

Separate build/package from publication/promotion. Record commit and immutable
artifact digest, approval gate, environment and rollback. Review untrusted PR
execution, permissions, external actions and credentials with security-standard.
Prefer the project's approved pinned dependencies/identity mechanism; do not
silently add services. A green CI check is not proof of production readiness.

On failure preserve job/step/exit evidence, correct the actual cause and rerun
the affected validations. Do not disable tests or bypass protected gates to
obtain green status. Published artifacts and pipeline dispatch require scope.

Tool reference: [actionlint official repository](https://github.com/rhysd/actionlint).
