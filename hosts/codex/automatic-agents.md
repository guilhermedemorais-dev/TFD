## Tradutor TFD

On every user turn in the main chat, start the native Codex subagent `tfd_translator` before substantive work, including for voice transcripts. Pass only the latest request and essential routing context. Wait for its English handoff, then reply to the user in Brazilian Portuguese unless they request another language. Keep corrections, constraints, literals and approvals. Subagents must not reapply this orchestration rule.

For TFD work, spawn the active `tfd_<sector>` role with the translated handoff and canonical task route. Use `tfd_harness` for project status and gate reports. Keep QA independent and respect the current approvals. If the host cannot spawn an agent, state the observed blocker and identify any inline fallback as such.

Before every final TFD response, apply the installed `tfd-token-usage` skill inline. Run its existing Python reader and append the measured usage line in Portuguese. Label an open turn partial, and use unavailable when the receipt is missing. Do not spawn a separate model for metering.
