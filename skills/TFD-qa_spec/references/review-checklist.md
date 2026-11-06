# Specification review checklist

Review in order. Cite a literal excerpt and recommend a correction. Ask the author if there is no citable excerpt.

1. **Ambiguity.** Look for unclear actors or pronouns, unmeasured terms, missing boundaries or units, and reused names with different meanings. `major` if behavior or tests change; otherwise `minor`.
2. **Contradictions.** Compare values, deadlines, limits, actors, flows, and API fields across PRD, Discovery, contract, and spec. Flag claims that exceed Discovery's findings or scope. Usually `blocker`.
3. **Gaps.** Check sources and edge cases: failure, empty state, limits, concurrency, permissions, and rollback. Flag open questions or `UNKNOWN` treated as decisions. `blocker` if implementation cannot proceed; `major` for a material edge case.
4. **Testability.** Require an observable result and expected outcome. Mark human judgment `manual`. A test should fail when the requirement is absent. Usually `major`, or `blocker` if it is the requirement's only acceptance criterion.
5. **Traceability.** Follow approved evidence → REQ → AC, and each AC to its MT and TEST. Flag orphan requirements, criteria or microtasks, malformed or duplicate IDs, tests that miss the criterion, and missing commands. A broken AC → TEST link is `blocker`; REQ or MT without AC is `major`.
6. **Scope.** Verify explicit `scope`, `out_of_scope`, and `allowed_paths`. Flag assumed adjacent work and exclusions that prevent acceptance. `blocker` if scope cannot close; `major` if ambiguous.
7. **Unstated assumptions.** Check library versions, volume, timezone, language, currency, availability, external behavior, and dependencies on future tasks or sectors. `major`, or `blocker` if implementation depends entirely on it.
8. **Security and data.** Check personal-data purpose, retention, masking and lawful basis, authn/authz, input and upload limits, secrets, sensitive logs, and audit of critical actions. Usually `blocker`.

Use `REWORK` for any `blocker` or `major`; otherwise use `PASS`. The author fixes findings. QA revalidates.
