---
name: tfd-token-usage
description: "Report observed TFD token use from local Python receipts. Use at the end of each TFD response, for file budgets, or for explicit Codex quota requests."
metadata:
  version: "1.2.0"
  owner: "token-usage"
---

# Token Usage

Run the existing Python counters from the TFD plugin root. Keep raw session logs local. Use the compact JSON receipt as the only source of numeric values. See the [Codex commands](../../hosts/codex/README.md#token-receipts) for exact options.

- **Every TFD final response.** Identify the current thread and turn from host metadata. Resolve its local session JSONL. Use `scripts/token_usage.py --list-turns` if needed, then collect the unique active turn with `--turn-id`. Use the active task and gate or `chat` and `reply`. Report `usage` as cumulative turn consumption, with cached input shown separately and an open turn labeled partial. Mark missing counters unavailable. Keep subagent receipts separate unless all contributing runs are measured.
- **Context warning.** Show `context_window` separately from cumulative `usage` in the response footer. If `warn_handoff` is true, append `Janela de contexto: <percent>%. Digite /compact para liberar espaço neste chat.` beside the consumption summary. Suggest a new chat with a short resume line only if compaction is unavailable or the user prefers to switch. Label a sample from a previous turn the last available reading.
- **Files or context budget.** Run `scripts/context_budget.py` on the selected files and report its tokenizer, counts and budget verdict as estimates.
- **Codex quota.** Run `scripts/token_usage.py --quota` only on a quota request. Report the available windows and resets separately from tokens.
