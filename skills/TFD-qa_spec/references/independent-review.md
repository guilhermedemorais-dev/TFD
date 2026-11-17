# Independent source consultation

Use at G3/G6 when workflow `review_version` is 1. Keep the four-field `findings.json` unchanged. The reviewer writes a separate project-local consultation JSON and adds its relative path as `consultation` and content hash as `consultation_sha256` to the review event. Never generate a reviewer receipt from the author's claims automatically.

The consultation records:

- `version: 1`, `reviewed_by` equal to the actual review actor, `artifact` and `revision` equal to the reviewed submission, and `findings_sha256` for the exact findings file.
- `references`: `{kind, path, sha256, locator}` for the approved G1 `prd` and `approval`; current `coverage` at G3; current `spec`, `task` and `discovery` at G6. Paths are project-relative. Read the source content at the recorded locator; a hash only detects changes.
- `approved_inventory`: `requirement_ids` and `business_rule_ids` extracted independently from the approved PRD. Compare it with Discovery and the task. Do not copy the author's reduced inventory or infer requirements by regex on arbitrary prose.
- `comparison`: `omitted_ids`, `extra_ids`, `contradicted_ids` and `observation`. Compare rule content, deliverables, acceptance criteria and restrictions as well as IDs. Name the actual discrepancy or the concrete comparison performed.
- `checks`: `{kind, claim_ids, source, revision, locator, status, observation, limits}`. Include `business_decision`, `guide` and `primary` kinds. Link the claim IDs to the checked inventory. `source` names the actual project record or HTTPS origin; record the original version/section and what it supports or contradicts.

For business behavior use the approved decisions, not an engineering convention. For technical design independently open applicable chapters of the [pinned guide](../../../library/architecture/technical-decision-procedure.md#bounded-research-at-any-stage), then verify decisive claims in original vendor documentation or specifications. The guide is a candidate, not authority. Do not force patterns, TDD, percentage targets or all 80 topics onto the project.

Statuses are `VERIFIED`, `NOT_VERIFIED`, `CONTRADICTED` or `N/A`. Explain a specific N/A in `observation`; business decisions cannot be N/A when rules apply. An inaccessible decisive source stays NOT_VERIFIED. Missing or contradictory required facts require REWORK with actionable major/blocker findings. PASS requires matching inventories, no outstanding discrepancies and resolved applicable source checks. Do not repair the author's artifact during independent review.

Before returning, run the pipeline against the actual workflow and report its command/exit. It checks bindings, hashes and declarations; it does not authenticate the reviewer, prove that a page was read, verify arbitrary official-domain claims or certify semantic correctness. State these limits and distinguish documentary review from executed application tests.

Reuse applicable source records and link detailed evidence once in the project. Recheck changed claims and impacted dependencies. Existing workflows without `review_version` retain their prior review protocol; upgrade them only through an explicitly scoped review, preserving earlier PASS records.
