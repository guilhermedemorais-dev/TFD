# Library source handoff

Select only an edition/item usable for the approved project without buying a
license; exclude paid Pro/Enterprise assets. Unknown cost/license is not eligible
until verified. Zero license cost and OSI open-source status are distinct: retain
applicable source-available/copy/redistribution restrictions and subtree terms.
No catalog proves every repository item free or all infrastructure/services free.


This is provenance in existing project artifacts, not a new runtime/schema/gate.
Resolve project-native components first, curated matching-stack sources second,
then targeted Context7 or official GitHub research when a concrete gap remains.
Catalog presence does not approve adoption or install packages. Libraries never
become standalone Harness skills by being listed here.

For each relevant library/component, keep one stable **library ID** and one stable
project **source ID** in COMPONENT_SOURCE_INVENTORY, PRD, frontend/component spec
and Human Task. Reuse existing project reference IDs instead of renumbering at
handoff. Record only applicable sources; do not fill a record for every catalog item.

| Field | Evidence to retain |
| --- | --- |
| Library ID / source ID | Stable catalog identity plus the project's existing reference ID |
| Official repository / docs URL | Exact official origin and consulted page/source |
| Version / commit | Observed package version or pinned source commit; UNKNOWN until verified |
| Component path / variant | Exact item/subtree and JS/TS, CSS/Tailwind or equivalent variant |
| Purpose / module | Product need and consuming module or microtask |
| License | Exact item/subtree terms and notices, not a repository-wide guess |
| Dependencies | Required packages/versions and project/runtime compatibility; UNKNOWN if unverified |
| Adaptations | Project tokens, API boundaries, accessibility, motion and behavior changes |
| Decision state | Existing PROPOSED / APPROVED / UNKNOWN / EXCLUDED with rationale |

PRD can retain a PROPOSED library with UNKNOWN pin/variant. SDD resolves the material
decision for its module before making it an executable dependency. Preserve the
same source ID in existing JSON `references[].id`; route its project file/section
and purpose through sector/microtask `required_sources` only when the dependency
is selected and necessary. Nonselected candidates are not REQUIRED sources.
Do not add library-specific schema fields or copy the global catalog into JSON.

Keep verified records in the client's existing reference/design library. Exact
source knowledge follows the module; unrelated tasks need not reload it. Versions,
licenses and dependencies must be revisited on relevant drift. Install selected
packages only in the chosen project under its approved package manager/lockfile.
Markdown instructions remain OS-neutral. Tool execution has separate runtime/OS
checks, and no catalog statement certifies macOS/Windows/Linux runtime behavior.
