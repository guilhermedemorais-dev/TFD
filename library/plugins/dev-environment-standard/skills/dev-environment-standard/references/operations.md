# Environment CLI operations

Run Python 3.11+ with the canonical checkout (or equivalent plugin distribution)
as `--repo-root`. The `--workspace` project may be separate. This CLI uses only
stdlib and the existing Harness tool-state helper. It does not depend on the
developer's installed global plugins matching this checkout.

## Diagnose and plan

From the repository root:

```bash
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py doctor --repo-root . --workspace . --json
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py prepare --repo-root . --workspace . --dry-run --json
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py status --repo-root . --workspace . --json
```

Omit `--json` for the human summary. Doctor/status never create state. A missing
snapshot returns `refresh_required`, not READY. A report can be DEGRADED because
tests or runtime evidence were not provided, even when its structure is valid.
Snapshots and validator evidence expire after 24 hours; MCP observations expire
after 300 seconds. Status preserves the original observation time and reports
its own check time separately. Source/test/configuration changes invalidate cache.
The exit code is nonzero for a blocked operation or failed applied action;
always inspect `plugin_health`, `ready` and `refresh_required`, not exit code alone.

Use `--state-dir` for an ignored, writable local directory when the installed
bundle is read-only. Default is this skill's `runtime-state/`. Config/evidence/
preferences/approval inputs must stay local; the filenames below are examples
inside ignored repository `runtime-state/`, never files to commit.

## Select only required capabilities

`--require CAPABILITY` resolves matching MCPs and specialist tools. `--select ID`
selects one MCP/library entry, `tool:OWNER:ID`, `project:dependencies`, or one
browser such as `browser:chromium`. These flags repeat. Selection determines the
plan but does not authorize installation. Tools retain their registry policy.

Example plan for project Python testing:

```bash
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py prepare --repo-root . --workspace . --require python-unit-testing --select tool:dev-implementation-standard:pytest --dry-run --json
```

Only project-approved locked dependencies can be prepared by the generic
dependency adapter. An official scanner with a platform-specific installer is
handed back to its owner for supported instructions; no guessed package names
or automatic system runtime installation. Conflicting lockfiles are explicit.

## Preferences and custom MCPs

An optional preference input is:

```json
{"mcp_preferences":{"figma":"enabled","firecrawl":"disabled","sentry":"not_requested"}}
```

Supply it with `--preferences runtime-state/preferences.json`. Choices persist
on prepare; a declined/unrequested choice is not a new prompt each session.
`auth_required` and `connected` are persisted runtime observations, distinct from
the preference to enable a provider. PROJECT_SPECIFIC is offered only when the
capability is required by the project. Custom intake uses `--custom-mcps` and an
object `{"custom_mcps":[]}` to record an explicit no-custom response.

A custom entry contains exactly: `id`, `name`, `provider`, `repository`,
`documentation`, `capabilities`, `maintainer`, `installation`, `transport`,
`permissions`, `authentication`, `risks`, `origin`. Supply reviewed nonsecret
metadata, never auth values or executable commands containing credentials.
HTTPS provenance is required. The custom adapter stores metadata privately and
hands setup to the host; it does not execute arbitrary custom installation text.
No custom entry is promoted into `mcp-library.json` automatically.
Persisted custom entries join the effective local catalog for doctor/status and
`--require` resolution. Fresh host evidence uses their private IDs. Custom setup
remains MANUAL_ONLY, regardless of claimed origin. `authentication` accepts
`none`, `host-managed`, `oauth` or `api-key`, never a credential value.

## Approve concrete actions

First request a dry-run with the intended `--host codex|claude` and explicit
`--host-config PATH`. Codex TOML and Claude JSON are supported for adding an
absent public MCP definition. An existing differing definition is never replaced.
An unsupported host receives USER_ACTION_REQUIRED.

Copy only reviewed plan actions into a local approval file:

```json
{"approvals":[{"component":"project:dependencies","command":["npm","ci"],"scope":"/absolute/path/to/project"}]}
```

The scope must exactly match the plan. This is a schema example, not preapproval
for the current project. MCP config actions use a `host-config:add` marker plus
host, provider ID and serialized public configuration; it is not a shell command.
This binds approval to the exact provider endpoint/package and target file.
Community actions additionally require `community_confirmed: true`, after audit.
UNKNOWN, privileged and runtime-only entries cannot be enabled by an approval
that contradicts policy.

Rerun prepare with `--approvals runtime-state/approvals.json` and without
`--dry-run`. Tools use the existing owner helper; subprocesses use argument arrays
and the requested workspace, never shell interpolation. Install/config receipts
distinguish executed/verified/registered/failure. Registration does not claim a
server started, connected or authenticated. Auth credentials remain in the host.

To recover a component previously available and now failing:

