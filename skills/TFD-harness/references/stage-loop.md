> Contexto TFD · 494 palavras · 645 tokens (o200k_base)

# Source-backed production stages

Use when the workflow declares `stage_loop_version: 1`, requiring coverage and review version 1. New initialization enables it; do not rewrite legacy approvals to imply new checks. Read the [executable receipt contract](../../../docs/stage-loop.md) for fields and the gate/reviewer matrix.

Within **each** production stage, including PRD, environment readiness, documentation and operations:

1. The owner identifies the current question, scope and artifacts. Query Graphify for relevant TFD references, then read the selected canonical sources and mandatory references. On unavailable/stale indexing, record the actual status and lexical fallback. Reuse a hashed prior navigation record only after checking source versions and present applicability. Never load the whole library or require a fresh network request for unchanged verified facts.
2. Produce the bounded deliverable and run its applicable self-checks. Record actual commands, exits, outcomes and limits in the author's `stage_receipt`; bind the exact artifact paths and hashes. Submit failed attempts honestly for REWORK and correct them before QA advancement. For code, use TDD where useful, review the diff and debug observed failures before retrying. A document or source label is not a test result.
3. An independent reviewer opens the canonical sources themselves, verifies the submitted revision and records their own checks and `stage_receipt`. Their actor differs from the author and other required reviewers. They may reuse compatible navigation evidence after their own source check; copying the author's conclusion is not independent review.
4. REWORK returns only affected work to its owner. Preserve prior snapshots, reconcile effects and revalidate impacted dependencies. Submit a new revision and obtain fresh applicable reviews. Missing prerequisites block the affected transition; retain the three-replacement limit.
5. Present the current package only after all required PASS verdicts. Human changes return to the affected owner and renewed QA. Advance after the required explicit human acceptance. Only previously authorized `reviewed_task` preparation permits coordinator completion of G3–G5 here.

G2 production and G3 review form one Discovery stage: `handoff` transfers the exact G2 package to G3 without claiming approval or duplicate QA. G3 coverage PASS and its existing source-consultation record precede architecture. G6 retains its separate spec/task/Discovery consultation.

At G7, current-phase checklist checkpoints and independent MT receipts complement phase QA; they never replace it. The microplan stays inside execution, not the Task. Keep incidental item self-checks local; do not launch a reviewer model for every trivial item.

G9 requires independent operational/security PASS and human authorization for the exact candidate, target and deployment attempt. G10 records deployment and post-deploy checks, receives independent QA, then permits coordinator `complete` without another human acceptance. A new attempt returns to G9 for renewed authorization. Neither this protocol nor merge approval grants deploy permission; merge remains separately authorized.

The evaluator checks local hashes, declared identities, ordering and evidence structure. It cannot authenticate a person, prove a model read a source, certify source truth or establish application behavior without executed evidence. Label mocked, inaccessible and untested claims honestly. The tool-free Translator does not run this loop.
