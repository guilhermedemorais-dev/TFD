> Contexto TFD · 162 palavras · 298 tokens (o200k_base)

# Graphify retrieval for TFD

`tfd_graph.py` indexes the shared TFD bundle with the pinned local Graphify
extractor. `worker.py` verifies the installed version and source hash in
`pin.json` before loading it. No upstream skill, host hooks, LLM or remote
ingestion is enabled.

Use `python scripts/graphify.py query "<focused question>"` for navigation.
Only an explicit `rebuild` writes the index. Missing, stale or invalid indexes
return fresh lexical pointers; selected skills and mandatory reads still apply.

Extraction runs on POSIX; Windows uses WSL 2 for rebuilding and a native
query-only Python environment for traversal. Runtime configuration and index
belong to the local Codex profile, outside the plugin and client repositories.
The indexed corpus is the TFD bundle, not client project code.

[Setup and operations](../../library/docs/operations/graphify.md) ·
[Acceptance criteria](../../library/docs/specs/graphify/module-spec.md)

Upstream: [Graphify-Labs/graphify at 8e6a6d2](https://github.com/Graphify-Labs/graphify/tree/8e6a6d2129d4aeffc7a0e9ed79b153f7f057f42b),
`graphifyy` 0.9.101, Apache-2.0. Adapter license notices are preserved in source.
