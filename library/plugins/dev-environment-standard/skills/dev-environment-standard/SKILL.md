---
name: dev-environment-standard
description: "Diagnose Engineering Harness plugin health and prepare or repair the development capabilities a task needs. Discover runtimes, specialist tool registries and MCPs, preserve local preferences, and reuse verified environment state. Does not implement product features or provision infrastructure."
---

# Dev Environment Standard

Own Environment Bootstrap / Plugin Health. The Engineering Harness supplies the
required capabilities; specialist skills retain ownership of their tools and
interpretation. Preparation does not replace implementation, SDD, security or
UI/UX, and an installation is not evidence that the specialist ran.

Read [operations.md](references/operations.md) before running the CLI and
[state-and-consent.md](references/state-and-consent.md) when preparing, repairing,
or accepting host evidence/custom MCPs. Consult [mcp-library.json](references/mcp-library.json)
for public MCP knowledge. LLM provider/model knowledge is owned by the Harness
provider registry when that plugin is available; Environment detects credentials,
runtime tools and host compatibility but does not duplicate the provider catalog.
Do not load every specialist's methodology merely to discover its registry.

## Choose the operation

- **doctor**: read-only discovery and health report. No installation, cache
  writes, persistent invalidation or automatic test runs with side effects.
- **prepare**: diagnose, plan CORE/required/selected capabilities, obtain missing
  choices and explicit approval, apply supported actions, verify and persist.
  Dry-run is read-only. CORE is a priority, not permission to install blindly.
- **repair**: identify a real failed component, invalidate only its stale
  observation, then prepare/verify that component under the same consent rules.
- **status**: compatible cached report plus cheap checks. Reuse it before tasks;
  run doctor only after incompatible state, missing evidence or a real failure.

The executable is [scripts/environment.py](scripts/environment.py). Use Python
3.11+ and explicit repository/workspace paths; discover these paths from the
current installation, never assume a particular developer's home directory.
The repository root identifies plugin knowledge; workspace identifies the
project being prepared. They can be different.

## Bootstrap loop

1. Inspect source of truth, current task requirements and actual host tools.
2. Run doctor. Separate plugin structure, available tools, connection and auth.
3. Discover all canonical skills. For each existing `references/tool-registry.json`,
   validate owner and entries, then use the shared `tool-state.py` helper.
   Skills without a registry still undergo structural health checks.
4. Plan only CORE, task requirements, selected components and their necessary
   bootstrap-safe prerequisites. Prefer what already exists and the project's
   lockfile/package manager. Never install all tools, browsers or managers.
5. On first prepare, show RECOMMENDED and OPTIONAL choices with capabilities.
   Offer PROJECT_SPECIFIC entries only when the project warrants them. Ask:
   **“Você utiliza algum MCP específico que não está nesta biblioteca?”**
6. Persist explicit choices and not_requested outcomes without treating silence
   as installation approval. A declined/ignored optional is not an every-session
   prompt. Revisit only when requested, reset, newly required, broken, changed
   materially, project-specific, or incompatible.
7. Present concrete actions, provider, version, scope and permissions. Apply
   only approved actions supported by the host. Preserve existing definitions;
   a conflict requires review, never an overwrite.
8. Verify tool presence/execution and MCP availability/connection/auth separately.
   Use host tools for connection and authentication; a config entry is insufficient.
   When the Harness requests multi-provider execution, run its provider status/
   probe flow without printing secrets. A provider config or environment-variable
   name is not proof of an executable model.
9. When `reverse-engineering-standard` is selected, detect Node.js 22.19+ and
   the plugin-local reverse context runtime. If runtime dependencies are absent,
   propose the scoped install inside
   `plugins/reverse-engineering-standard/runtime/`; after approval run
   `npm run bootstrap` there, which verifies and installs the vendored REA
   tarball, and then run `node reverse-context-gateway.mjs probe`. Do not globally install REA or
   optional engines by default. Install/prepare Ghidra, Hopper, IDA, JADX,
   Binwalk, Unblob or Wakaru only when the selected target actually requires
   that provider and the user approves the preparation.
10. When `seo-standard` is selected, detect Python 3.10+ and the plugin-local
    SEO runtime. If it is absent, propose the scoped bootstrap under
    `plugins/seo-standard/runtime/`; after approval run `python bootstrap.py`
    and then `python seo-gateway.py probe`. Prefer the vendored BeyondSEO
    release. Do not install browser support or crawl arbitrary sites unless the
    selected Task requires it and scope is authorized.
