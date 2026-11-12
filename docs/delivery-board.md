> Contexto TFD · 801 palavras · 1180 tokens (o200k_base)

# Phase-based delivery board

Apply this profile when the project explicitly adopts it. Use the [gate contract](../skills/TFD-harness/references/gates.md) and project ledger for approvals and evidence. Keep one Task and linked Issue per module. Dispatch in Task dependency and gate order. Skip inapplicable phases and schedule Foundation, database and infrastructure prerequisites in their required development phases.

## Status options

Use this `Status` display order. Return to `Discovery / Spec` for each new phase's G6 work.

| Status | Entry and next decision |
| --- | --- |
| `Backlog (PRD)` | Capture the demand. Record constitution, environment, briefing and PRD decisions at G0, G0.5 and G1. |
| `Discovery / Spec` | Start G2–G5 research, QA, architecture and planning. Prepare and independently review the G6 spec, Discovery, Task and view. |
| `Spec / Human Review` | Send the matching G6 package after independent QA PASS for explicit Task and spec approval. |
| `Frontend / Development` | Start approved frontend G7 work, self-tests and independent QA. |
| `Frontend / Human Review` | After G7 PASS, the human tests locally and accepts the reviewed frontend revision. |
| `Backend / Development` | Start approved backend G7 work, self-tests and independent QA. |
| `Backend / Human Review` | After G7 PASS, the human tests locally and accepts the reviewed backend revision. |
| `Documentation / Development` | After G7 approvals and G8-review local acceptance, write and integrate both documentation deliverables. |
| `Documentation / Human Review` | After independent documentation and access checks pass, the human approves the G8 technical docs and user help. |
| `DevOps / Preparation` | After G8 approval, prepare and independently verify the release candidate and operations. |
| `DevOps / Human Review` | After applicable independent PASS, the human checks the candidate in authorized staging against local acceptance and reviews security and rollback evidence. |
| `Deploy` | Deploy the exact candidate to the authorized target after explicit human deploy approval. Record execution and verification. |
| `Done` | Record successful deployment and post-deploy verification in the approved environment. |

Preserve human gates. Only explicit `preparation.mode=reviewed_task` authorization permits coordinator completion of G2–G5 after applicable QA. Record G8-review in the last applicable development review. Require separate explicit deploy and merge decisions for their respective operations. Keep board, QA and human approval evidence distinct.

## QA labels and rework

The coordinator reflects observed transitions on the linked Issue when authorized. Set `QA em andamento` when independent QA starts, keeping the production column. On REWORK, record findings and replace it with `Em ajustes` while the owner corrects them in the same phase. For human changes, preserve the comment and return the card to the affected production column with `Em ajustes`. Restore `QA em andamento` when QA starts on the corrected revision. Apply the gate contract's rework limit.

Keep `QA em andamento` until all applicable independent reviewers pass the current revision. Clear QA labels on aggregate PASS before Human Review or on phase changes. Clear the QA badge when review stops or is interrupted. On BLOCKED, clear that badge, keep the status and use `blocked` with the cause. Preserve unrelated labels. Record revision, findings, commands, results and human decisions in the same Issue and ledger.

## Documentation and release

Documentation owns versioned content and coordinates in-product integration with implementation owners. Restrict the technical section and its resources to administrators. Expose tutorials to administrators and regular users. Test both roles through navigation and direct URLs, including denial of technical content to regular users. Verify accepted behavior and remove sensitive content before submission.

DevOps pins the candidate containing the accepted implementation and documentation. Compare behavior with local acceptance in authorized staging. Record reproducible configuration, artifact identity, security checks, resolution of blocking findings, rollback readiness and verification commands. After authorized deployment, record target smoke checks before `Done`. Keep failures in `Deploy` with the blocker and follow approved recovery.

## Configure an adopted GitHub Project

For the adopted board, this profile's Status options and `Done` rule replace the eight default states in the [GitHub governance procedure](../library/plugins/devops-standard/skills/devops-standard/references/github-governance.md). Follow its other safeguards. Discover read-only, propose in-place renames by ID and add missing options after authorization. Preserve IDs, card values, unrelated options, labels and settings. Reuse matching labels and add only missing ones. Verify Status grouping and enable `Labels` under View → Configuration → Fields. Check closure, merge and other automation for premature `Done`. Propose corrections, apply authorized changes and verify fields and visibility. Record required manual configuration.

Check permissions separately for each linked repository and the Project view. An authorized integration can use repository `Issues: write` to create `QA em andamento` and `Em ajustes` and apply them to Issues. If it lacks permission, a person with repository write access creates missing labels under Issues → Labels → New label. A Project editor enables `Labels` under View → Configuration → Fields if the field is hidden, then checks a linked Issue card. [API permissions](https://docs.github.com/en/rest/issues/labels#create-a-label) · [Manual label setup](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels#creating-a-label) · [Board fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-board-layout#showing-and-hiding-fields)
