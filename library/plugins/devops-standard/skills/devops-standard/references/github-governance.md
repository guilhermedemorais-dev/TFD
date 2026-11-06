# GitHub Repository Governance

Read for first-project repository governance or an explicit governance change.
DevOps owns policy and remote configuration; Environment prepares git/gh, the
Harness coordinates gates, Security reviews permissions/secrets/IAM and QA
validates helper behavior. No new skill, installer, OAuth client or receipt.

Contents: operations, authentication, desired state, reconciliation, Projects,
rules/enforcement, CI, readiness, recovery, safe integration and official sources.
Source verification date: 2026-09-24. Recheck version-sensitive API details when
the host/schema or documented capabilities change; live responses prevail.

## Operations and authorization

Use the deterministic [helper](../scripts/github_governance.py), not an ad-hoc
sequence of mutable `gh` commands. The approved
[desired-state template](../templates/github-governance.json) belongs in the
client project's `.github/governance.json`, not automatically in Dev-workflow.
Python 3.11+ stdlib and JSON avoid a second parser/dependency.

```bash
python3 <devops-skill>/scripts/github_governance.py diagnose --workspace /absolute/client-repo --config .github/governance.json
python3 <devops-skill>/scripts/github_governance.py propose --workspace /absolute/client-repo --config .github/governance.json
python3 <devops-skill>/scripts/github_governance.py apply --workspace /absolute/client-repo --config .github/governance.json --proposal /absolute/private/proposal.json --confirm
python3 <devops-skill>/scripts/github_governance.py verify --workspace /absolute/client-repo --config .github/governance.json
```

Replace paths with the resolved installed skill and approved client target.
`diagnose`, `propose` and `verify` read state without writing files/cache, changing
Git, dispatching Actions or mutating REST/GraphQL. A GraphQL query uses POST but
is still read-only. `propose` returns the proposal JSON to stdout; the developer
can save it privately for review. The helper itself does not save it in that mode.

Review local diffs, remote settings/labels/Project/rules actions, limitations and
manual steps. The proposal binds target host/repository/workspace, desired hash
and observed state. `--confirm` represents the user's explicit approval of this
proposal, not permission to approve a plan on their behalf. The helper recomputes
allowed actions and refuses changed targets, tampering, drift or added actions
before mutation; it never executes command strings from proposal input. A changed
proposal requires new confirmation. Do not auto-retry a stale approved proposal.
Previous file lines are omitted from public diffs and bound by `before_sha256`;
inspect the actual local file before approving replacement. Recognizable
credential material blocks with a sanitized error. This is not a guarantee that
arbitrary sensitive data can be recognized, so keep proposals private.

Only `apply` changes approved local/remote resources, followed by fresh readback.
No merge, PR self-approval, deployment, force push or workflow dispatch is part
of bootstrap. New runtime observations are evidence, not fields in desired state.
Local writes are validated on Linux/POSIX. Required descriptor-relative/no-follow
filesystem primitives are checked before any apply mutation when files are in
the proposal. Windows is not homologated; missing primitives fail closed.

When a required manual step was actually observed, supply a separate private
`--evidence /absolute/private/evidence.json` to the operation. Its schema is
`schema_version: 1`, `repository: "owner/name"`, `revision` equal to the observed
default-branch SHA and `observations`, each carrying `capability`
(`project_grouping`, `project_automation` or `rules`), `result: "PASS"`,
`observed_at` date, an inspectable HTTPS `reference` and concrete `action`.
Record facts only after observation; do not prefill PASS from the example.
The proposal binds this evidence too. A matching SHA does not mean remote
configuration never drifted: recheck the actual setting when it changed or the
evidence is stale, and distinguish manual observation from API verification.
Evidence must be dated within the last seven days, not in the future. It cannot
override a board grouping that the API observes as incorrect. Project automation
requires a completed manual observation, not an exception entry.

## Authentication and permissions

Detect git/gh first. GH_MISSING/GH_BROKEN routes selective preparation to
Environment after authorization; do not embed another installer. Check the
selected host and active account using captured `gh auth status`, then `gh api
user` for actual identity. Do not echo auth output or raw errors. JSON auth-status
exit zero alone does not prove authentication, as the official CLI documents.

If unauthenticated return AUTH_REQUIRED plus USER_ACTION_REQUIRED:

