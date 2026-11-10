> Contexto TFD · 1606 palavras · 2379 tokens (o200k_base)

# Reviewed task delivery

Task: `TFD-KNOWLEDGE-001`; specification revision: `4`; maintenance route: Oficina `INC-001`.
Status: proposed specification for independent QA. Implementation and verification results are not asserted here.
Source: the user's explicit maintenance authorization recorded in [INC-001](../office/incidents/INC-001.json). It preserves interactive PRD questions, token economy and each implementation stage's review/approval loop.

## Scope and decisions

Extend the existing sector instructions and workflow evaluator. Reuse the current Task schema, project evidence and Graphify adapter; do not add a knowledge engine, dependency, task format or agent. Apply the smallest complete change satisfying the approved requirements, not the fewest lines or a partial fix.

The manual workflow remains the default. An explicitly authorized preparation mode can consolidate technical preparation after an approved PRD; it cannot impersonate a human or approve implementation. A purely advisory mode would not enforce the distinction; replacing all gate approvals would remove the user's retained controls. The selected alternative is therefore a narrow opt-in extension.

## Requirements

| ID | Required behavior | Acceptance / test |
|---|---|---|
| REQ-01 | Product asks only unresolved material PRD questions, reuses answers and keeps business decisions with the user. | AC-01 / TEST-02 |
| REQ-02 | Existing native sectors have concise, role-specific decision/test obligations and conditional topic triggers. | AC-02 / TEST-02 |
| REQ-03 | Missing material context starts bounded research at Discovery or the affected owner, including later architecture, spec, implementation and QA. | AC-03 / TEST-02 |
| REQ-04 | Reuse applicable project evidence; store source/revision, question, applicability, limits, decision, owner and planned/executed checks in existing project records. | AC-03 / TEST-02 |
| REQ-05 | Shared engineering theory is consultative. Graphify locates canonical sources; required reads survive missing/stale retrieval. | AC-04 / TEST-02 |
| REQ-06 | Research covers engineering beyond manuals 001-080; MatthewKerns is an external URL consulted by relevant chapter at origin on demand, never copied or indexed in core/project graphs. | AC-04 / TEST-02 |
| REQ-07 | Optional workflow preparation is strictly scoped to the authorized reviewed-task mode; default manual semantics remain unchanged. | AC-05 / TEST-01 |
| REQ-08 | Coordinator completion applies only to G2-G5 with current prerequisites and independent required QA; other gates retain human approval. | AC-06 / TEST-01 |
| REQ-09 | In the opt-in mode, G6 requires task.spec equal to artifacts.spec and a structurally valid independent spec QA PASS for that exact submitted spec and revision. | AC-07 / TEST-01 |
| REQ-10 | Preserve build, self-test, applicable independent QA, scoped rework and human approval for each implementation phase. | AC-08 / TEST-01 |
| REQ-11 | Preserve bounded context and the existing library; measure before/after source cost without claiming runtime token savings or host behavior. | AC-09 / TEST-02 |

## Workflow extension

Optional root field of the existing workflow log (not of the Task JSON):

```json
{"preparation":{"mode":"reviewed_task","authorization":"docs/authorization.md"}}
```

When absent, retain current workflow behavior and existing tests. When present, require an object with exactly `mode` and `authorization`, the supported mode, and a project-relative existing nonempty authorization file. Reuse existing path validation; reject absolute paths, traversal, escapes, unsupported modes, malformed objects or empty evidence. Authorization is a record of the user's explicit preparation scope, never a grant created by the coordinator. The evaluator validates supplied records; it does not authenticate humans.

In this mode only, add action `complete` at G2, G3, G4 and G5. It uses the current submitted revision and project-relative nonempty completion evidence. It is allowed only in AWAITING_APPROVAL, after every required current review is PASS. Its normalized actor must differ from the submission author and each required reviewer, using existing separation rules. Rework resets reviews and requires a fresh revision; BLOCKED remains blocked.

| Gate | Opt-in terminal action |
|---|---|
| G0, G0.5, G1 | Human `approve`; interactive PRD and scope decision retained |
| G2, G3, G4, G5 | Coordinator `complete`, or an actual independent human `approve` |
| G6, G7, G8-review, G8 | Human `approve`; coordinator `complete` rejected |

Do not accept `complete` without opt-in authorization, before submission/QA, on stale revisions or from an author/reviewer. No extra stage is skipped. This policy changes preparation only; publication, installation, merge, production data operations and deploy retain separate authorization.

For G6 in the opted-in workflow, read the `qa_spec` review evidence as the existing findings JSON and validate it with `skills/TFD-qa_spec/scripts/check_findings.py`'s `validate_findings`. Require JSON verdict PASS, `artifact` equal to the submitted `artifacts.spec` project-relative path, and `revision` equal to the review/submission revision. A text file, malformed findings, REWORK content hidden behind a PASS event, different artifact or stale revision cannot satisfy G6. Require the existing canonical Task field `task.spec` to equal the current submission's `artifacts.spec` project-relative path. Missing or different `task.spec` is rejected in this mode even when valid PASS findings name the submitted spec; no new Task field is introduced. Keep current author/reviewer separation and artifact SHA-256 checks. The same submission binds the spec, matching Discovery, canonical Task identity/revision and generated task view. Findings do not prove substantive correctness: independent QA still reads matching sources and acceptance checks.

