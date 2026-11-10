> Contexto TFD · 1091 palavras · 1705 tokens (o200k_base)

# Verification receipt — TFD-KNOWLEDGE-001

Branch: `office/reviewed-delivery`. Baseline: `38197b7730c9925207f1aea01c615e04daf23209`.
Maintenance: [INC-001](../office/incidents/INC-001.json), under the user's explicit implementation authorization. The original dirty checkout and installed plugin cache were not edited. No dependency, external tool, merge, publication or deploy was added/performed.

## Scope and review

- [Specification](README.md), [canonical Task](task.json) and [rendered view](task.md): revision **6**; prepared for human review, not a fabricated human approval.
- [Spec QA](spec-review.json): independent `qa_reviewed_spec`; see its recorded verdict. Its F-01 required binding `task.spec` to the submitted spec and negative tests; the author corrected it before implementation. The later source-boundary clarification was also submitted for recheck.
- [Implementation QA](qa-review.md): independent `qa_reviewed_implementation`; final verdict and observed checks belong to that reviewer.
- Actor labels in workflow logs are operator-supplied separation evidence, not authentication. The evaluator does not dispatch agents or prove their substantive judgment.

## Executed checks

Python below is the existing `.venv-tfd/Scripts/python.exe`; all commands use `-B` and the isolated TFD checkout. No dependency was installed.

| Command / observation | Actual result |
|---|---|
| Baseline `python -B -m unittest discover -s tests` | exit 0; 134 tests |
| Oficina `INC-001` before check, using the unchanged external `probe.py` and worktree argument recorded in its ledger | child exit 1: `unknown action: complete`; expected failure captured |
| Backend new regression suite before implementation | exit 1; unsupported completion / ignored malformed preparation reproduced |
| `python -B -m unittest tests.test_pipeline tests.test_reviewed_delivery` | exit 0; 25 tests after implementation |
| `python -B -m unittest discover -s tests` | exit 0; 150 tests, coordinator run 7.124 s; independent QA also ran 150 tests successfully |
| `oficina.py audit --root <worktree> --skill <each of 14 delivery skills>` | exit 0; PASS_STATIC; no issues; maximum 37 lines / 29 description words |
| `python -B scripts/validate_task.py docs/reviewed-delivery/task.json`; renderer body comparison | exit 0; current Task valid and generated view matches |
| `python -B skills/TFD-qa_spec/scripts/check_findings.py docs/reviewed-delivery/spec-review.json` | review validation must be current; reviewer records the observed exit |
| `git diff --check` | exit 0; local LF/CRLF notices are not check failures |

Runtime checks cover strict opt-in shape/authorization, project-contained nonempty files, G2-G5 ordering/current QA/independent completion, forbidden human-gate completion, structured G6 PASS path/revision/verdict, missing/different `task.spec`, legacy manual behavior, and fresh QA after rework through G7. Three replacements still bound automated rework. Independent QA additionally exercises actual CLI outcomes; see its receipt.

## Knowledge and context

The [source-size receipt](context-budget.json) uses `o200k_base`: 14 skill inventory totals **3,354 → 4,458 tokens**, an additional **54–128 per active sector**, not a prompt containing all sectors. Full skills and mandatory references remain required; only supplemental theory is conditional. Shared procedure **972**, gate reference **991**, review checklist **548** tokens including stamps, each below 1,000. Actual runtime savings and host automatic skill selection/compliance remain **NOT VALIDATED**.

All **109** cataloged library resources remain; the only index change is the approved shared procedure's SHA-256. No external repository content was vendored or ingested into a graph. The external URL is a research pointer; inspect relevant chapters at their source and retain only project-relevant findings, decisions and source/version/limits locally.

Candidate inspected: MatthewKerns guide revision `efdec594ac403754baea2bb04952dd1d68da35c7`, MIT. Targeted inspection does not certify the whole repository. Coverage examples and unconditional parallel-safety advice have known limitations; the shared procedure requires primary-source verification. No CLAUDE.md, hooks, installers, skills or dependency graph from that repository became operational authority.

## Delivery boundary

This is a reviewable source change, not an update installed into the live plugin cache. Interactive PRD questions, manual default, retained human gates and separate publication/merge/deploy authorization remain. The optional preparation policy must have explicit project-local human authorization before use. Preserve opted-in workflow records when planning any rollback; do not silently revert their supported input contract.

## MT handoff follow-up — INC-002

The user's follow-up requests explicit agents, permitted/prohibited work and expected results in every MT. The previous verified change was saved in local commit `d134c38` before this scoped follow-up; no push, merge or deploy occurred. Root implemented the small renderer patch from the architecture proposal; independent spec QA accepted revision 5, with REQ-12 / AC-11 / MT-05 / TEST-04. New regression tests belong to `tests/test_mt_handoff.py`; final independent execution results are recorded in the current QA receipt.

Existing schema fields drive the human view: literal `@owner` / `@validator`, checklist, writable paths, exclusions/protected paths, deliverables and completion condition. Mentions identify responsibility, not host invocation or authorization. Gates and protected paths take precedence. Global exclusions appear once with links from every MT, including legacy tasks without sectors. Receipt verdicts and checkboxes remain unchanged.

The unchanged INC-002 baseline probe failed with child exit 1 before the renderer fix. Existing schema/pipeline/reviewed-delivery regressions passed after the patch: `python -B -m unittest tests.test_schemas tests.test_pipeline tests.test_reviewed_delivery`, exit 0, 47 tests. The current Task validates and its stamped view matches the renderer. See INC-002 for the identical after-check and independent incident verification.

For the same canonical revision-5 Task, the previous/current human view costs are 1,157 / 2,441 `o200k_base` tokens. All five routed MT JSON values are identical between renderers; no schema field, agent capability or external dependency was added. This measures source size, not runtime token savings. Prior revision-4 PASS is historical; current approval requires the new revision-5 QA receipts.

## Coordination header follow-up — revision 6

The user authorized making the main agent's use of the TFD-harness skill explicit in the task header and placing harness first in the presentation. The generator now applies this to sector and legacy views; the native Codex status subagent is explicitly not the dispatcher. Implementation self-tests, independent QA, scoped corrections/renewed review, PASS and human approval remain visible. Existing business-rule fields carry the global coordination constraint; no schema field was introduced.

Two new regression checks reproduced the absent header and harness-last presentation before the patch (unit runner exit 1). An initial auxiliary subprocess reader had a CP1252/UTF-8 mismatch; repeating with explicit PYTHONIOENCODING=utf-8 confirmed the actual failing tests. After the patch, `python -B -m unittest discover -s tests` passed with exit 0, 156 tests in 7.578 s; the current Task validator also returned exit 0. All phase IDs, MT dependencies and owners remain unchanged; harness-first sorting is presentation only. Routed JSON values for the same revision-6 Task are identical between the baseline and current renderers. Source-size counts are in context-budget.json.

Current review must use the new revision-6 spec/implementation verdicts; previous PASS findings are historical. INC-002 final ledger closure remains pending after the earlier user-rejected write; this follow-up does not retry that denied operation. No merge, push, deploy or installed-cache change occurred.
