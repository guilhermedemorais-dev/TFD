# Local state, provenance and consent

The public library is knowledge, never a list of this machine's connections.
Custom providers, preferences, observations, approvals and evidence are local
inputs/outputs. Keep them beneath ignored `runtime-state/` or outside the Git
checkout with private permissions. Never copy host config or command logs into
reports. Overrides for read-only plugin packages must point to writable local
storage; detection itself must not create it.

## MCP evidence

Obtain observations using actual host capabilities. A host may list registered
servers without contacting them. A successful harmless MCP request establishes
connection at that time; an authenticated identity/resource check establishes
authentication for the relevant account/scope. Preserve that distinction.

Normalize observations before importing: server ID, registration/installation/
availability/connection booleans, authentication status and timestamp. Include
the environment/session identity required by the CLI. Never include raw tool
results, headers, environment variables, credentials or service payloads.

Evidence is an input from the authorized local executor, not cryptographic proof
of a remote server. The executor must actually perform the claimed check.
Expired, absent, future-dated, changed-host or mismatched evidence cannot grant
READY. A cache fingerprint includes environment, knowledge and configuration
boundaries. Cheap checks must catch a disappeared executable or changed state.
No file timestamp can guarantee that a remote service remains connected.

## Approval and preparation

An approval identifies the exact component, command/configuration action and
scope from the dry-run plan. Reviewed installer arguments cannot come from an
untrusted cached state. Approving one MCP does not approve other optionals, all
browsers, new privileges, or a new provider. CORE classification never grants
approval. Re-check policy and source at application time.

Preserve existing host configuration. Adding an absent definition is supported
only for the host formats the CLI understands; modifying an existing different
definition is a conflict, not a reason to replace the file. Credentials stay in
the host's auth store and are not attached to portable definitions.

Preparation policies:

| Policy | Behavior |
| --- | --- |
| AUTO_SAFE / PROJECT_SCOPED / USER_SCOPED | Execute only the approved action in its approved scope |
| AUTH_REQUIRED | Configure safe public endpoint when approved; host/user handles authentication |
| PRIVILEGED | USER_ACTION_REQUIRED; never invoke sudo automatically |
| MANUAL_ONLY | Instructions and evidence requirements |
| RUNTIME_PROVIDED | Detect only; never install |

After failed installation, record failure safely and avoid identical retry loops.
Repair is a new targeted, approved attempt after a real failing verification or
an external condition change, not a blanket reinstall. Retain successful state
for other components.

## Custom MCP intake

Collect name/ID, repository or provider, documentation, capabilities, maintainer,
supported install method, transport, permissions, authentication needs and risks.
Verify these against the provider's primary documentation before classification.
Use only the CLI's allowlisted metadata schema; reject credential-bearing keys,
URL userinfo/query secrets and recognizable secret-bearing free text. Installation
metadata is never evaluated as shell code. Pattern checks cannot recognize every
possible secret, so the executor must review metadata before submitting it.

UNKNOWN stays detect/manual-only. COMMUNITY requires explicit provider-specific
consent. OFFICIAL/VERIFIED_THIRD_PARTY is an audited conclusion, not a status the
provider can self-assert to authorize installation. The current adapter may
require manual configuration for custom MCPs even after consent; say so.

Persist custom metadata and choices only locally. Contribution to the public
library is a separate reviewed change, never an automatic consequence of use.

## Choices

Persist enabled, disabled and not_requested as preferences; keep auth_required
and connected as separate runtime observations, not user preferences. First-use
optional questions are consolidated. A refused
or unanswered choice is not repeatedly shown on every status/prepare invocation.
New task requirements may surface a previously declined capability with a reason;
the requirement does not silently replace the previous choice with consent.

## Validation evidence

Report executable syntax checks separately from behavioral suite results.
Evidence for validators must name commands, successful exit status, time and
the source fingerprint/revision actually tested. Editing the plugin afterward
invalidates that evidence. Do not rerun a mutable project suite during doctor
just to obtain a green badge. Run tests explicitly in their authorized scope,
then import a sanitized observation using the operations contract.