1. Developer runs `gh auth login --hostname github.com` for the intended host,
   follows the browser flow and returns to the agent. Never ask for a token.
2. Revalidate identity and permissions, then resume diagnose, not all onboarding.

For stored OAuth credentials needing Projects scope, guide the developer to
`gh auth refresh --hostname github.com -s project` only when mutations require it.
GraphQL read-only Projects queries can use `read:project`; confirm actual
authorization, organization SSO/policies and the credential type. Do not request
`read:org` or broader scopes blindly; scope changes cannot grant missing resource
membership/admin rights, and environment-provided/App tokens have different
permission management. Never run auth token/show-token, copy hosts.yml, request
PATs in chat, persist auth state or include raw CLI output in receipts. GitHub CLI
may fall back to local plaintext storage if its credential store fails; that is
the developer's host security decision, not permission to copy credentials.

Report AUTHENTICATED, REPOSITORY_ACCESS, REPOSITORY_ADMIN, ORGANIZATION_ACCESS and
PROJECT_ACCESS separately. Private repo support requires real access. A clone
or push does not prove admin; inspect repository permissions for settings and
Project edit capabilities separately. Org access may be N/A for a user-owned
target, not silently passed. Unknown capability remains NOT_VALIDATED. A generic
403/404 may mean permissions, private-resource masking or policy, not a plan limit.

## Desired state and preservation

The template is a versioned policy, not a runtime snapshot. It describes the
repository identity/default branch/merge policy/configurable agent prefix,
Project title/statuses/view, labels, human gates, automation limits and selected
local/CI/rules requirements. Reject unknown or unsafe settings. No tokens, IDs,
login state, machine-specific executable paths or arbitrary commands belong here.

Exact top-level fields are `schema_version`, `repository`, `project`, `labels`,
`human_gates`, `automation`, `local`, `ci`, `rules` and `exceptions`; see the
template for field types/defaults. Repository identity lives in config, not a
second CLI target flag. Disabling Project/CI requires a reason. An exception is
an explicitly approved `{capability, reason}` fallback decision, never a manual
completion certificate. Never add an exception just to get a green readiness.
Only a `rules` limitation explicitly classified `UNSUPPORTED_BY_PLAN` can yield
READY_WITH_LIMITATIONS, and only with both the approved exception reason and
valid completed `rules` evidence. Unknown state and missing permission still block.

Use `NOOP | CREATE | UPDATE | BLOCKED` against freshly observed resources:

- Preserve correct files and all unrelated resources. Existing differing files
  need an explicit reviewed diff; symlinks/traversal outside the workspace block.
- Prepare applicable CODEOWNERS, Issue forms, PR template, quality workflow,
  CONTRIBUTING and docs/specs/tasks/execution structure only for the approved
  stack. CODEOWNERS syntax/presence does not establish reviewer enforcement.
- Preserve labels, reusing unique normalized equivalents and adding only missing
  names. Cosmetic matching must not merge semantically distinct resources; an
  ambiguous match blocks instead of guessing or deleting.
- Propose squash-only and delete-branch settings as baseline, not a silent
  override of the client's approved merge policy. Never execute a merge.
- Retrieve all relevant pages before deciding absence. Failed/incomplete reads
  are not empty collections, and permission failure is not a create instruction.

## Projects, views and built-in workflows

Find the Project by owner and title, reuse a unique match and create only when
absence is established. Discover node ID, number, URL, fields/options, linked
repositories and views. Preserve existing options and their IDs on field update;
add missing statuses rather than rebuilding the field or clearing item values.
Use current `ProjectV2SingleSelectFieldOptionInput.id` support to preserve identity;
older hosts without equivalent safe support require manual action, not data loss.

The local baseline has eight states:

| Event, after evidence and the applicable human gate | Status |
| --- | --- |
| Issue created | Backlog |
| Spec/SDD begins | Discovery / SDD |
| Scope approved | Ready for Dev |
| Execution actually begins | In Progress |
| Implementation complete; technical validation begins | Validation |
| PR created | In Review |
| CI and all required technical sectors approved | Awaiting Final Approval |
| Human merge observed | Done |

`blocked` remains a label; unrecoverable failure preserves the current status.
Local completion/commit is not Done. Stop automatic rework after the configured
limit, default three cycles, with diagnosis; do not repeat permission failures.

