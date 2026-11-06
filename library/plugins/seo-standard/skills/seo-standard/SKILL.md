---
name: seo-standard
description: "Use for websites, landing pages, service pages and small ecommerce when the goal is better technical SEO, AEO/GEO readiness, schema, search-intent alignment, conversion copy and post-change verification."
---

# SEO Standard

Own SEO/AEO/GEO and conversion-readiness analysis inside the Engineering Harness.

Read [site-delivery.md](references/site-delivery.md) for website delivery work.
Read [beyondseo-integration.md](references/beyondseo-integration.md) when using
the BeyondSEO runtime. Load only the relevant vendored BeyondSEO playbooks for
technical SEO, on-page, schema, AEO/GEO, search intent or conversion copy.
Consult
[tool-registry.json](references/tool-registry.json) for runtime ownership.

## Preconditions

1. Identify the target website/page, business goal and intended conversion.
2. Confirm authorized crawl/edit scope.
3. Load this SKILL and emit the normal SKILL_RECEIPT.
4. Distinguish public evidence from business facts supplied by the user.
5. Never promise rankings or fabricate traffic/search-volume evidence.

## Workflow

1. Inspect the site/project and current business intent.
2. Run the bounded BeyondSEO audit needed for the Task.
3. Classify findings by evidence, impact and priority.
4. Cover technical SEO, AEO/GEO, schema, intent/content and conversion copy when applicable.
5. Produce exact recommended changes, affected URLs/files and acceptance checks.
6. Route implementation to dev-implementation-standard.
7. Re-run fresh validation after changes.
8. Return EXECUTION_RECEIPT with before/after evidence and unresolved limitations.

## Commercial site standard

For landing pages and sites sold to clients, treat these as default concerns:

- indexability and crawlability;
- metadata and canonical correctness;
- headings and semantic structure;
- schema;
- mobile/performance evidence;
- search-intent alignment;
- AEO/GEO answer-friendly structure;
- persuasive but factual copy;
- clear CTA and objection handling;
- revalidation before delivery.

Backlinks, reputation, competitor research and editorial planning are available
but should not be forced into every small site.

## Ownership boundaries

- sdd-spec-factory turns validated findings into specs/Task requirements.
- dev-implementation-standard owns code changes.
- ui-ux-standard owns visual hierarchy/accessibility.
- qa-testing-standard owns functional behavior.
- security-standard owns AppSec.
- dev-workflow-standard owns routing and final gate reconciliation.

SEO Standard may write proposed copy/content, metadata and structured-data
requirements, but does not self-approve product implementation.
