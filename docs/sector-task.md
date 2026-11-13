> Contexto TFD · 883 palavras · 1262 tokens (o200k_base)

# Sector task

Author one canonical `task.json` per module in the project. Follow the [TFD task schema](../schemas/task.json) and use the [generic example](../examples/task.example.json) as a structural reference. Use imported execution-contract guidance as reference material. The library's v2 format applies to its own [workflow](../library/docs/workflow-pipeline.md).

From the TFD root, validate the project task with `python -B scripts/validate_task.py <task.json>`, then generate its sibling Markdown view with `python -B scripts/render_task.py <task.json>`.

## Human review

Generate the complete, collapsible review when handing the task to a human. Save it alongside the project's review evidence and use its Markdown as the body of the authorized linked Issue. If the body exceeds GitHub's limit, use a short summary and link to the complete review in an authorized location. The canonical `task.md` is the artifact bound to G6. Keep its original command and filename.

```powershell
python -B <tfd-root>/scripts/render_task_review.py <task.json> <task-review.md>
python -B <tfd-root>/scripts/render_task_review.py <task.json> <task-review.html>
```

Pass `--workflow <workflow.json> --project-root <project>` to include evidence and checkpoints verified against the submitted revision. Open the local HTML and use **Copiar Markdown** to copy the complete review. GitHub renders the Markdown's checklists, collapsible sections and Mermaid diagram. Record the human decision for the specific revision in the linked Issue and project ledger. The preview checkboxes are review notes.

Use the [generic review example](../examples/task-review.example.md) to see how task, phase, sector and microtask titles supply the headings. Include measurable acceptance criteria tied to each affected microtask and its verification. Shared criteria are appropriate when they establish the same observable result across multiple microtasks. Give each microtask its actual deliverables and specific completion condition.

Use `business_rules` for domain behavior and `references` for the technical artifacts the reviewer needs. Link only the applicable IDs from each microtask. A backend reference can point to an API contract, permissions, data invariants or error cases. A frontend reference can point to journeys, UI states, accessibility checks or a prototype. Record the version or location of the applicable artifacts in the project. Keep broader research in Discovery and consult the engineering library on demand. [Requirements traceability](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052%2B-%2BBidirectional%2BTraceability%2BBetween%2BHigher%2BLevel%2BRequirements%2Band%2BSoftware)

## Sector routing

Declare ordered phases and the sector matrix. Use REQUIRED with assigned microtasks or N/A with a reason. Each microtask identifies its phase, sector, owner, independent validator, mandatory reference IDs, writable paths, dependencies, checklist and expected output. The canonical Markdown view derives each MT's literal `@owner` and `@validator`, permitted checklist and writable paths, prohibited out-of-scope edits/gate bypass, deliverables and completion condition from these existing fields. Show global exclusions/protected paths once and link them from each MT. The main agent uses the TFD-harness skill to coordinate and delegate after dependencies and gates; the native Codex status agent does not delegate. Show this coordinator at the top and the harness sector first without changing execution dependencies. Mentions identify responsibility; they do not invoke an agent or grant permission. Keep routed execution JSON unchanged. The task view links to this JSON. From the TFD root, print the smallest applicable route with `python -B scripts/render_task.py <task.json> --sector <id> --microtask <MT-id>`. Add `--measure` to count the routed JSON before reading it. Omit `--microtask` for the entire sector. Check source size separately before loading the routed references and preserve all mandatory requirements.

Dispatch independent microtasks only after their dependencies and approval gates pass. For parallel work, confirm available host slots, approved contracts and disjoint writable paths. QA may prepare tests alongside implementation. Its integrated verdict requires the delivered revision, independent reviewers and evidence. Rework the existing microtask and retest its affected checks.

Keep the full active skill, routed global constraints and every applicable mandatory reference; retrieval ranking cannot remove them. Consult supplemental theory only for the affected decision. Save concise, versioned research and local decisions in existing project records, then hand off their paths instead of repeated source dumps. Missing material context can reopen Discovery from any sector. Resolve technical facts within authorized research; missing business decisions or scope changes return to the user.

The [reviewed preparation contract](../skills/TFD-harness/references/gates.md) permits explicitly authorized coordinator completion of G2-G5. Present the canonical task, matching spec/Discovery and independent spec QA PASS at human G6 approval. Each G7 phase still completes self-test, applicable independent QA, scoped rework and human approval. This does not authorize publication, merge or deploy.

Keep mutable evidence in the module's existing workflow ledger. Set `task_id` and `contract_revision` for the displayed receipts. Add `sector_receipts` keyed by sector. Each entry may carry `summary`, `blockers`, observed `total_tokens` and the `token_receipt` path. Its `reviews` object is keyed by microtask ID. A review includes `role` matching the validator, distinct `reviewer` and `executor` identities, `verdict` (`PASS`, `REWORK` or `BLOCKED`), `observation` and `evidence`. Record sanitized token receipts per run and aggregate only runs attributed to that sector. Keep unavailable totals empty.

Use `python -B scripts/render_task.py <task.json> --workflow <workflow.json>` to display observed checkboxes and sector totals without creating another task or changing the submitted contract view. The ledger's gate events remain the source of gate decisions. A receipt without a current independent verdict leaves both boxes open.
