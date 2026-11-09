> Contexto TFD · 86 palavras · 143 tokens (o200k_base)

# Graphify retrieval for TFD

The TFD adapter and isolated worker are packaged in `integrations/graphify/`
at the plugin root. Use `scripts/graphify.py` for Windows/WSL or native POSIX
dispatch. The upstream assistant skill is not installed.

The adapter filters the shared TFD bundle, checks provenance and freshness,
bounds output and provides fresh lexical fallback. Runtime activation and
graph rebuilding are explicit actions. Client projects are outside this corpus.
[Operations](../../docs/operations/graphify.md) ·
[Acceptance criteria](../../docs/specs/graphify/module-spec.md) ·
[Research references](../../../README.md#referências-técnicas)
