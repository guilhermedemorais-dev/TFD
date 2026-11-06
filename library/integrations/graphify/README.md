# Graphify adapter

Source of truth: [operations](../../docs/operations/graphify.md) and
[module acceptance](../../docs/specs/graphify/module-spec.md).

`office_graph.py` owns corpus filtering, provenance, freshness, bounded output and
local lexical fallback. `worker.py` bridges actual pinned Graphify extraction,
build and traversal APIs in an explicitly selected Python environment.
`pin.json` binds upstream version, commit and all Python source bytes. This is
not Graphiti, an embedding database, a new model, or semantic LLM indexing.
