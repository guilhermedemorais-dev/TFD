# Model and Provider Routing

This is a local Engineering Harness extension. It resolves **where** an owner
skill executes. It never changes **which skill owns the work**.

## Invariant

```text
Task / execution_list
  -> capability
  -> owner_skill
  -> provider/model resolver
  -> context retrieval
  -> executor runtime
  -> receipts
  -> Harness validation
```

Skills define methodology. The Task defines authorized work. Providers/models are
replaceable runtimes. Context retrieval supplies evidence; it is not authority.

## Availability states

Keep these distinct:

- `UNCONFIGURED`: credential/configuration is absent.
- `CONFIGURED`: required environment variable exists, but no remote call proved it works.
- `AVAILABLE`: an observed provider probe succeeded.
- `DEGRADED`: the provider exists but the requested capability/model is not verified.
- `UNAVAILABLE`: probe failed or runtime explicitly rejected the request.
- `ADAPTER_REQUIRED`: provider is known but the active host needs a verified adapter.

Never infer AVAILABLE from a TOML block or environment-variable name.

## Selection

1. Resolve the current execution list and `owner_skill`.
2. Load that skill and mandatory references. Provider selection never precedes
   skill ownership.
3. Determine the capability requested by the list, for example `coding`,
   `reasoning`, `qa`, `security`, `tool_use` or `long_context`.
4. Enumerate only providers that are configured and whose runtime probe can be
   performed safely.
5. Prefer an explicitly approved provider/model. Otherwise select the lowest
   priority number that can prove the requested capability.
6. If the active provider fails, persist `EXECUTION_HANDOFF` and continue the
   same list with another compatible runtime. Never restart completed work.
7. If no compatible runtime exists, return BLOCKED or single-agent/degraded mode
   explicitly. Do not pretend that delegation occurred.

The versioned provider registry contains public metadata and setup links only.
Secrets stay in host secret storage or environment variables.

## NVIDIA

NVIDIA NIM is treated as a provider, not one agent per API key. One configured
credential may expose multiple models. Model discovery must query the provider
at runtime. Technology/coding hints are ranking hints only; they are not proof
that a model satisfies a Task. The Harness can expose every discovered model,
while routing only models whose required capability was verified or explicitly
approved.

## Codex configuration

The installer may generate a **proposed** provider block for the user's
`config.toml`, but must merge conservatively, back up the original and never
write a secret value. Runtime compatibility is tested after configuration.

## Evidence

Record provider/model/runtime in the existing `EXECUTION_RECEIPT` and
`EXECUTION_HANDOFF`. Do not create another Task or another completion system.
