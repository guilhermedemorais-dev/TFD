# Skill-Owned Tools

The Harness maps a required capability to its specialist owner. Each owner
selects, prepares, runs, interprets, fixes, and revalidates its domain tools.
The Harness checks receipts and scope; it does not own installation commands.

The Environment `platform_tools` route selects packaged catalogs for authored
Harness entrypoints. Reuse the persisted OS/runtime selection on `status`, and
route only eligible entries after owner/prerequisite gates. Shared scripts retain
their canonical paths. Windows/macOS pending validation is not permission to use
an unverified route, nor a blanket prohibition on separately compatible external
tools. RAG/context retrieval is supplemental context, not this runtime cache.

`dev-environment-standard` may discover every owner registry and prepare only
the capabilities a task needs through this same helper. It never copies registry
entries or takes over tool interpretation. Owners are discovered dynamically.
For read-only diagnostics use `probe` or `resolve --read-only`; neither writes
or invalidates state. Project-local virtualenv/node_modules executables precede
PATH resolution, and verify/install/run operate in the requested workspace.
CLI run preserves the tool's failing exit code; `--quiet` suppresses tool output
when a consumer needs only the compact receipt. Do not publish raw tool logs.

`devops-standard` owns operational tooling through its own registry. Git and gh
remain usable for basic Harness/executor repository work; registry ownership
does not force a DevOps handoff for a normal commit. Terraform and OpenTofu are
alternatives, not a requirement to install both. `act` is optional and runs real
workflow steps: never treat it as an inert YAML parser. No security scanners
are duplicated in the DevOps registry.

The helper is an execution/cache utility, not a production authorization
firewall. The owner must enforce task and human gates before calling `run` or
`install`. For composite tools supply the subcommand explicitly, e.g. registry
`docker-compose` verifies `docker compose version`, while a run receives
`-- compose config --quiet`. The workspace selects execution cwd; the CLI must
preserve a failing tool exit status so validation cannot silently pass.

Each specialist keeps versioned knowledge in `references/tool-registry.json`.
The registry lists capability, official repository, executable, verification,
and installation policy. It is an initial catalog, not a closed whitelist.
Runtime observations live in ignored `runtime-state/tool-state.json` beside the
skill. They are specific to host, Python prefix, workspace, and optional
`TOOL_RUNTIME_ID` for containers/CI. The active virtualenv is also included.
Never commit this file.
For a separately installed or read-only plugin, set `TOOL_REGISTRY_PATH` to
that skill's registry and `TOOL_STATE_PATH` to a writable, persistent local
state file. Both overrides must be supplied together.

Use `plugins/dev-workflow-standard/scripts/tool-state.py OWNER TOOL ACTION
--workspace PROJECT` for `resolve`, `detect`, `install`, `run`, `invalidate`,
and `install-failed`. The helper never installs implicitly. The owner skill
chooses an official supported installation command compatible with the project.
Its explicit `install --install-method METHOD -- COMMAND ARG...` action runs
without a shell, verifies the resulting tool, and persists state immediately.
The owner must review the command, scope, and privileges before invoking it.
Example: `python3 plugins/dev-workflow-standard/scripts/tool-state.py
dev-implementation-standard python-unittest run --workspace . -- --version`.
Detection of an already installed tool also records the state immediately.

Fast path: `resolve` returns a compatible installed executable/version; run it
directly without repeated network discovery. Slow path: missing, stale, changed
environment, missing executable, or incompatible required version means detect,
choose official installation if needed, verify, and persist. If actual execution
shows a broken installation, invalidate it and rebuild the state. A failed
install is recorded with reason and timestamp; do not repeat the same failed
attempt in the same cycle, but retry after the external condition changes.

The owner runs the project-native validation first when appropriate. A tool
finding is a candidate, not a confirmed defect. On FAIL: analyze, confirm,
correct inside scope, run again, and record final validation evidence. Escalate
scope, architecture, spec, privilege, credential, or persistent tool failures.

When applicable the `EXECUTION_RECEIPT` includes skill, capability,
`tool_planned`, `tool_used`, `tool_repository`, `tool_version`,
`tool_state_source`, `installation_performed`, `installation_source`,
`initial_result`, `findings`, `corrections`, `final_result`, and
`validation_evidence`. The Issue `EXECUTION_REPORT_COMMENT` summarizes tool
preparation and meaningful findings for humans without local paths or logs.
