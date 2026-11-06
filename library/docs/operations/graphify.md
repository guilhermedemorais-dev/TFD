# Shared Graphify retrieval

Use one derived index of the Office bundle across CTO Global, project
orchestrators and workers. Query it for relevant files and relationships, then
read the selected canonical files, full selected skills and mandatory references.
A query, no match, graph edge or cache never replaces those reads, role ownership,
Task/spec authority, independent validation or human approval.

## Windows 10 and WSL 2

This worker imports POSIX `resource` and rejects a runtime without those limits.
Use the [WSL 2 operation guide](windows-wsl.md) on Windows 10: Codex CLI, Python,
the isolated Graphify environment and the worker run in the selected Linux
distribution. Installing WSL does not move a Windows app/session there. Keep its
profiles/configuration separate and regenerate local indices/readiness paths.
This is the selected compatibility route, not executed WSL or native Windows
homologation. The current integration uses the free local engine, not a Cloud
trial or paid Graphify API; Codex account usage remains separate.

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

Use absolute paths. `BUNDLE` is the actual installed Office source root containing
`AGENTS.md` and `agents/`, not a user's software project, skill cache subtree or
another checkout. `INDEX` belongs to an external private cache directory, outside
the bundle. `PYTHON` is the reviewed virtual environment interpreter.

```bash
python3 integrations/graphify/office_graph.py rebuild --bundle /absolute/office-bundle --index /absolute/private-cache/office-graph.json --graphify-python /absolute/graphify-venv/bin/python
python3 integrations/graphify/office_graph.py query --bundle /absolute/office-bundle --index /absolute/private-cache/office-graph.json --graphify-python /absolute/graphify-venv/bin/python --query 'mandatory reference owner'
```

Only explicit `rebuild` writes the index, atomically with private temporary file
permissions. Query never rebuilds. A prepared persistent installation must record
its actual bundle path/revision/fingerprint, index path and interpreter in a local
readiness receipt. Root/session instructions must point every role to those same
paths. Existence or a receipt alone does not prove Graphify dispatch: execute a
query and verify `status: GRAPHIFY` and expected relationships. Registration and
installation are separate from real agent/LLM behavior, which remains NOT_RUN
until exercised on the host. No VS Code installation is part of this adapter.

## Corpus, safety and freshness

The corpus spans root README/AGENTS and `agents`, `skills`, `library`, `docs`,
`maintenance`, `integrations`, `scripts` and legacy `plugins` whose references
remain canonical for selected V2 skills. It reads supported textual source/config
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
This is resource limiting, not OS/network isolation against malicious packages.

Freshness currently reads all selected source bytes for each query. This optimizes
the context returned to an agent, not filesystem I/O. Compare returned UTF-8 bytes
with selected corpus bytes only as a context-size proxy. Neither upstream nominal
budgets nor byte comparisons establish actual model token use, percentage savings,
semantic completeness, task fidelity or delivery success.

## Validation

```bash
python3 -m unittest discover -s tests -p 'test_graphify*.py' -v
```

The deterministic suite covers freshness, identity, corrupt/schema/pin data,
malformed graph elements, symlinks/hardlinks/credentials, canonical legacy
references, injected text as data, fallback, no matches and output bounds. A real
pinned Graphify extraction/traversal smoke is separately required to claim the
Graphify path executed. See the module receipt for observed results.