```bash
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py repair --repo-root . --workspace . --component tool:dev-implementation-standard:pytest --dry-run --json
```

Review/approve the targeted plan before applying. Repair does not reinstall
healthy components or erase other preferences.

## Host runtime evidence

The host executor must perform safe capability/connection/auth checks, then write
only normalized facts to a local file supplied via `--runtime-evidence`:

```json
{
  "schema_version": 1,
  "host": "codex",
  "workspace": "/absolute/path/to/project",
  "config_digest": "sha256-of-current-host-config",
  "observed_at": "actual-observation-time-in-UTC",
  "mcps": {
    "github": {"available": true, "connected": true, "authenticated": true}
  }
}
```

These are schema placeholders, not real evidence. Compute the digest from the
current config; use `none` when no config exists for this host, `missing` for a
configured path that is absent. Observations are valid for 300 seconds and the
matching host/workspace/config. Accepted fact fields are booleans: `installed`,
`connected`, `authenticated`, `auth_required`, `broken`, `available`. Report auth
required only after an actual auth challenge/check; catalog auth requirements do
not prove this developer has an expired login.

A credential-free config inspection records only registered names/enabled flags.
It does not contact or start servers, read tokens for diagnostics, or mark them
CONNECTED. A host inventory can establish AVAILABLE while a successful harmless
call establishes CONNECTED; auth is another observation. Do not infer that `gh`
CLI login proves the GitHub MCP's authentication.

## Validation evidence and health

Run the repository's tests and validators explicitly, record their real results,
and pass `--validation-evidence FILE`. Evidence shape is `schema_version: 1`,
the current doctor `fingerprint`, actual UTC `observed_at`, and `checks` with
command, exit_code and result. The source/config fingerprint and bounded age
prevent reusing validation after edits or across environments. Never synthesize
successful evidence just to make health green.

Generic dependency/browser actions report EXECUTED, not VERIFIED, when the
installer exits successfully. Pending and failed receipts survive later prepare
runs; the same action is not silently repeated. After the authorized executor
has actually checked the project or launched the selected browser, add that
check's `component` (for example `project:dependencies` or `browser:chromium`) to
its validation-evidence check. The evidence must match the current fingerprint
and be observed after the receipt's `executed_at`. Run prepare with that evidence
and no new selection to record VERIFIED_EXTERNALLY without reinstalling.

For a failed generic initial install, repair the specific cause manually within
the approved scope and perform that same real component check. Do not erase the
whole state or fabricate a successful check. Automatic `repair --component` is
limited to an MCP/tool previously observed available and now failing.

`capabilities_ready` covers the requested capabilities. Full `ready` additionally
requires CORE/auth, valid test evidence and no unverified preparation receipts.
Optional tools absent from the current task do not prevent full readiness.

Doctor checks manifests/marketplaces, canonical skills and agent metadata,
registries, internal links, script syntax, ignored/writable state and README.
Behavioral tests are reported separately and are NOT VALIDATED without matching
evidence. A tool's version command proves detection, not that every command or
browser interaction works. Browser binaries discovered in cache require separate
execution evidence. The report preserves these limits.

## Current adapter boundaries

Hostinger (`hostinger`), AWS API MCP (`aws`) and WordPress MCP Adapter (`wordpress`)
are PROJECT_SPECIFIC and use host handoff, not automatic setup. Inspect their
plans without changing account/site configuration:

```bash
python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py prepare --repo-root . --workspace . --select hostinger --select aws --select wordpress --dry-run --json
```

These selections return USER_ACTION_REQUIRED. Approvals cannot turn this handoff
into a supported installer. Identify the exact account/site and minimum permissions
first; credentials remain in the host. Hostinger can expose hosting/DNS/billing
mutations. AWS API needs a deliberately scoped IAM profile; read-only mode is an
additional safeguard, not a replacement for IAM or protection from sensitive
outputs/local file access. WordPress requires the site's compatible official
adapter and reviewed exposed abilities; do not substitute WordPress.com or invent
a universal site URL. Do not install the adapter on a live site during bootstrap.
No provider action, cloud provisioning or content mutation is authorized by a
catalog entry. Verify connection/auth separately only after approved setup.
The AWS API MCP documentation marks that server superseded by the official AWS
MCP server. Review the linked successor/migration documentation before new setup;
the legacy entry is explicit knowledge, not a recommendation to install it.

- Safe additions to explicit Codex TOML/Claude JSON config files are implemented.
- Actual MCP connection/auth verification is performed by host capabilities and
  imported as fresh observations, not simulated by network reachability.
- Firecrawl, Supabase, Docker setup and custom providers use manual/host handoff
  where API keys, project scoping or host-specific prerequisites are involved.
- Browser and project dependency preparation is capability-driven and approved;
  missing system libraries/runtimes return a manual action instead of sudo.
- No CI/CD, deployments or infrastructure services are created.