11. Persist sanitized local observations and return HEALTH_REPORT plus human
   summary, installations actually performed, blockers and next action.

## Platform routing

During assisted installation invoke `prepare` once with the actual execution
runtime and writable local state. `platform_tools` selects the packaged
`Tools (Linux)`, `Tools (Windows)` or `Tools (macOS)` catalog and persists the
binding in the existing environment state. This is not an automatic host hook
and never rewrites manifests. Before later tasks reuse `status`; do not ask
which OS to use on every request. WSL selects Linux, not native Windows.
Runtime, catalog or source drift requires preparation again. Interpreter file
checks are cheap cache invalidation, not certification of runtime support.

Catalogs reference canonical owner scripts without duplicates. Route only
`eligible: true` entries, subject to owner gates and prerequisites.
`NOT VALIDATED` needs verification or an approved adapter; `UNSUPPORTED` has
no approved platform route. This does not block unrelated external tools with
their own compatible registry/runtime evidence. Context retrieval via Potpie
or lexical fallback supplements Task sources; environment state owns OS selection.

## Library, ownership and local state

| Artifact | Responsibility |
| --- | --- |
| MCP Library | Public, versioned provider/capability/policy knowledge |
| Custom MCP | Developer-local, audited extension; never automatically published |
| Tool Registry | Specialist-owned tool definitions, not copied into this plugin |
| Environment State | Ignored local observations, preferences and compatible health snapshot |

MCP tiers: `CORE`, `RECOMMENDED`, `OPTIONAL`, `PROJECT_SPECIFIC`, `COMMUNITY`,
`RUNTIME_PROVIDED`. Provenance is a separate field: `OFFICIAL`,
`VERIFIED_THIRD_PARTY`, `COMMUNITY`, `UNKNOWN`. Runtime states are `AVAILABLE`,
`INSTALLED`, `CONNECTED`, `AUTH_REQUIRED`, `MISSING`, `BROKEN`, `UNSUPPORTED`.

Preserve all four distinctions:

```text
installed != connected
connected != authenticated
registered != available
planned tool != executed tool
```

UNKNOWN never installs automatically. COMMUNITY requires specific consent after
source/permission review. `node_repl` is detect-only when supplied by the host.
Docker MCP Registry is a catalog, not a connectable server. Docker MCP Gateway
is an optional lifecycle/isolation route when compatible Docker tooling already
exists; Docker is not a mandatory bootstrap dependency.

## Preparation authority

`AUTO_SAFE`, `PROJECT_SCOPED` and `USER_SCOPED` actions may execute only after
approval for the concrete action and scope. `AUTH_REQUIRED` prepares only as far
as the host safely supports, then hands authentication to the user.
`PRIVILEGED` returns `USER_ACTION_REQUIRED`; `MANUAL_ONLY` gives instructions;
`RUNTIME_PROVIDED` only detects. Missing runtimes never trigger silent admin/root
installation. Browser preparation selects only the required engine.

Keep lockfiles intact. Prefer npm ci, frozen pnpm, version-appropriate locked
yarn, and uv sync --locked. Python uses the existing isolated/project-approved
environment. Dependency lifecycle hooks execute project code and belong in the
action's approval scope. Do not use arbitrary shell strings from runtime state.

## Health and handoff

`HEALTHY` requires evidence for structure, references, registry validity, state
safety, scripts and relevant validators/tests. Unknown checks are NOT VALIDATED.
`DEGRADED` means usable portions exist but evidence/capabilities are incomplete.
`BLOCKED` means a required prerequisite or invariant fails. Task readiness is
separate from whether every optional catalog entry happens to be installed.

Return to the Harness with the required capability status and evidence, then
let its router invoke the owner skill. A healthcheck does not produce a
specialist execution receipt on that specialist's behalf.

## Scope and security

Do not persist or print passwords, tokens, API keys, OAuth tokens, cookies,
headers or raw host configuration. Provider setup may show the required
environment-variable name and official setup/documentation URL, but never the
secret value. Use host credential storage and scoped
permissions; report USER_ACTION_REQUIRED for a real manual auth requirement.
Do not acquire credentials as part of discovery. Custom provider claims require
review and stay local even after approval.

Advanced Git workflows, protections, CI/CD, Actions/GitLab/Jenkins, deploy,
SSH/VPS/cloud, Kubernetes/Terraform/Ansible, reverse proxies/Nginx, production
Docker and infrastructure observability belong to `devops-standard`.
Git detection and GitHub collaboration remain in scope. Application debugging
with Sentry is distinct from provisioning infrastructure.
