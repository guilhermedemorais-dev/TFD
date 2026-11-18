# Complete external REAP capability

REAP is a separate complete skill collection, not three embedded excerpts.
Preserve every upstream file and all 26 packs at the
[pinned source](../../../integrations/reap/source.json). Any applicable pack may
be selected. Selection limits the current context, never the installed catalog.
Use ordinary repository tools for questions answered by complete source alone.

## Invoke through the host executor

1. Resolve the installed `reap-prompts` plugin and its complete
   `skills/reap-prompts/SKILL.md` index from the actual host. Read the index to
   select the matching full skill; do not limit selection to a fixed subset.
   Check separately that the required REA tools and provider are available.
   A skill pack is not an executable engine or an RPC endpoint.
2. Delegate the bounded investigation to an available native agent/executor,
   passing the canonical plugin/index path, question, target and revision,
   already authorized actions, relevant PRD gap and required result. The
   executor reads the selected full `SKILL.md` and applicable REA skill before
   using actual host tools. Do not put every pack in the main agent's prompt.
3. Require the executor to return the selected plugin/pack paths and revision,
   target identity/hash, tools actually used, findings with file/function,
   address or Evidence IDs, observed checks/exits, limitations and unresolved
   questions. Distinguish observation, inference and unknown; static findings
   do not prove runtime behavior or backend enforcement.
4. Discovery evaluates that result, checks relevant original evidence and
   consolidates it under the existing [output contract](evidence-format.md)
   and [coverage contract](coverage.md). The prompt is methodology, not proof
   of a product rule. Independent G3 QA and human gates remain unchanged.

Discovery remains responsible while the external capability performs the
delegated work. If no native executor exists, disclose inline execution as a
fallback using the same installed skill and evidence contract. If the plugin,
engine or required permission is missing, report that exact limitation; do not
claim delegation or engine execution. Continue independent supported research.

The complete collection includes installation, reconstruction, security and
runtime workflows. Availability does not authorize every action: execute only
the user's current task and existing approvals. Discovery research does not
authorize reconstruction or product implementation. Reuse valid target/scope
approval instead of asking again. Upstream setup scripts can replace existing
skill folders; package completeness never requires executing those scripts or
replacing the current REA engine/configuration.

## Separate plugin packaging

Keep the entire upstream repository and MIT license outside the TFD bundle.
Run [the local packager](../../../scripts/reap_plugin.py) with
`--source <pinned-git-clone> --output <new-external-marketplace-folder>`.
It preserves every original file under `plugin/upstream/`, exposes all 26
complete skills under `plugin/skills/`, and records source/body hashes.
The pinned upstream has malformed unquoted YAML descriptions: only that scalar
is quoted in the active copies; names and full bodies remain unchanged.
The [compatibility manifest](../../../integrations/reap/plugin.json) adds no
hooks, MCP registration or onboarding execution.

The generated marketplace is `reap-local`, plugin `reap-prompts`. For Codex use
`codex plugin marketplace add <external-marketplace-folder>` and
`codex plugin add reap-prompts@reap-local --json` commands. Verify all upstream
file hashes, normalized skill hashes and all folders in the installed cache. A later source
revision requires review, not a silent download of `main` or `@latest`.
For another host, use its verified full-skill/plugin registration mechanism;
do not assume Codex commands work in OpenBot or Claude Code.
