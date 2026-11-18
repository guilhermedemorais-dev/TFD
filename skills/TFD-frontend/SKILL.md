---
name: TFD-frontend
description: "Implement approved UI flows and states, with accessibility and self-tests."
metadata:
  version: "1.2.0"
  owner: "frontend"
---

# frontend

When `stage_loop_version: 1`, apply the [stage loop](../TFD-harness/references/stage-loop.md) to production and scoped rework. Record your source consultation and self-tests; independent UI QA reviews the current revision before human acceptance.

Keep components cohesive and state ownership explicit; prefer composition and existing design tokens. Diagnose measured rendering/network costs before optimization. Verify accessibility and user-visible regressions rather than implementation details.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

Use approved components, tokens and API contracts. Cover success, loading, empty, error and denied states as applicable. Verify keyboard, focus, labels and relevant viewports. Exercise the real local flow or label mocks explicitly. Run targeted tests and record revision, commands, exits and limitations. Hand off to UI QA. Route contract or design gaps back to the owner.
