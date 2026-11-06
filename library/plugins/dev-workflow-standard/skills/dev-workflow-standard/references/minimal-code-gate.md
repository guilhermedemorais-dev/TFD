# Minimal Code Gate

Apply before specs, before implementation, and during final review. The goal is
the smallest complete change that satisfies current approved requirements.

`REUSE_INVENTORY` and `MINIMAL_CODE_GATE` are local evidence conventions built
on established reuse and minimal-change principles.

## Reuse Inventory

Before creating code, search by responsibility, domain term, symbol, route,
interface, schema, call site and behavior. Inspect sibling modules and shared
controls, not only the target file.

```text
REUSE_INVENTORY
- searched_paths:
- queries_and_symbols:
- existing_candidates:
- call_sites_checked:
- decision: REUSE | EXTEND | REPLACE | CREATE
- reason:
```

## Decision Order

Prefer, in order:

1. reuse an existing implementation
2. extend the existing owner of the responsibility
3. replace and migrate a defective duplicate
4. create new code only when no suitable owner exists

Do not create wrappers, services, repositories, helpers, hooks, components,
configuration layers or generic abstractions for hypothetical future use.

## New-Code Test

Every new unit must answer:

- What approved requirement needs it now?
- Which existing implementations were inspected?
- Why can none be reused or extended safely?
- Who owns this responsibility after the change?
- Which duplicate or obsolete path is removed or deliberately retained?
- What test proves the behavior without coupling to implementation detail?

New abstractions require at least two current concrete consumers or an explicit
approved architecture decision. Similar behavior with different names is still
duplication.

## Scoped cleanup and complete simplification

Apply cleanup to the approved change and its affected consumers, not as an
unsolicited repository-wide rewrite. Preserve the full approved scope, existing
architecture, interfaces and conventions; simplicity never authorizes an
automatic MVP, omitted requirement or architecture change.

- Inspect candidate dead code, unused options/configuration, obsolete paths and
  dispensable dependencies. Before deletion, check callers, public exports,
  manifests, configuration, fixtures, tests, generated entrypoints and dynamic
  or string-based references where applicable. Absence of text-search hits alone
  is not proof of non-use. Record evidence and remove, retain with reason, or escalate
  uncertainty; public consumers and unresolved references cannot be guessed away.
- After the existing Decision Order, satisfy any remaining need with the
  standard library or platform first, then a compatible installed dependency,
  then the minimum necessary new code. Preserve suitable project-native owners.
  Do not add a dependency for a trivial helper; justify unavoidable additions
  against the approved requirement and existing alternatives.
- Trace shared causes before bug fixes and correct the responsible owner once.
  Complete every affected caller, fixture, test, configuration and export needed
  by the change, including paths outside the diff. Required edits outside the
  allowed scope return to Harness for contract expansion before editing.
- Merge equivalent implementations when safe and simplify unnecessary branches,
  conversions, wrappers and boilerplate. Split unrelated responsibilities only
  when it improves understanding or testing. Optimize for readable, complete
  behavior, not line counts, code golf or helpers created merely to shorten files.
- Moving, merging or deleting code must preserve boundary validation, error
  handling, security, accessibility, calibration and protection against data
  loss. Check correctness at relevant edge cases and expected load; performance
  findings need an actual affected path, not hypothetical optimization.
- Validate changed behavior with meaningful, risk-appropriate checks, including
  callers and regression cases. Nontrivial logic or bug fixes need a check that
  would detect the failure, not a test mirroring implementation details. Trivial
  documentation-only changes do not need invented behavioral tests; run required
  repository checks and state the bounded validation scope.
- Record intentional limits, their consequences and the condition for revisiting
  them in the existing Task/evidence ledger, with a nearby code comment when
  useful. Do not create a competing debt ledger or waive required behavior.

## Additive evidence and review

Append these fields to the existing `MINIMAL_CODE_GATE`; preserve every original
field. Before implementation, record candidate decisions and planned validation;
final PASS requires executed evidence. Use explicit N/A with a reason for an
inapplicable field, never an unexplained blank.

```text
- cleanup_candidates_and_decisions:
- removal_reference_evidence:
- platform_and_dependency_choices:
- shared_root_and_affected_consumers:
- preserved_behavior_and_validation:
- intentional_limits_and_revisit_conditions:
- not_checked_and_remaining_risks:
```

Review the connected flow, not just changed lines. Findings must identify a
concrete case, affected path and smallest complete correction. Prioritize
correctness, data/security risks, expected-load failures, missing meaningful
tests, measured slowdowns and unnecessary complexity, in that order. Functional
QA verifies its routed scope; Security, UI/UX and other required owners retain
their approvals. This gate does not replace those owners or human acceptance.

Final `PASS` is also forbidden when a material deletion lacks reference evidence,
affected consumers remain incomplete, safeguards or approved requirements were
removed, or required validation was not executed. Report uncertainty and request
REWORK or BLOCKED as appropriate; justified N/A is not a validation waiver.

## Inspiration and limits

This additive upgrade adapts principles from Dietrich Gebert's MIT-licensed
[Ponytail core](https://github.com/DietrichGebert/ponytail/blob/2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5/skills/ponytail/SKILL.md)
and [Ponytail Review](https://github.com/DietrichGebert/ponytail/blob/2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5/skills/ponytail-review/SKILL.md),
verified at commit `2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5`.
It documents current inspiration, not verified historical derivation. No
third-party hooks, session modes, tools or dependencies are installed or activated.

```text
MINIMAL_CODE_GATE
- result: PASS | REWORK | BLOCKED
- reused_or_extended:
- new_units_and_justification:
- duplicates_removed:
- retained_overlap_and_owner:
- evidence:
```

`PASS` is forbidden when the reuse inventory is missing, a new abstraction is
speculative, or equivalent behavior was duplicated without an approved reason.
