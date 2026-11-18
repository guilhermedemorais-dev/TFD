---
name: TFD-discovery
description: "Investigate gaps in an approved PRD using indexed sources. Produce traceable findings for the spec. Use for Discovery or research rework requested by spec QA."
metadata:
  version: "1.10.0"
  owner: "discovery"
---

# Discovery

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md). G2 hands off the source-bound, self-checked package; G3 supplies its independent coverage review and acceptance. Do not invoke a second QA merely for the handoff.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md). Research is not limited to manuals 001-080: inspect relevant repository chapters at the external source, then verify decisive claims with primary sources. Keep only its URL/revision as a source pointer; never vendor or graph the whole repository. Keep a bounded question, owner and sufficient-evidence stopping condition; reuse compatible project findings.

1. Derive spec questions and project type (web, mobile, desktop, or other) from the approved PRD and project evidence. Ask if the type is unclear and affects research.
2. Search the project's `docs/discovery/` and relevant ADRs for the question and technology version before fetching supplemental sources. Reuse a verified, still applicable finding by reference. Reopen the original section when scope, version, evidence or decision changes. For unresolved gaps, use the [TFD library index](../../library/indexes/resources.json) and Graphify to locate relevant bundle sources. Keep required reads.
   If reverse engineering could answer a question, ask whether to use REA and which compatible variant the user authorizes for that project type. Confirm the target and scope, reusing valid authorization already given. Use reference software only if the user identifies it. Delegate authorized investigations through the [complete external REAP plugin](references/rea-prompts.md); retain Discovery ownership and evaluate the returned evidence. Call only the authorized variant on the authorized target. While approval, target, or capability is missing, continue independent research.
3. Report an inaccessible index path and use canonical lexical lookup; a retrieval failure does not waive required reads. Mark essential unresolved gaps `BLOCKED` and other gaps `UNKNOWN`.
4. Within authorized read-only research, resolve technical gaps autonomously; do not wait for the user to supply a source. For technical docs, try Context7 first, then official docs directly as needed. Reuse prior business answers; route only missing material business choices to Product. Ask for scope or permission only when required. Record consulted, verified sources in project `docs/`.
5. Write short, project-specific findings with the source section, revision and applicability limits to `docs/discovery/` using the [output contract](references/evidence-format.md). Before G3, author `coverage.json` using the [coverage contract](references/coverage.md), with requirements, business rules, areas and evidenced flows. Link the finding at handoff. Run `python <skill-dir>/scripts/check_evidence.py <sources.json> <evidence.json> --coverage <coverage.json> --require-coverage`.
   For authorized analysis, record the target, revision, and evidence limits.
6. Submit findings and coverage to independent G3 QA before spec authoring. Supply the approved PRD references and all applicable sources; the reviewer performs and records their own consultation. QA reviews matching Discovery, coverage and spec revisions together; checker success is structural validation, never QA `PASS`. For research rework, revisit the flagged question, update evidence, and send the affected spec for correction and joint review. Production requires QA `PASS` and human approval.

Discovery gathers evidence. Leave architecture, implementation, and task approval to later stages.