## Research and context contract

Load the sector's full skill, its routed Task slice, global approved constraints and all applicable mandatory references. Consult only relevant supplemental topics and exact source sections; no whole-library or all-manual preload. Use the shared technical decision procedure and existing reference IDs, not copies of every chapter in each skill.

A research checkpoint has a question, affected decision, owner, checked sources/version, unresolved gap and sufficient-evidence stopping criterion. Prefer compatible project records, then verified library and version-matched official sources. Expand when the existing evidence is insufficient or stale. Another technical uncertainty can be resolved within approved scope; a material missing business decision, conflicting authority or permission boundary returns to the user. After three unsuccessful scoped rework cycles, stop with diagnosis, not another identical attempt.

The MatthewKerns repository remains an external source: https://github.com/MatthewKerns/software-development-best-practices-guide. Record only that external URL in the shared source pointer; consult relevant chapters at their origin on demand, critically checking claims and examples beyond manuals 001-080. Do not copy, vendor, distribute, ingest, chunk or index repository content in either the TFD core graph or project graphs. Project records may retain bounded project-specific decisions and evidence with chapter URL, inspected revision and limits, never a local corpus of that repository. Do not import its CLAUDE.md, skills, hooks, installers, MCP or dependency graph as authority. Do not impose a pattern, cloud, numerical style threshold or TDD rule merely because a manual recommends it.

Persist bounded project-specific findings, alternatives, accepted decisions, contracts, risks and AC/test links using the existing project documentation/reference fields. Distinguish facts, local decisions and assumptions, and planned checks from executed evidence. Recheck source applicability when versions, boundaries or contradictory evidence change; no arbitrary freshness TTL. Do not promote client knowledge into the global plugin or rewrite installed caches. A missing retrieval index does not waive required sources; a missing essential source blocks only its dependent claim.

## Phases, owners and validation

1. Architecture authors this specification and the single current-schema Task/view; independent spec QA reviews the exact revision before implementation.
2. Harness maintains native instructions and shared references; backend implements the narrow workflow behavior and its regression tests.
3. Independent QA verifies both the behavior and instruction boundaries; the coordinator consolidates exact commands, exits, scope and limitations for human review.

| AC | Observable acceptance |
|---|---|
| AC-01 | Product retains interactive questions for missing business decisions; no automatic PRD invention or G1 approval. |
| AC-02 | Existing 14 native delivery skills (harness plus 13 sectors) retain bounded responsibility and explicitly route material technical gaps. |
| AC-03 | Research is available beyond Discovery and returns project-local, version-aware evidence/decisions without duplicating the library. |
| AC-04 | Required reads and canonical authority survive Graphify failure; MatthewKerns remains only an external URL, with relevant chapters consulted at origin on demand and no repository content copied, distributed or indexed in core/project graphs. No external tool is installed. |
| AC-05 | All existing manual pipeline cases retain their result; missing/invalid/empty/outside authorization and unknown preparation shapes fail closed. |
| AC-06 | Authorized G2-G5 completion preserves ordering/current reviews; author/reviewer/stale/premature/forbidden-gate completion fails. |
| AC-07 | Opted-in G6 requires task.spec equal to artifacts.spec; reject a missing/different task.spec even with matching valid PASS findings, as well as text/malformed/REWORK/wrong-artifact/stale findings. Accept matching validated PASS; manual legacy review evidence remains compatible. |
| AC-08 | G6/G7/G8 gates still await actual human approval; applicable QA and the existing three-rework boundary remain intact. |
| AC-09 | Modified skills stay within 150 lines and descriptions within 60 words; shared procedure and gate reference each stay within 1,000 measured tokens; report comparable before/after counts without fabricated runtime savings. |
| AC-10 | The canonical Task validates against the existing schema and its Markdown sibling matches the same revision rendered by the existing script. |

TEST-01: `python -B -m unittest tests.test_pipeline tests.test_reviewed_delivery`. Include a negative case with current valid PASS findings for artifacts.spec while the canonical Task points to another spec, and a case with task.spec missing; both must fail only in opted-in mode.
TEST-02: `python -B -m unittest tests.test_discovery_skill tests.test_qa_spec_skill tests.test_reviewed_delivery` plus measured context-budget and independent scenario review.
TEST-03: `python -B scripts/validate_task.py docs/reviewed-delivery/task.json` and verify its Markdown sibling equals the existing renderer output.
Full regression before delivery: `python -B -m unittest discover -s tests`.

## Limits and recovery

There is no client application schema/data migration, API endpoint or production deployment in this maintenance scope; those sections are N/A. The existing workflow-log extension is an input contract, not a new Task schema. Test with synthetic disposable projects, no secrets and no external mutation. Restore modified source from the reviewed branch revision if regression checks fail; any already-used opted-in logs need an explicit compatibility decision before reverting support. Preserve approvals, evidence and the original checkout's preexisting changes. Host instruction compliance and total run-token improvements remain NOT VALIDATED until observed; structural tests alone cannot prove them.
