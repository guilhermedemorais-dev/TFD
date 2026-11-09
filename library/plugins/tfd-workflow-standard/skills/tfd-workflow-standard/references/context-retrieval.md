# Context Retrieval

Context retrieval augments the existing `context-routing.md` contract. It is
not a second source of truth and it never changes authorization.

## Backend order

1. Load every Task `required_source` exactly as the contract requires.
2. If additional context is materially useful, invoke `context-retriever.py`.
3. Prefer Potpie when its CLI is installed and healthy.
4. Fall back to local deterministic lexical retrieval when Potpie is unavailable.
5. Return paths/snippets/evidence to the specialist. The specialist still
   applies its canonical skill and the Task constraints.

Potpie is used as an external Apache-2.0 context engine. The Harness integrates
its public CLI contract rather than vendoring the entire Potpie monorepo.

## Security boundary

Retrieval MUST:

- stay inside the resolved workspace;
- enforce `allowed_paths` when supplied;
- reject path traversal and symlink escapes;
- exclude common generated/vendor/secret directories by default;
- never index or print environment variables, credential stores or obvious
  secret files;
- return evidence, not permission.

A retrieved file outside authorized scope may be reported as a possible context
gap, but it cannot be edited or treated as an approved Task source.

## Required versus retrieved

`required_sources` are normative and cannot be omitted because a search engine
did not rank them. Retrieved context is supplemental. If retrieved material
conflicts with a required source, use `source_of_truth_conflict` and stop the
affected checkpoint.

## Output contract

The retriever emits JSON:

```json
{
  "backend": "potpie|local",
  "query": "...",
  "required_sources": [],
  "results": [
    {
      "path": "relative/path",
      "score": 0.0,
      "line_start": 1,
      "line_end": 10,
      "snippet": "..."
    }
  ],
  "warnings": []
}
```

Mutable retrieval results belong in execution evidence, never in the normative
Task JSON.
