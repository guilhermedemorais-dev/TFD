> Contexto TFD · 1192 palavras · 1806 tokens (o200k_base)

# Graphify retrieval

The TFD package includes a shared local index adapter and pinned worker.
Query for relevant files and relationships, then open canonical sources and mandatory
references for the task. The active task, independent review and human approval
remain authoritative.

## Windows 10 and WSL 2

Extraction uses POSIX `resource` limits. On Windows, `scripts/graphify.py`
dispatches explicit rebuilding to WSL 2. Queries can use an isolated native
Windows interpreter, with Job Object process CPU/memory limits, avoiding WSL
launch permissions inside the Codex sandbox. Windows extraction is rejected.
On Linux, the same POSIX environment supports both actions. Lexical fallback
requires neither Graphify nor WSL.

## Source and implementation

Reviewed upstream: [Graphify-Labs/graphify at 8e6a6d2](https://github.com/Graphify-Labs/graphify/tree/8e6a6d2129d4aeffc7a0e9ed79b153f7f057f42b),
branch `v8`, distribution `graphifyy` version `0.9.101`, Apache-2.0.
The adapter verifies distribution version and a fingerprint of all package Python
source against `integrations/graphify/pin.json` before importing Graphify.
Installed dependencies remain part of the trusted local environment. This check
is integrity/provenance, not a sandbox or signature of an untrusted environment.

Rebuild uses actual upstream `graphify.extract.extract(..., parallel=False)` and
`graphify.build.build(..., directed=True, dedup=False)` with AST parsers and
structural Markdown extraction, including explicit links, call relationships and
cross-file references. Markdown is structural, not semantic LLM interpretation.
Queries call pinned private API `graphify.serve._query_graph_text`, BFS depth 2,
with upstream nominal budget 1200 and an independent output byte cap. The CLI's
query logging/stamp writes are deliberately avoided. Private API changes require
review and a new pin; do not silently upgrade. No LLM, provider SDK, embeddings,
remote ingestion, graph server or upstream host-install command is invoked.

## Explicit local operation

Prepare a dedicated virtual environment from the reviewed exact commit and its
inspected dependencies. Installation is a separate authorized Environment action;
this adapter never installs dependencies. Do not run `graphify install` because
it modifies host integrations. Do not install optional LLM/provider extras.

Use absolute paths for the approved bundle, its private index cache and the
reviewed virtual environment interpreter. This indexes plugin resources.
Adapting this integration to a project repository
requires an explicit corpus and a separate acceptance test.

Only explicit `rebuild` writes the index, atomically with private temporary file
permissions. Query never rebuilds and uses bounded in-memory pipes, so it needs
no writable temporary directory. A prepared persistent installation must record
its actual bundle path/revision/fingerprint, index path and interpreter in a local
readiness receipt. Root/session instructions must point every role to those same
paths. Existence or a receipt alone does not prove Graphify dispatch: execute a
query and verify `status: GRAPHIFY` and expected relationships. Registration and
installation are separate from real agent/LLM behavior, which remains NOT_RUN
until exercised on the host. No VS Code installation is part of this adapter.

### Local configuration

After creating a dedicated POSIX virtual environment and installing the exact
reviewed commit above, verify the distribution and source hash using the worker.
Do not use a floating release. The base dependencies are sufficient; provider
and media extras are unnecessary. Keep the environment's dependency lock locally.

Create `$CODEX_HOME/tfd-graphify.json` (default `~/.codex/tfd-graphify.json`):

```json
{"python":"/absolute/venv/bin/python","wsl_distribution":"your-installed-distro","query_python":"C:/absolute/query-venv/Scripts/python.exe"}
```

Omit `wsl_distribution` and `query_python` on Linux. The Windows query-only
environment uses the same verified Graphify wheel and NetworkX; AST/parser
dependencies belong to the separate extraction environment. It cannot rebuild
and is not a full Graphify CLI installation. No upstream assistant skill is enabled.
On Windows use local drive paths on the
standard `/mnt/<drive>` WSL mount. Custom WSL mounts require direct POSIX use.
Run from the TFD root with the host's Python:

```text
python -B scripts/graphify.py rebuild
python -B scripts/graphify.py query "validate_task gates acceptance"
```

Use `python3` on Linux when appropriate. Override `--config`, `--bundle` or
`--index` for isolated checks. The default index is
`$CODEX_HOME/tfd-graphify/index.json`. Missing runtime configuration permits
query fallback but rejects rebuilding. Register current native profiles with
`scripts/install_codex_agents.py --agents-dir <profile>/agents`; tool-using
roles receive the shared query route, while the translator remains tool-free.
Global instructions must resolve `<tfd-root>` to the actual local installation.

## Corpus, safety and freshness

The corpus spans supported root text entrypoints and `agents`, `skills`, `library`,
`docs`, `maintenance`, `integrations`, `scripts`, `hosts` and `schemas`. It reads supported textual source/config
extensions only. Historical frozen snapshots (`v1-frozen`), evidence/receipt/cache
folders, runtime-state, credentials, dependency environments and binary files are
excluded. Actual canonical legacy references remain available; historical prose
never supersedes the active contract/Task. Coverage is bounded by these explicit
filters, not a claim to ingest every byte in the repository.

Reject symlink roots/parents, symlink or hardlinked/special input files, suspicious
credential filenames and recognized secret-like contents. Only filtered files are
copied to a disposable staging tree for upstream extraction, preventing parser
resolution against project files outside that tree. Conservative secret filters
can omit benign files and do not guarantee detection of every secret. Do not
point this tool at projects, credential stores or sensitive corpora.

Cache schema/pin, absolute bundle identity, revision, per-file SHA256 and aggregate
fingerprint are checked against a fresh source scan on every query. Added,
removed or dirty changed selected sources invalidate the old graph. Unsupported,
corrupt, stale or missing indexes and unavailable/mismatched Graphify produce
fresh local lexical pointers, with an explicit status. Graph data and excerpts
remain `UNTRUSTED_DERIVED_DATA`; injected instructions cannot establish policy.
Schema 2 recognizes a Windows drive and its standard `/mnt/<drive>` WSL mount
as the same bundle identity; file hashes, revision and corpus still must match.
`INFERRED` is a graph confidence label, never a normative owner or security fact.
The cache hash detects inconsistency, not adversarial authorship/authenticity.

## Result and limits

JSON includes `status`, bundle/revision/fingerprint, up to six lexical source
pointers with path/line/SHA256/excerpt, optional real `graph_context`, and a reminder
that mandatory reads remain required. Lexical source ranking complements Graphify
traversal; graph relationships are separate evidence, not a replacement ranking.
Failures return bounded fresh pointers even without Graphify installed. Query
inputs are limited to 512 characters; total JSON is at most 16,000 UTF-8 bytes,
Graphify text at most 6,000 bytes. Corpus/index/file/graph limits fail explicitly;
POSIX worker CPU/address-space/file-size limits and wall timeout constrain work.
Windows query workers enforce CPU/memory limits through a Job Object and emit
only bounded query text; Windows has no POSIX file-size limit in this adapter.
This is resource limiting, not OS/network isolation against malicious packages.

Freshness currently reads all selected source bytes for each query. This optimizes
the context returned to an agent, not filesystem I/O. Compare returned UTF-8 bytes
with selected corpus bytes only as a context-size proxy. Neither upstream nominal
budgets nor byte comparisons establish actual model token use, percentage savings,
semantic completeness, task fidelity or delivery success.

## Validation

The deterministic suite covers freshness, identity, corrupt/schema/pin data,
malformed graph elements, symlinks/hardlinks/credentials, canonical legacy
references, injected text as data, fallback, no matches and output bounds. A real
pinned Graphify extraction and traversal check is required before recording
that the TFD integration ran. Local verification evidence is recorded separately
from benchmark claims; installation alone does not establish host behavior.
