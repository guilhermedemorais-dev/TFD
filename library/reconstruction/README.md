# Evidence to specifications and reconstruction

Local V2 extension inspired by the reviewed Replica pack, not its runtime or
eleven-stage workflow. Load this file only for reference-product discovery,
behavior reconstruction or the associated coverage check. Preserve the current
REA gateway, SDD hierarchy, approved stack, one Task per module and owner gates.

## Capture and handoff

1. Reuse the current PRD, specs, source inventory and findings before inspecting
   a reference. Identify authorized target, version/date and the question.
2. Extend existing records with the [inventory template](inventory-template.md)
   where needed. Use stable existing IDs; add screen/flow/evidence IDs only if
   absent. Classify OBSERVED, INFERRED or UNKNOWN and link each material claim to
   a source revision and exact evidence. Reference screenshots are research
   assets, never product assets. Do not copy proprietary code, identity or content.
3. Separate reference behavior, proposed improvement, approved requirement,
   implementation declaration and verified result. Only approved scope feeds
   the current canonical Task/JSON. An inferred data model is not a verified
   database schema. Record missing access rather than inventing behavior.
4. SDD links evidence -> approved requirement -> rule/state -> acceptance ->
   test using existing IDs. Extend existing module/page/component/API/database
   specs, not a second `replica/architecture.md`. Detail actors, permissions,
   pre/postconditions, states/transitions, persistence, errors, integration
   failures and applicable races/idempotency. Keep visual and backend evidence
   distinct. Approved product changes use existing revision/equivalence gates.
5. Implementation records what was built; QA independently verifies outcomes
   and relevant negative cases at the exact artifact revision. UI owns visual
   validation; Security and DevOps keep their own gates. A skeleton, fake data,
   unit suite or screenshot cannot prove a complete integrated flow.

## Feedback and differences

When differentiation is part of scope, collect current real feedback before
finalizing requirements. Keep source URL/date, exact short supporting excerpt,
sample size, deduplication and limitations. Verify source independence by actual
origin, not an arbitrary CSV label. Keyword matching can misread negation and
positive reviews; review themes against originals, including Portuguese when
relevant. A complaint supports a hypothesis, not automatic roadmap approval.

Report functional gaps separately from design differences. Never average visual
similarity into functional completeness. Blank/cropped screenshots, different
states/viewports and missing comparisons are inconclusive. Mandatory criteria
cannot disappear through `skip`, low weighting or denominator changes. Changing
scope requires the approved canonical Task revision, not an evidence-ledger edit.

## Optional coverage checker

`coverage.py` checks the existing Task's canonical acceptance and required-test
IDs against a **mutable evidence index**, not another execution contract.

```sh
python library/reconstruction/coverage.py --project-root /absolute/project --contract docs/execution/TASK.json --ledger docs/receipts/coverage.json --source-revision EXACT_ARTIFACT_REVISION
```

The ledger carries `task_id`, `contract_revision`, `contract_sha256`,
`source_revision` and `criteria`. Each criterion has `id`, `declared_state`
(`PLANNED`, `IMPLEMENTED`, `PARTIAL`, `SKIP`, `UNKNOWN`) and `cases`. Each case
has `test_id`, `status` (`PASS`, `FAIL`, `NOT_RUN`), `source_revision`, `path`
and `sha256`. Paths are project-relative evidence files. Every canonical
criterion needs IMPLEMENTED plus current PASS case evidence. All canonical
required test IDs must be represented. Missing/skip/partial/stale/failed cases
block completeness. Do not fill this index before checks actually execute.

Exit 0 means all required evidence records are present with matching hashes;
1 means incomplete coverage; 2 means malformed/unsafe input. The helper does
not execute tests, authenticate authors, verify semantic sufficiency, inspect
an Issue or attest independent owner approval. The caller must supply the
current artifact revision, including an uncommitted-worktree fingerprint when
applicable. A hash is integrity metadata, not a signature or authorization.
No exit code authorizes merge, deploy or scope changes.

## Provenance and rationale

Reviewed source: [Replica Skill](https://github.com/Jakeschincariol/replica-skill/tree/77c9436fb3d18c3d58169efb8caf4fe906b0dc51),
manifest 1.0.0, MIT, copyright 2026 Jake Schincariol. The local procedure and
checker are independently written; no upstream code or skill body is bundled.
Any future substantial copied portion must preserve its MIT copyright/license.

Selected ideas: stable screen/flow inventory, evidence-linked feedback and gap
reporting. Existing Office SDD/REA already supply ownership, traceability and
technical specs; those remain canonical. Rejected upstream behavior: replacing
the workflow, default managed stack, weighted release score and unconditional
launch sequence. Reviewed `parity.py` returns 0 with missing must-haves unless a
threshold fails, and `skip` removes rows without approval. The local checker
uses canonical criteria and explicit evidence instead of that heuristic.
