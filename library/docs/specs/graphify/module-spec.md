# Graphify bundle retrieval acceptance criteria

Status: design reference for a proposed TFD integration.

## Requisitos

| Requirement | Acceptance criterion |
| --- | --- |
| REQ-01: explicit, local, pinned Graphify indexing | AC-01: only `rebuild` creates an index; actual upstream deterministic extraction/build runs in an isolated Python environment. No install, LLM, remote ingest or host configuration side effect. |
| REQ-02: bounded retrieval with provenance and freshness | AC-02: output has source revision, corpus fingerprint and per-source SHA256. Dirty changes, corpus identity changes, unsupported schema/pin and corrupt indexes cause fresh local fallback; query never silently rebuilds. |
| REQ-03: shared bundle retrieval | AC-03: one index spans current agents, skills, library, docs, maintenance, integrations and scripts, plus root entrypoints. Canonical legacy plugin references are included; frozen migration snapshots and historical receipts do not override current sources. All roles may query; selected full skills and mandatory references remain required, including on no match. |
| REQ-04: safe derived data | AC-04: reject symlink/hardlink/special files, credential paths and secret-like contents; stage only approved files before upstream extraction. Graph content is untrusted navigation evidence; inferred relations grant no authority. Output and subprocess limits apply. |
| REQ-05: resilient operation and honest measurement | AC-05: missing Graphify/index, extraction failure, stale or corrupt cache yields bounded fresh lexical pointers. Compare output bytes with corpus bytes only as a proxy, never actual token savings or task fidelity. |

Prepared before implementation: positive real extraction/query smoke; missing dependency/index; dirty addition/change/removal; same paths in a different bundle; invalid schema/pin/graph; symlink and credential exclusions; injected instruction treated as data; bounded output; no-result mandatory reads. LLM interaction/host behavior remains NOT_RUN.
