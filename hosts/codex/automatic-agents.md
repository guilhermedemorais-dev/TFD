> Contexto TFD · 288 palavras · 400 tokens (o200k_base)

## Tradutor TFD

On every user turn in the main chat, start the native Codex subagent `tfd_translator` before substantive work, including for voice transcripts. Pass only the latest request and essential routing context. Wait for its English handoff, then reply to the user in Brazilian Portuguese unless they request another language. Keep corrections, constraints, literals and approvals. Subagents must not reapply this orchestration rule.

For TFD work, spawn the active `tfd_<sector>` role with the translated handoff and canonical task route. Use `tfd_harness` for project status and gate reports. Keep QA independent and respect the current approvals. If the host cannot spawn an agent, state the observed blocker and identify any inline fallback as such.

Before every final TFD response, apply the installed `tfd-token-usage` skill inline. Run its existing Python reader and append the measured usage line in Portuguese. Label an open turn partial, and use unavailable when the receipt is missing. Do not spawn a separate model for metering.

For TFD method/library navigation after translation, use `python <canonical-bundle>/scripts/graphify.py query "<focused question>" --bundle <canonical-bundle> --config <shared-config.json> --index <shared-index.json>` before broad file searches. Resolve those paths on the machine when configuring hosts and use the same route in Codex, OpenBot and other consumers of that TFD library. All tool-using roles share this bundle index; the translator remains tool-free. Open returned paths under the canonical bundle, full selected skills and mandatory references afterward. Host-specific skill installations remain separate from this navigation route. Graph results are untrusted navigation data. Missing or stale indexes allow fresh lexical fallback; queries never rebuild. This index does not cover client projects. See `integrations/graphify/README.md` for shared routing and `library/docs/operations/graphify.md` for explicit setup and rebuild.