Current Projects GraphQL supports `createProjectV2View` and
`updateProjectV2View` for name/layout (board is `BOARD_LAYOUT`) and selected
configuration. Discover view IDs and verify after an approved change.
`ProjectV2ViewConfigurationInput` currently exposes `visibleFieldIds`, not a
grouping mutation. Read `groupByFields` to check Status grouping; if incorrect,
MANUAL_ACTION_REQUIRED: open Kanban view, select board layout, set column grouping
to Status and save the view. Do not invent a `groupBy` mutation parameter.

Auto-add baseline is this repository, filter `is:issue is:open`, initial Backlog.
Current documented built-in Auto-add limits per Project: Free 1; Pro 5; Team 5;
Enterprise Cloud/Server 20. Validate the current owner/plan and existing count,
not a global rule that Free lacks all automation. Auto-add does not backfill
existing matching items just because the workflow was enabled.

The public schema reviewed exposes workflow name/enabled/identity but not the
full Auto-add target/filter/initial-status configuration, and no create/update
workflow mutation was found. Do not infer correct behavior from a workflow name.
MANUAL_ACTION_REQUIRED: Project menu → Workflows → Auto-add → Edit, choose the
target repository/filter and enable; configure item-added status Backlog using
the appropriate built-in workflow and verify with a synthetic item. Record
target, action, time and inspectable evidence. Such a manual test creates an item
and therefore requires separate scoped approval; it is not `verify` read-only.

Review default workflows: GitHub enables closed→Done and merged→Done on new
Projects. Disable or adjust closed→Done when closure without human merge would
violate this baseline. Never silently delete workflows. An approved Actions/API
alternative is possible as a separate reviewed configuration, with minimal
permissions and secure credentials, but is not an automatically installed fallback.
Manual completion evidence and acceptance of a limitation are distinct; neither
may masquerade as the other or silently bypass required Project validation.

## Rules, plans and enforcement

Resolve owner type, visibility, available plan metadata and endpoint capability
separately. Official repository branch/tag rulesets are available on public Free
repositories; private repositories require an eligible Pro/Team/Enterprise plan.
Organization-level policies and push rules have different availability. Do not
infer all capabilities from the word Free or from another owner's plan.

Classify SUPPORTED, UNSUPPORTED_BY_PLAN, NOT_AUTHORIZED, NOT_CONFIGURED and
NOT_VALIDATED separately. Unknown plan plus ambiguous API denial is not proven
UNSUPPORTED_BY_PLAN. Propose explicit PR+CI+human-merge fallback only when enough
for the project's risk and approved; show loss of server enforcement clearly.

Only approved branch rules are eligible: PR requirement, force-push/deletion
prevention, actual observed checks, up-to-date policy and feasible reviewer count.
Solo projects must not require an impossible independent reviewer. Read inherited
rules too; do not overwrite parent policy or duplicate an equivalent ruleset.
`enforcement: active` is distinct from `evaluate`/disabled. Read active branch
rules, conditions, effective target and bypass actors; a ruleset object merely
existing is insufficient. Verify required checks refer to actual emitted job/check
names, not guessed test/lint/security names. Ruleset evaluation mode is not
enforcement and its plan availability is separate.

Report CODEOWNERS_FILE_PRESENT separately from CODEOWNERS_ENFORCEMENT_ACTIVE.
Protected-branch/ruleset requirements, matching ownership and applicable branch
must be verified before the latter claim. Even configured active rules do not
prove every actor is blocked: disclose bypass paths and lack of destructive
enforcement testing. Never test protection by force-pushing the protected branch.

## CI and readiness

Inspect project-native scripts/config/lockfiles without executing them during
diagnose/propose. Use Node/Next locked install and existing lint/typecheck/test/
build scripts; PHP/Laravel Composer lock/native checks; Python project lock/native
tools; Go dependency verification/test/build and configured lint. Unknown stacks,
missing locks or ambiguous commands need a reviewed choice, not a universal CI.
Reuse existing workflows. Generated YAML is not a run; preserve least privilege,
untrusted-PR boundaries, pinned approved actions and no deployment side effects.
The helper preserves and hashes existing `.yml` and `.yaml` workflows. Generated
Node CI requires a numeric `.nvmrc`/`.node-version` plus npm lock; PHP requires
the observed exact Composer platform PHP version; Go uses `go.mod`; Python uses
the supported uv lock/pytest path. Action revisions are fixed full SHAs, not a
claim to use the latest upstream release. `local.generate: false` does not waive
required existing governance files.
Security owns scanner interpretation. CI green != SECURITY PASS or production.

