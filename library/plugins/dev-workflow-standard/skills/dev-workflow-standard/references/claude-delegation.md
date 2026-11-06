# Executor LLM Delegation Protocol: Claude Code Adapter

Use this adapter when the orchestrator agent selects Claude Code as the executor
LLM for bounded implementation work. Agent roles remain provider-neutral.

## Objective

Reduce Codex context and token consumption without weakening source-of-truth,
review, QA, security, or user approval gates.

## Mandatory Trigger

Delegate the code-writing checkpoint to an executor LLM when any of these apply:

- a feature, refactor, integration, migration, or non-trivial bugfix is requested
- implementation spans more than two files or more than one technical concern
- the expected patch is larger than a small localized edit
- repetitive code, tests, component work, or mechanical changes are required
- a PRD, spec, roadmap phase, or implementation checkpoint exists

The orchestrator agent may edit directly only for genuinely small changes such as a typo,
single-line config correction, tiny documentation adjustment, or narrowly
localized patch that does not justify delegation overhead.

## Availability Gate

When Claude Code is the selected executor LLM, run:

```bash
command -v claude
claude --version
claude auth status
```

Set `CLAUDE_STATUS`:

- `AVAILABLE`: binary exists and authentication is valid.
- `SANDBOX_NETWORK_BLOCKED`: authentication is valid, but a delegated prompt fails with DNS, connection, API network, or timeout symptoms inside the restricted workspace.
- `INSTALLED_ONLY`: binary exists but authentication or provider setup fails.
- `UNAVAILABLE`: binary is missing or cannot start.

Use a minimal prompt test only when auth status is inconclusive. Do not spend a
model request on every checkpoint merely as a health check.

When `CLAUDE_STATUS != AVAILABLE`, record the matching LLM availability state
and use `llm-handoff.md` to select another authorized executor LLM. Do not make
the orchestrator agent silently absorb implementation work.

### Restricted Workspace Recovery

The current workspace may allow the `claude` binary and local authentication
checks while blocking outbound API traffic. When `claude -p` fails or times out
with connection, DNS, network, or API transport symptoms:

1. Keep the same bounded prompt, working directory, tool allowlist, and checkpoint scope.
2. Set `CLAUDE_STATUS=SANDBOX_NETWORK_BLOCKED`.
3. Retry the same command with the platform's approved external-network or escalated execution path.
4. Ask for user approval through the execution permission mechanism when required.
5. If the escalated retry succeeds, set `CLAUDE_STATUS=AVAILABLE_EXTERNAL` and continue normal diff review.
6. If it also fails, persist `EXECUTION_HANDOFF` and select another authorized
   executor LLM; stop only when no capable LLM is available.

Do not repeatedly run ordinary sandbox retries after the network-block pattern
is established. One restricted attempt and one approved external retry are
sufficient for the same checkpoint.

## Checkpoint Sizing

Split implementation before calling the executor LLM:

- one layer, module, or coherent responsibility per checkpoint
- one objective and one expected diff per invocation
- normally no more than five directly changed files per checkpoint
- one to three acceptance criteria per checkpoint
- database, backend/API, frontend/UI, tests, and docs stay separate when they can be reviewed independently

If a coherent change requires more files, explain the coupling in the brief.
Never send an entire multi-phase project as one executor prompt.

## Context Budget

Send identifiers and paths, not the full orchestrator conversation or a second
compressed copy of the contract.

Include only:

- `task_id`
- `execution_contract_path`
- sector and phase for routed contracts
- current branch/revision
- relevant prior receipt or handoff path when resuming
- output instruction: return only changed files, tests, and blockers in at most 12 lines

Do not paste whole repositories, long chat transcripts, unrelated logs, or
complete documentation trees. The executor validates the contract, then reads
its routed Task sections, relevant global constraints, named sources with
purpose and mandatory skills. Harness reads the complete Task; the specialist
uses `context-routing.md` and requests expansion when needed. The orchestrator
agent inspects the resulting files, receipt, and diff instead of requesting a
long implementation explanation.

## Execution Command

The default delegation mode for Guilherme is `VISIBLE_TERMINAL`. Create a
temporary prompt file containing the bounded brief, then run the bundled helper
with approved GUI/external execution:

```bash
plugins/dev-workflow-standard/scripts/claude-visible-delegate.sh \
  "<canonical-project-root>" \
  "<prompt-file>" \
  "<status-file>"
```

Resolve the helper from the installed plugin root when operating in another
repository. The helper opens `gnome-terminal`, starts the real interactive
Claude Code CLI with the checkpoint already submitted, and writes the exit code
to the status file after the user ends Claude with `/exit`.

While the selected executor LLM is active:

- The orchestrator agent must not edit the delegated files.
- The orchestrator agent may poll status without duplicating the executor conversation.
- The user can watch Claude's native interface, tool calls, and edits directly.
- The orchestrator agent begins diff review only after the status file exists.

Opening a GUI terminal requires the platform's approved external/escalated
execution path. Request that approval through the execution permission
mechanism. Do not replace visible mode with a hidden call merely to avoid the
approval prompt.

If no graphical session or supported terminal exists, report that visible mode
is unavailable and ask before using the headless fallback. The fallback command
is:

```bash
claude -p "<bounded implementation brief>" \
  --permission-mode acceptEdits \
  --tools "Read,Edit,Write,Glob,Grep" \
  --output-format text
```

This mode allows bounded file edits but keeps shell execution and final
validation with the orchestrator agent. Add tools only when the checkpoint specifically needs
them and the risk is understood. Never use `--dangerously-skip-permissions`.

## Required Visibility

Before invoking the executor LLM, tell the user:

- the checkpoint being delegated
- the allowed scope
- which LLM transport will open
- that the executor agent will implement and the orchestrator agent will review

After the executor returns, report whether it executed successfully and summarize
its claimed changes. Do not imply delegation occurred if no executor ran.

## Review Gate

After every executor checkpoint, the orchestrator agent must:

1. Inspect `git status` and the scoped diff.
2. Reject unrelated edits or architecture drift.
3. Validate the diff against the source-of-truth and acceptance criteria.
4. Run canonical tests, lint, typecheck, runtime, QA, or security checks as applicable.
5. Fix only small review findings directly; delegate substantial rework as a new bounded checkpoint.
6. Record provider availability, whether external execution was required,
   delegated checkpoint, `SKILL_RECEIPT`, `REUSE_INVENTORY`, validation evidence,
   and remaining gaps.

Do not start the next implementation checkpoint until the current diff is
reviewed and reconciled.
