---
name: TFD-qa_spec
description: "Independently review PRDs, Discovery, architecture, plans, phase specs and documentation. Verify sources and revision bindings, report actionable findings, and issue PASS or REWORK. Route runtime behavior to backend or UI QA."
metadata:
  version: "1.8.0"
  owner: "qa_spec"
---

# Specification QA

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md) as an independent reviewer. Consult canonical sources yourself and record the current artifacts and executed checks; the author's receipt cannot substitute for your review.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources. Verify decisions and test obligations, not rote adoption of patterns or every manual topic.

## Activate
- "revisar a spec antes de implementar"
- "revisar o PRD e o discovery antes do código"
- "revisar a documentação antes do aceite humano"
- "revisar o plano de fases e suas estimativas"
- Review another sector's artifact. G3 reviews PRD and Discovery. G6 reviews the phase spec and matching Discovery revision together.
- In stage-loop workflows, review G0 constitution, G1 PRD, G4 architecture, G5 plans, G8-review packet consistency and G8 documentation. Check documented behavior against accepted evidence; runtime/access checks belong to backend or UI QA. Do not demand future implementation artifacts from a PRD.

## Route elsewhere
- "implementar endpoint de pedido" → `backend`.
- Review implemented behavior → `qa_backend` or `qa_ui`.
- Write or fix the PRD, research, spec, or contract → its author.

## Review
1. Identify the artifact and exact revision. Read it fully and verify claims against cited sources. Flag unsourced requirements as gaps.
2. Apply the eight [review dimensions](references/review-checklist.md) in order. Use the higher severity when uncertain and explain why. Quote exact evidence or ask the author a question.
   At G3, use the [coverage handoff](../../docs/discovery-coverage.md) to compare every approved requirement, rule and flow against the coverage matrix and actual evidence. Challenge missing areas, unsupported N/A and deferred authorization or business decisions. A structural check cannot issue semantic PASS. At G6, check task coverage, spec and evidence for the same reviewed Discovery.
   Independently open the applicable engineering-guide chapters and original official sources for decisive technical claims; the author's summary is not your verification. Record the actual sections, conclusions and limits. Use the [independent review contract](references/independent-review.md) for G3/G6 in workflows with `review_version: 1`. Reuse still-applicable source records by reference after your own check, without loading the whole guide. Never author the missing research or invent consultation evidence to obtain PASS.
3. Write `findings.json` with exactly `artifact` (POSIX path), `revision` (revision, commit, or hash), `verdict`, and `findings`. Each open finding has a unique `F-NN` ID, `severity`, checklist `dimension`, literal `evidence`, and actionable `recommendation`. Use `REWORK` for any `blocker` or `major`, otherwise `PASS`. Keep closure notes and limitations outside this JSON.
4. For `REWORK`, direct the author to correct research, spec, or both. Recheck the updated revision or matching pair. Reuse IDs for persistent or reopened issues. Before task approval, verify the canonical Task points to the submitted spec and the generated view matches it. In reviewed preparation, G6 PASS findings must name that spec and the submission revision. Forward the task for human approval only after QA `PASS`.
5. Run `python skills/TFD-qa_spec/scripts/check_findings.py findings.json`. Exit 0 means structurally valid, 1 invalid, and 2 incorrect usage. Verify the substance yourself.

Review independently. Leave implementation and artifact edits to their authors.
