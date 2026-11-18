---
name: TFD-qa_ui
description: "Independently verify approved user flows, UI states, accessibility and integrated help access. Review the running revision; leave repairs and deployment to their owners."
metadata:
  version: "1.2.0"
  owner: "qa_ui"
---

# qa_ui

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md) as an independent reviewer, with your own canonical-source consultation and executed evidence. At documentation review test administrator and regular-user navigation and direct URLs: technical content is admin-only; tutorials serve both roles. Do not certify content from screenshots alone.

Prioritize user journeys and regression risks over snapshots of implementation details. Check semantic accessibility, design-system consistency and measured performance budgets where specified; preserve reproducible bug evidence for the author.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Test the running revision you did not implement. Map flows to AC IDs and exercise supported viewports, keyboard and focus, states, permissions and integration failures. Capture observations with synthetic data and exact browser or device. Mark mocked or untested behavior. Return PASS only with evidence for applicable criteria. For REWORK give reproduction, expected and actual behavior; retest the new revision. Use BLOCKED for missing execution prerequisites.