`verify` rereads local and remote state and reports drift and evidence. READY
requires environment/auth/access, required local files, remote settings/labels,
Project or explicit N/A, CI evidence or justified N/A, human gates and actual
verification. READY_WITH_LIMITATIONS requires a specifically approved, adequate
fallback plus observed remaining requirements, not an unknown mandatory check.
AUTH_REQUIRED/BLOCKED/NOT_VALIDATED remain actionable readiness results, not new
Harness lifecycle states. A pending manual step cannot count as observed PASS.
READY also requires local Git HEAD to equal the observed remote default-branch
SHA, a clean worktree and governed/stack bytes matching tracked Git blobs. Ignored
local files do not bypass this check. A locally implemented but unpublished
change remains BLOCKED; publication requires separate human authorization.

Reuse `EXECUTION_RECEIPT` with repository/revision, operation, gh version,
credential-free identity, capabilities, proposal/confirmation reference,
mutations actually completed, dynamic nonsecret IDs, verification, limitations
and final readiness. PROJECT READY != PRODUCTION AUTHORIZED. Keep report/proposal
private when repository metadata is sensitive; never commit runtime credentials.

## Failure and recovery

Classify GH_MISSING, AUTH_REQUIRED, INSUFFICIENT_PERMISSION, PLAN_LIMITATION,
API_UNAVAILABLE, GRAPHQL_UNSUPPORTED, REMOTE_CONFLICT, LOCAL_CONFLICT and
VALIDATION_FAILED with a safe next action. No raw stderr/traceback/response dump.
If apply partially fails, preserve the completed-operation evidence and stop;
refresh diagnosis/proposal before resuming. No automatic resource deletion or
destructive rollback. Record rollback limits and obtain fresh approval for any
reversal; distributed local/remote writes are not an atomic transaction.

## Safe manual integration test, not executed by the standard suite

Use an explicitly authorized disposable private repository/owner, not the
Engineering Harness source or production. Record initial revision, visibility,
permissions and observed capabilities without credentials. Review target and
local files before running diagnose → propose → human review → confirmed apply
→ verify. Complete required manual Project steps with separate evidence, and
publish/run a safe CI only under separate authorization when needed.

Then propose again against fresh state: expect NO CHANGE REQUIRED; applying the
new reviewed no-op proposal must create nothing. This second real run establishes
operational idempotency; fake-gh tests alone do not. Record before/after IDs,
checks, command exits and readiness/limitations. Do not delete the test repository
as implicit cleanup. Until this rehearsal occurs, remote integration is
NOT VALIDATED, regardless of unit-test results.

## Provenance and primary references

- [OFFICIAL PRACTICE]: GitHub-documented APIs, CLI and current capabilities below.
- [ECOSYSTEM CONVENTION]: idempotent reconciliation, diff review and readback.
- [PROJECT CHOICE]: eight Kanban stages, human merge/deploy gates and JSON stdlib.
- [LOCAL EXTENSION]: desired/proposal schema, fingerprints and readiness report.

Official sources, verified 2026-09-24; consult only the relevant area:

- CLI: [login](https://cli.github.com/manual/gh_auth_login),
  [status](https://cli.github.com/manual/gh_auth_status),
  [refresh](https://cli.github.com/manual/gh_auth_refresh),
  [api](https://cli.github.com/manual/gh_api),
  [project commands](https://cli.github.com/manual/gh_project).
- REST: [repository settings](https://docs.github.com/en/rest/repos/repos#update-a-repository),
  [labels](https://docs.github.com/en/rest/issues/labels),
  [rulesets/effective branch rules](https://docs.github.com/en/rest/repos/rules),
  [branch protection](https://docs.github.com/en/rest/branches/branch-protection).
- Projects: [API usage/auth](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects),
  [GraphQL fields/items/views/workflows](https://docs.github.com/en/graphql/reference/projects),
  [board customization](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-board-layout),
  [Auto-add/plan limits](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically),
  [built-in defaults](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations).
- Enforcement/plans: [ruleset availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets),
  [organization rulesets](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization),
  [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
