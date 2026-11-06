# Anti-AI Design

Use this file when visual quality, perceived product value, or differentiation
matters. The goal is not to make the interface unusual. The goal is to avoid
lazy, repetitive composition that looks generated instead of designed.

## Start from product character

Before styling, identify:

- audience and buying/usage context
- product category and task density
- desired perception: trustworthy, premium, technical, calm, playful, fast,
  editorial, utilitarian, etc.
- brand constraints and existing visual language
- content priority and primary action

Do not invent a visual personality that conflicts with the product.

## Common generic-AI failure modes

Avoid using these as automatic defaults:

- dark navy background + purple/blue gradient glow
- giant centered headline followed by three identical glass cards
- excessive rounded rectangles for every content group
- pill badges above every heading
- gradient text without semantic or brand reason
- identical 3-column feature grids repeated down the page
- bento grids inserted regardless of content structure
- floating blobs, dot grids, aurora effects, and particles added merely to fill
  empty space
- dashboards made mostly of stat cards instead of the real workflow
- meaningless charts and fake metrics used as decoration
- every control receiving large radius, shadow, border, and hover animation
- excessive microcopy such as `AI-powered`, `smart`, `next-generation`, or
  `seamless` where the interface should demonstrate the value instead

These patterns are not forbidden. They require a reason tied to brand, content,
or interaction.

## Composition rules

- Build hierarchy from the user's task and content, not from component demos.
- Vary section rhythm based on information density instead of repeating the same
  container pattern.
- Use whitespace deliberately. Dense operational software may need less than a
  marketing site.
- Prefer a few strong visual decisions over many decorative effects.
- Let typography, proportions, imagery, content hierarchy, and interaction
  quality carry more identity than gradients and shadows.
- Use asymmetric composition only when it improves emphasis or brand character.
- Preserve familiar interaction patterns for high-frequency product actions.
- Use motion to explain change, continuity, hierarchy, or feedback, not to prove
  that Motion is installed.

## Product UI

For SaaS, ERP, CRM, admin, dashboards, and operational software:

- design around tasks, entities, decisions, and state transitions
- show the most important action near the information that drives it
- prefer tables, lists, filters, timelines, command surfaces, and detail panels
  when they match the workflow
- reduce dashboard-card proliferation
- distinguish read, edit, destructive, approval, and exceptional states clearly
- use progressive disclosure for secondary controls
- optimize scanability and keyboard/mouse efficiency where users work for long
  sessions

## Marketing UI

For landing pages, institutional sites, product launches, and campaigns:

- derive section order from the decision journey, not a template's section list
- use real proof, product visuals, examples, constraints, and outcomes instead of
  decorative filler
- make hero composition specific to the offer and audience
- avoid generic icon-card sections when a diagram, product screenshot, timeline,
  comparison, case study, or demonstration communicates better
- repeat a visual motif only when it creates recognizable brand continuity

## E-commerce

- prioritize product understanding, trust, price, variants, delivery, returns,
  availability, and checkout clarity
- use lifestyle or editorial visuals only when they improve product perception
- do not hide commerce-critical information behind fashionable interaction
- keep mobile purchasing paths short and obvious

## Differentiation check

Before approving a screen, ask:

1. If the logo and brand color disappeared, would the information architecture
   still feel specific to this product?
2. Does the screen expose real domain concepts, or could the same layout sell a
   CRM, crypto dashboard, AI tool, and restaurant app by changing the copy?
3. Are decorative choices doing work, or merely occupying pixels?
4. Is the primary workflow visually obvious within a few seconds?
5. Did external components get normalized into one coherent product language?

If the result is interchangeable with a generic template, revise composition,
content hierarchy, and domain-specific patterns before adding more decoration.
