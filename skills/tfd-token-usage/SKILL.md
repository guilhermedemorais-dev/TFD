---
name: tfd-token-usage
description: "Report observed TFD token use from local Python receipts. Use at the end of each TFD response, for file budgets, or for explicit Codex quota requests."
metadata:
  version: "1.3.0"
  owner: "token-usage"
---

# Token Usage

Run the [Codex commands](../../hosts/codex/README.md#token-receipts) from the TFD plugin root. Keep raw logs local. Report numbers from the JSON receipt.

- **Every TFD final response.** Resolve the current session and turn from host metadata. Use `--list-turns` if needed and select with `--turn-id`. Use the task and gate or `chat` and `reply`. Report total, uncached input, cached input and output. Label open turns partial and missing counters unavailable. Combine subagent receipts only if all contributing runs are measured.
- **Context warning.** Show `context_window` separately. Label previous-turn and pre-compaction samples. Pass `--compact-threshold-percent` only for a confirmed Codex setting. For `compaction.guidance: manual`, preserve the checkpoint and append `Digite /compact para liberar espaço neste chat.` For `native_configured`, report the configured threshold. Codex compacts. Count explicit events from the selected turn. Suggest a new chat only if compaction is unavailable or the user prefers to switch.
- **Files or context budget.** Run `scripts/context_budget.py` on the selected files and report its tokenizer, counts and budget verdict as estimates.
- **Codex quota.** Run `scripts/token_usage.py --quota` only on a quota request. Report the available windows and resets separately from tokens.
