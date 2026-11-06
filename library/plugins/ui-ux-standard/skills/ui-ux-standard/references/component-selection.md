# Component Selection

Use this file when several component libraries, templates, blocks, or patterns
could satisfy the same UI requirement.

## Decision process

Evaluate each candidate against the actual product task, not against demo-page
visual appeal.

Score qualitatively on:

- workflow fit
- consistency with the existing design system
- accessibility quality
- responsive behavior
- interaction/state completeness
- dependency cost
- implementation/adaptation effort
- maintainability
- performance implications
- visual differentiation appropriate to the product
- licensing certainty

Do not create a numeric score unless the project explicitly requires one. A
short comparison with rationale is usually better than fake precision.

## Foundation versus accent components

Prefer a stable base for recurring product primitives:

- buttons
- inputs
- select/combobox
- dialogs
- menus
- tables
- tabs
- forms
- navigation
- feedback states

Use specialist libraries selectively for components where they materially add
value:

- hero sections
- interactive product demos
- animated backgrounds
- high-impact feature sections
- specialized visualizations
- rich empty/onboarding states

Do not import a second design language merely because one component looks
impressive in isolation.

## Template policy

Templates are reference accelerators, not project architecture.

Before using a template:

1. Identify the parts that solve the current information architecture or
   conversion problem.
2. Strip demo-only sections, fake metrics, placeholder copy, and decorative
   clutter.
3. Map typography, colors, spacing, radius, elevation, and motion to project
   tokens.
4. Replace generic information hierarchy with the product's real workflow.
5. Verify mobile behavior instead of inheriting the template blindly.
6. Rebuild or reject sections whose DOM, accessibility, performance, or
   dependency cost is poor.

## Avoid library soup

As a default, use:

- one primitive/component foundation
- the project's own design tokens
- zero to two specialist sources for exceptional patterns

Exceed this only when there is a documented reason and a normalization strategy.

## Custom-build gate

Build from scratch when at least one applies:

- no candidate fits the workflow without substantial distortion
- adaptation would cost more than a focused custom implementation
- available candidates conflict with accessibility or performance requirements
- licensing is unclear or incompatible
- the project already has primitives that make a custom composition simpler
- the component is a core product differentiator whose behavior is specific to
  the domain

Record the reason in `COMPONENT_SOURCE_INVENTORY`.

## Handoff example

```text
COMPONENT_SOURCE_INVENTORY
- project-native candidates: Button, Dialog, DataTable
- external candidates searched: Origin UI data-table patterns; shadcn blocks
- selected source/component: project DataTable + adapted Origin row-action pattern
- why selected: preserves product primitives while improving row actions
- adaptation required: spacing, action menu, mobile overflow, permission state
- license/dependency status: no new runtime dependency; source terms verified
- rejected alternatives: animated table pattern added unnecessary motion
- custom-build justification: NA
```
