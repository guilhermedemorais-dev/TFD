# Codex adapter

The plugin root contains the native manifest and local marketplace. From that
root, inspect the listing and install on the selected Codex profile:

```powershell
codex plugin marketplace add (Get-Location).Path --json
codex plugin list --marketplace tfd-local --available --json
codex plugin add the-factory-developer@tfd-local --json
```

Prepare the Python tools once per machine. The installer creates or reuses an
isolated environment, installs the declared packages, and downloads the default
tokenizer vocabulary for subsequent local use. Run from the TFD root:

```powershell
$tfdVenv = Join-Path $env:LOCALAPPDATA 'TFD\python'
python -B scripts/install_python.py --venv $tfdVenv
& (Join-Path $tfdVenv 'Scripts\Activate.ps1')
```

If activation is unavailable, call `Scripts/python.exe` in that environment
directly. On Unix, the corresponding interpreter is `bin/python`. Use this
Python for token measurement and skill authoring validation.

Open a new chat in the target project. Select The Factory Developer and use
`TFD-harness` to open or resume the module. The plugin supplies the skills;
the harness selects the current sector, and `agents/*.json` describes its
inputs, outputs, and independent reviewer. Keep approval and workflow logs
under the target project's `docs/`.
Resume a module from its canonical task JSON and workflow log in that project.
The plugin provides the tools. The project's workflow log carries the current
gate, approvals, blockers and evidence used to resume across chats.

To enable visible native subagents, run from the TFD root:

```powershell
python -B scripts/install_codex_agents.py --agents-dir (Join-Path $env:USERPROFILE '.codex\agents')
```

Add [the automatic agent rule](automatic-agents.md) to the active profile's
global `AGENTS.md`, then open a new chat. This registers the Tradutor and TFD
sectors as native roles instead of using the skill as inline guidance only.

The host must confirm shell and any requested connectors are available before
using them. Reviewers need independent context and a distinct actor in the
workflow log. If independent execution is unavailable, request review in a
separate session. If a required capability cannot run, record the limitation
and block the affected transition. REA and other complementary plugins have
their own installation and authorization.

## Token receipts

Before reading selected files into the agent, measure them locally. Apply a
project budget to PRDs and stack notes and the skill limit to individual references.

```powershell
python -B <tfd-root>/scripts/context_budget.py <prd.md> <stack.md> --max-total-tokens <budget>
python -B <tfd-root>/scripts/context_budget.py <prd.md> <stack.md> --stamp
python -B <tfd-root>/scripts/token_usage.py --quota
```

The preflight uses an available `tiktoken` encoding (`o200k_base` by default).
Counts cover the document body and exclude its generated header. Exit 0 means
measured within the supplied budget, 1 means input error, 2 means over budget,
and 3 means tokenizer unavailable (words still reported). Stamp Markdown,
Python, JS and TS in place before hashing. Report other formats, including
JSON, in the run receipt.

`--quota` passes through all statuses and windows returned by the installed
AI Codex Usage reader, including five-hour, weekly and other reported windows.
Use `--quota-reader`
to select its script if discovery is ambiguous, and `--live` for a live query.
The provider reports rate-limit windows as percentages. Compare file tokens
with the context budget allocated for sources, after reserving room for the
existing conversation, instructions, tools and output. Account percentages
cannot be converted into task tokens.

Run the Python collector on Codex events to record measured usage by task,
gate and attempt. Keep the receipt in the target project. Save one receipt
per run or Desktop turn. Label rework with its attempt number.

```powershell
# Codex CLI: capture the run in a private local file.
codex exec --json "<task prompt>" > codex-run.jsonl
python <tfd-root>/scripts/token_usage.py codex-run.jsonl --task COM-004 --stage G6 --attempt 1

# Desktop: use the session JSONL for the chat, then select its turn.
python <tfd-root>/scripts/token_usage.py <session.jsonl> --list-turns
python <tfd-root>/scripts/token_usage.py <session.jsonl> --turn-id <turn-id> --task COM-004 --stage G6 --attempt 2
```

Redirect the collector's JSON output to a file in the project's evidence
directory. Keep the raw JSONL private. It can contain prompts, code and tool
outputs. The receipt contains counters and labels. Exit 0 means measured,
1 means invalid input and 2 means partial or unavailable. For Desktop,
`model_context_window` is the reported window and
`peak_reported_input_tokens` is the largest input count reported within the
selected turn. Input includes cached input. Reasoning is a reported breakdown
and is not added again to total tokens. To measure all work on a task, collect
each separate reviewer or subagent run as well.

## GitHub CI handoff

Keep project-specific CI in the target repository's `.github/workflows/`.
Document commands, required checks, and evidence paths in that project's
`docs/`. The TFD DevOps sector reads those instructions and reconciles observed
checks with the task. An approved task can be linked to a GitHub Issue through
an authorized GitHub action or tool. Update the linked Issue in place on rework.
A workflow run alone does not create it.
Publish only the sanitized token receipt when the repository allows it.
