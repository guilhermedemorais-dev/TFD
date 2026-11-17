# Discovery coverage before G3

Discovery authors `coverage.json` alongside sources, evidence and findings before
G3. Use the approved PRD's stable IDs; keep the inventory complete. Reuse applicable
project answers. Resolve technical facts autonomously with bounded source research;
route only missing material business decisions to Product.

The JSON object has `version: 1`, `requirement_ids` (REQ- IDs),
`business_rule_ids` (RULE- IDs), `areas` and `flows`. IDs are nonempty strings with
the indicated prefix and an alphanumeric suffix; IDs within a list and flow IDs
must be unique. A requirement or rule may participate in several flows.

`areas` contains exactly `business`, `ui_ux`, `frontend`, `backend`, `data`,
`security`, `quality` and `operations`. Every area records:

- `status`: `COVERED`, `N/A` or `UNKNOWN`;
- `summary`: a nonempty, project-specific explanation;
- `evidence_ids`: IDs present in `evidence.json`;
- `reason`: required and nonempty for `N/A` and `UNKNOWN`.

`COVERED` needs at least one real `OBSERVED` or `INFERRED` finding, with a locator
and a verified source. Every referenced finding must meet this condition. `N/A`
must explain non-applicability and have an empty evidence list. `UNKNOWN` blocks
the gate even when the record is structurally valid. If business rules exist,
`business` must be `COVERED`.

Each flow records `id` (FLOW- ID), a nonempty `summary`, `requirement_ids`,
`business_rule_ids` and `evidence_ids`. Its requirement/rule references must belong
to the top-level inventory, and its evidence must be verified and non-UNKNOWN.
Every inventoried requirement and business rule needs a flow with actual evidence.
An isolated UI observation cannot fill missing areas or unevidenced flows.

In coverage mode, a finding with `class: UNKNOWN` and `essential: false` also
requires nonempty `rationale` and `affected_decision`. These fields explain why the
gap is nonessential; a boolean alone cannot certify unanswered privacy,
authentication or material business contracts. Independent QA checks semantics,
source applicability and whether the inventory omits approved PRD items. A source
label, duplicated UI observation or checker exit 0 does not prove those contracts.

Run:

```text
python <skill-dir>/scripts/check_evidence.py sources.json evidence.json --coverage coverage.json --require-coverage
```

Exit codes: `0` structurally valid, `1` invalid or required coverage missing,
`2` a recorded essential gap or UNKNOWN area blocks progress. Errors take priority
over blocks. Neither exit 0 nor generated findings grant QA PASS or human approval.
The original two positional arguments remain valid for legacy callers; supplying
`--coverage` enables coverage validation, while `--require-coverage` rejects its
absence. Python callers may use `validate(sources, evidence, coverage=None)` or
`validate_coverage(coverage, sources, evidence)`, both returning `(errors, blocked)`.
