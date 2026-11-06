# Discover and prepare stack CLIs

Owner-approved local integration policy, 2026-10-21. This extends the existing
Environment/tool-state workflow; it does not create a second installation engine.

## Responsibility and order

1. The requesting sector (Frontend, Backend or other owner) identifies the approved
   stack, actual runtime/framework versions, project scripts, lockfile and exact
   operation. Consult its selected Task resources and central metadata first:
   `library/tools/stack-clis.json`. Do not read every tool's documentation/body.
2. Check compatible project-local tools and cached state. Reuse them. A CLI may be
   a runtime, package manager, generator or framework command; absence of a CLI is
   a valid answer. React tooling is not automatically React-owned tooling.
3. For a catalog gap, new framework version, stale documentation or unknown flag,
   research the official project documentation/repository. Distinguish official
   tools from documented ecosystem/community alternatives and deprecated tools.
   Prefer an existing mature tool; do not introduce a framework to obtain a CLI.
4. The sector selects and validates suitability for the approved operation. Record
   the docs/version and required installation. Environment detects the real OS,
   runtime and manager and performs necessary preparation. Catalog maintains the
   shared record; sectors consume indexes, not duplicated tool lists.

## Authorized automatic preparation

The owner has authorized installation of necessary selected CLI tools for the
approved project work. Reuse this authorization for routine project-local setup;
do not ask the owner again for technical choices already covered by the Task.
Record the concrete package/version, command, scope and authorization in the
existing installation receipt or exact-command approvals when the canonical
Environment helper requires that representation. Never bypass a host approval.

Prefer existing package.json scripts, installed local binaries and the project
manager/lockfile. For Python use its chosen manager or an isolated project venv;
resolve the venv interpreter directly on Linux/Windows/macOS instead of depending
on shell activation. Install only missing compatible selected tools. Pin resolved
versions and retain lockfiles; docs' @latest examples are discovery examples, not
permission to upgrade all projects. npx/npm exec may download and execute code,
including with --help; they are not read-only availability probes.

Catalog argv templates are documentation, never executable commands to copy
blindly. Resolve placeholders from inspected project state, adapt to its existing
package manager and explicit target path, verify current flags and dependencies,
and use the existing Environment/skill-owned-tools protocol. Do not add a generic
shell runner that trusts catalog strings. Do not install all entries together.

System-wide runtime installation, privileged/global changes, production operations,
paid/account-linked services and unrelated tools require their applicable scope
and host authorization. Missing network or required approval is BLOCKED for that
operation; continue independent work without removing the capability.

## Generation, execution and verification

A scaffolder is for an approved new empty directory, never a replacement for an
existing repository. Inspect generated files and dependencies in the diff. Retain
PRD decisions on architecture, paths, package manager, styles and module system;
check generated agent instructions for conflicts. Use documented dry-run/diff
options where supported, not invented universal flags. Do not use overwrite/all,
create containers, register cloud services or deploy as a default generator step.

Record support documentation separately from INSTALLED, CONFIGURED, AUTHENTICATED,
AVAILABLE and VERIFIED observations. Documentation review is NOT_VALIDATED runtime.
Verify the exact selected binary/version and bounded operation with appropriate
project checks. Failure must not trigger unbounded reinstall/retry loops. No token
saving or native-platform homologation claim without measurements/executed tests.
