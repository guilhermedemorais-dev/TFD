---
name: TFD-qa_spec
description: "Review pre-implementation artifacts at G3/G6. Verify sources, report actionable findings, and issue PASS or REWORK. Recheck corrections independently."
metadata:
  version: "1.5.0"
  owner: "qa_spec"
---

# Specification QA

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources. Verify decisions and test obligations, not rote adoption of patterns or every manual topic.

## Activate
- "revisar a spec antes de implementar"
- "revisar o PRD e o discovery antes do código"
- Review another sector's artifact. G3 reviews PRD and Discovery. G6 reviews the phase spec and matching Discovery revision together.

## Route elsewhere
- "implementar endpoint de pedido" → `backend`.
- Review implemented behavior → `qa_backend` or `qa_ui`.
- Write or fix the PRD, research, spec, or contract → its author.

## Review
1. Identify the artifact and exact revision. Read it fully and verify claims against cited sources. Flag unsourced requirements as gaps.
2. Apply the eight [review dimensions](references/review-checklist.md) in order. Use the higher severity when uncertain and explain why. Quote exact evidence or ask the author a question.
3. Write `findings.json` with exactly `artifact` (POSIX path), `revision` (revision, commit, or hash), `verdict`, and `findings`. Each open finding has a unique `F-NN` ID, `severity`, checklist `dimension`, literal `evidence`, and actionable `recommendation`. Use `REWORK` for any `blocker` or `major`, otherwise `PASS`. Keep closure notes and limitations outside this JSON.
4. For `REWORK`, direct the author to correct research, spec, or both. Recheck the updated revision or matching pair. Reuse IDs for persistent or reopened issues. Before task approval, verify the canonical Task points to the submitted spec and the generated view matches it. In reviewed preparation, G6 PASS findings must name that spec and the submission revision. Forward the task for human approval only after QA `PASS`.
5. Run `python skills/TFD-qa_spec/scripts/check_findings.py findings.json`. Exit 0 means structurally valid, 1 invalid, and 2 incorrect usage. Verify the substance yourself.

Review independently. Leave implementation and artifact edits to their authors.
