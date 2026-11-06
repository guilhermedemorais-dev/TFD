# Live design guide, owned by the client project

Use during frontend module specification, component changes and visual review.
The plugin supplies a reusable starter, not a client-specific design system.

## Establish, then extend

1. Inspect existing design docs and real components. Reuse an equivalent
   catalogue (including a generated component explorer) and record its entry
   URL/path and build command instead of creating a competing library.
2. Before closing UI specs, agree visual direction, approved references,
   density, typography, layout, spacing and tokens with the user. Ambiguous
   phrases such as "not app-like" need a reference or a decision, not guessing.
3. Maintain `docs/design/design-guide.md`, `docs/design/index.html`,
   `docs/design/design-tokens.json` and `component-source-inventory.md` in the
   **client project**, never its installed plugin directory. Evidence belongs
   in `docs/design/references/` and `docs/design/visual-qa/` as needed.
4. During each module's SDD, add only missing components, variants and states to
   that same catalogue. Prefer demonstrations importing the actual project
   components. One HTML entry may use separate source/assets or a build; it
   does not require a giant single file or a new framework/service.
5. Validate the rendered catalogue and obtain the relevant visual approval
   before frontend implementation. A pending catalogue/approval blocks that
   frontend handoff, not unrelated approved backend work. Catalogue approval
   does not replace final rendered application validation.

`assets/live-design-guide/index.html` (relative to the skill directory) is an
optional dependency-free starter. Copy/adapt only when there is no suitable
catalogue. Its SAMPLE-STATUS component is a fixture example, not approved
project UI. Replace it with relevant project components, not a copied generic
visual identity. Its static semantic tests are not browser evidence.

## Component contract

Use stable component IDs and a revision, with an HTML anchor for each. The
guide/inventory records name, purpose, consuming modules, source path/URL and
source revision, tokens, dimensions/spacing, variants, responsive rules,
example content, inputs/outputs/events, mouse and keyboard behavior, focus and
semantics, usage limits, acceptance criteria and approval/validation status.

Demonstrate applicable default, hover, focus, active, disabled, loading, empty,
error and success states; also permissions, selection and destructive
confirmation when relevant. Justify N/A states. Complex widgets need
deterministic fixtures and testable interactions, with no purchases, external
messages or writes. Label mocks, unavailable integrations and untested states.
A screenshot is not an interactive widget; a frontend fixture is not backend
implementation or an end-to-end PASS.

Use the project's approved component sources before custom UI. Record reuse,
adaptation, license/dependency checks and rejected alternatives in the source
inventory. Research functional sources in `docs/biblioteca-referencias/`;
inspect relevant implementation, examples and tests rather than README alone.
For authorized web references, combine DOM/computed CSS, measurements, states,
interactions and viewports. Scraping or one screenshot cannot prove complete
coverage, inaccessible flows or server behavior. Preserve coverage limitations.

## Handoff and revision discipline

SDD references the exact guide section, catalogue anchor, component ID/revision,
tokens and source inventory in the existing Task design/references fields and
the equivalent JSON. Do not create a second task template or JSON per widget.
Keep normative instructions in those existing fields; mutable approval and
validation evidence stays in receipts/Issue comments.

Implementation consumes those sources, reuses approved components and updates
the same catalogue/guide when authorized behavior changes. If code, tokens,
guide or catalogue conflict, return to Harness for resolution and updated
card/JSON revision. Reuse earlier evidence only after checking applicability
to the current component/source revision.

UI/UX owns fidelity, layout, responsive behavior, keyboard/focus, accessibility
and visual states. QA owns functional transitions, forms and real integrations.
Report each viewport, state/interaction exercised, revision, actual environment,
commands and artifacts. A parse/build check does not prove browser rendering.
Untested checks remain `NAO VALIDADO`; no screenshot or approval closes another
owner's gate. Include changed paths, limitations and measured tokens or
`NOT_AVAILABLE` in the existing material execution report.
