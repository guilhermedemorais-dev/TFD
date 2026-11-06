# Functional test strategy

Read for planning, selecting validation or investigating run failures. Use the
task's actual acceptance criteria as the oracle; do not invent unspecified
behavior. A conflict goes back to the Harness, not into a rewritten test.

## Planning output and depth

Record short linked artifacts in the QA Task section:
`QA_GUARDRAILS`, `TEST_SCENARIOS`, `REGRESSION_TARGETS` and
`VALIDATION_REQUIREMENTS`. A scenario states preconditions, action, expected
result, test level, revision/environment needs and required evidence. Preserve
IDs for mapping planned to executed cases; never count planned cases as passed.

| Functional risk | Proportional depth |
| --- | --- |
| LOW | Focused smoke/isolated behavior; docs-only may be N/A |
| MEDIUM | Happy, negative and affected regression cases |
| HIGH | Payment/precision, tenant behavior, integrations, concurrency, jobs or state transitions: inspect failure/recovery and persistence boundaries |
| CRITICAL | Data loss, irreversible operations, production migrations or business/safety-critical processing: explicit safe environment and approval; block unsafe testing |

Depth is based on business effect, recoverability and affected scope, not copied
from security severity. Choose the cheapest level that proves the behavior:
unit for isolated logic, integration for boundaries, E2E for whole flows,
browser when actual UI runtime matters. Do not turn all tests into E2E or impose
a generic pyramid. Coverage percentages alone do not prove relevant behavior.

## Contextual categories

Select only material categories: happy/negative path; boundaries and malformed,
null or empty input; validation/permission behavior; state transitions;
retry/timeout/cancellation; concurrency/idempotency/duplicate submission;
pagination; timezone/date and decimal precision; partial failure/recovery;
large data; stale state; browser/device differences; affected regression.

For example, payment validation may require duplicate submit, timeout after
acceptance, webhook before UI response and rounding, not every category above.
Use property-based testing for meaningful invariants and safe bounded fuzzing
for parsers/inputs when justified. Specify seed/example, time/resource budget,
isolated target and stopping conditions. Never imply authorization to attack a
third party or mutate live customer data.

## Run and diagnosis

Capture command, exit code, exact revision, environment, selected cases,
observations and sanitized artifact pointers. Separate failures before rework:

| Classification | Evidence and response |
| --- | --- |
| PRODUCT_BUG | Reproduced mismatch with a valid expected behavior; use bug-report |
| TEST_BUG | Invalid assertion/fixture/oracle established; request scoped test correction, do not weaken acceptance |
| ENVIRONMENT_FAILURE | Missing service/data/config or incompatible runtime; route owner preparation and rerun |
| FLAKY_TEST | Intermittent outcome under recorded conditions; investigate isolation, ordering, concurrency, timing and shared state |
| TOOL_FAILURE | Runner/browser/tool cannot perform the intended test; repair or approved fallback, no automatic product-bug claim |

Unknown cause remains a candidate, not a confirmed product bug. For flakiness,
record initial failure and every bounded retry, seed/order and conditions; a
green retry does not erase failure. Any quarantine needs an authorized decision,
owner and follow-up, and cannot waive mandatory coverage silently. If a required
check cannot execute, QA cannot PASS. Report completed partial scope and the
BLOCKED mandatory gate rather than pretending the product passed or failed.

For bugfixes, use bug-report's initial reproduction and fixed-revision retest.
Retest adjacent failure/legitimate paths and selected regressions, not only the
single happy case. Existing test artifacts from Implementation are inputs, not
proof that independent QA executed them.

## Primary guidance and optional knowledge

- [OFFICIAL PRACTICE] [Playwright best practices](https://playwright.dev/docs/best-practices):
  test user-visible behavior with isolation, resilient locators and observable
  assertions; consult current project-compatible guidance for browser work.
- [OFFICIAL PRACTICE] [pytest flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html):
  investigate uncontrolled state, ordering and timing rather than equating every
  red test with a product bug. Sources verified 2026-09-24 for this bundle.

SWE-bench, Defects4J and BugsInPy may inform reproduction/regression reasoning
when a task needs examples. They are optional knowledge, never project evidence.
Do not download datasets into the repository or require them for ordinary QA.
No knowledge registry is introduced without a concrete operational consumer.
