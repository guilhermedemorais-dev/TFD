> Contexto TFD · 1179 palavras · 1970 tokens (o200k_base)

# Stage-loop version 1

New `pipeline.py <workflow.json> --init` workflows declare `stage_loop_version: 1`, `coverage_version: 1` and `review_version: 1`. Existing workflows without the new field retain their original protocol. Adopt the new protocol only through scoped review of the affected active work; never reinterpret earlier approval evidence.

This is a source/runtime contract, not an automatic host upgrade. Installed Codex profiles and legacy `strict_v2` or OpenBot adapters keep their existing fields and behavior until an explicitly scoped compatibility upgrade is verified. Preserve their extra data; do not add a new marker to an active legacy log merely to make an older adapter accept it.

The [sector procedure](../skills/TFD-harness/references/stage-loop.md) applies consultation, production, self-checks, independent review, scoped rework and acceptance inside every production stage. The [delivery board](delivery-board.md) remains an optional view; gates are not additional board columns.

## Gates and independent reviewers

| Gate | Production or review package | Required independent roles in version 1 |
|---|---|---|
| G0 | Constitution | `qa_spec` |
| G0.5 | Environment readiness | `qa_backend` |
| G1 | Briefing and PRD | `qa_spec` |
| G2 | Discovery production | Internal `handoff` to G3; no second QA |
| G3 | Discovery coverage review | `qa_spec` and existing G3 consultation |
| G4 | Architecture and contracts | `qa_spec` |
| G5 | Phase plan and estimates | `qa_spec` |
| G6 per phase | Spec, matching Discovery, Task and generated view | `qa_spec` and existing G6 consultation |
| G7 per phase | Implementation, self-tests, approved Task snapshot and execution receipts | Existing applicable `qa_backend`, `qa_ui`, `security` tracks |
| G8-review | Review packet and local verification | `qa_spec` for documentary consistency |
| G8 | Technical documentation and user help | `qa_spec`; also `qa_ui` when the workflow has UI phases |
| G9 | Release candidate and preparation | `qa_backend` and `security` |
| G10 | Deployment and post-deploy verification | `qa_backend`, `security`; also `qa_ui` when the workflow has UI phases |

Reviewers verify their actual domain: documentary QA compares content with accepted behavior; UI QA tests integrated help and role access; backend QA checks readiness and operations; Security verifies the candidate's applicable controls. None repairs the author's artifact or executes deployment on DevOps' behalf. Human gates require all current PASS verdicts. Explicit `preparation.mode=reviewed_task` authorization permits coordinator `complete` at G3–G5, not at G0/G0.5/G1/G6/G7/G8-review/G8/G9. G10 completion is separately described below. Legacy G2 approval/completion semantics remain unchanged outside this mode.

## Author and reviewer receipt

Each `submit` and `review` event has `stage_receipt`, a project-relative POSIX JSON path, and `stage_receipt_sha256`. The receipt has:

- `version: 1`, `actor`, `gate`, `phase` (`null` outside per-phase gates), `revision` matching the event;
- `role: "author"` on submission, or the required review sector such as `qa_spec` on review;
- `artifacts`: the exact submitted artifact map, with each entry `{ "path": "...", "sha256": "..." }`;
- `knowledge` and nonempty `checks` as defined below;
- for reviewers, `findings_sha256` matching the event's existing `evidence` file.

Keep receipts and evidence immutable. Reviewer identities differ from the author and the other required reviewers. A new submission revision resets current reviews. The existing four-field spec findings and G3/G6 `consultation` plus `consultation_sha256` remain required; the generic receipt does not replace them.

`knowledge.navigation` requires `method`, `query`, `evidence`, `sha256` and `status`. The evidence is a hashed project-local JSON record of the actual navigation; its `status` or `runtime_status` must match the declaration:

| Method | Required declaration |
|---|---|
| `graphify` | Successful actual query with status `GRAPHIFY`; pointers alone do not verify sources |
| `lexical` | Actual fallback status `INDEX_MISSING`, `INDEX_STALE`, `INDEX_INVALID`, `UNAVAILABLE` or `GRAPHIFY_UNAVAILABLE`, plus `reason` |
| `reuse` | Status `VERIFIED`, `original_navigation`, `original_navigation_sha256`, `revision` and current `applicability` |

After navigation, read only selected canonical sources. `knowledge.sources` contains nonempty records with `kind: "project"`, `"bundle"` or `"remote"` (default `project`), `path`, `sha256`, `revision`, `locator`, `observation` and `status: "VERIFIED"`. Project and bundle paths resolve safely within the client project or the TFD bundle that owns the evaluator. A bundle source does not need copying into the project. A remote source additionally records its original HTTPS `origin`; its `path` and hash bind project-local consultation evidence, not proof that the remote page was read. Mandatory reads survive ranking and fallback. External decisive technical claims still need primary-source verification. Reuse navigation economically, while each independent reviewer performs their own source check.

Each `checks` entry has `command`, integer `exit`, `result` (`PASS`, `FAIL`, `BLOCKED`) and `observation` describing what actually happened. PASS requires exit 0; unresolved results cannot support advancement or reviewer PASS. Author submissions may record failed self-checks honestly and return to REWORK; REWORK/BLOCKED reviewers may also record failed checks. Record the actual verification procedure; do not invent a command execution for a visual or documentary observation. Use the existing evidence records for detailed manual observations and state verification limits.

## Handoff and execution

At G2, submit the author receipt and normal Discovery artifacts first. A subsequent `handoff` event from the coordinator carries the same `artifacts` and `sha256` maps plus nonempty `evidence`; it transfers the package to G3. It is neither approval nor autonomous task-preparation authorization. The G3 submission also has an author receipt bound to that snapshot. G3 independently reviews the matching package before acceptance and architecture; there is no additional G2 QA.

At every G7, also submit immutable `task_snapshot`, `sector_receipts` and `execution_checkpoint` entries in the event's `artifacts` map, with matching entries in its `sha256` map and the author's `stage_receipt.artifacts` map. `task_snapshot` is a byte-for-byte JSON copy of the approved G6 Task for that phase: its SHA-256, Task ID and contract revision match the approval's submitted Task. Preserve these copies separately; do not reserialize a snapshot or replace it with the latest Task.

Checkpoint and MT review bindings use that phase's approved snapshot, phase and attempt. Every checklist item in the phase is verified, and each MT has independent current-attempt PASS with hashed review evidence. Validate these bindings for **all** historical and current G7 submissions, even after a later G6 updates the canonical `task.json` in place. Preserve that active Task path, ID and revision rules. Preserve the existing checkpoint and sector-receipt formats. Phase QA still checks integration; MT PASS alone cannot approve the phase. This new snapshot requirement does not reinterpret legacy workflows.

## Release and deployment

G9 `release_candidate` is a project-local JSON artifact containing `candidate` (project-relative artifact path), `candidate_sha256` and explicit `target`. Retain the exact artifact used for staging and review. The human G9 `approve` event additionally names `deploy_authorization` and `deploy_authorization_sha256`. That JSON contains:

```json
{
  "version": 1,
  "action": "deploy",
  "actor": "the-approving-human",
  "revision": "the-current-G9-revision",
  "release": {
    "candidate": "releases/bundle.bin",
    "candidate_sha256": "the-actual-sha256",
    "target": "the-approved-environment"
  },
  "attempt": 1,
  "observation": "Reference to the explicit human deployment decision"
}
```

G10 submits `deployment` and `post_deploy_checks` JSON artifacts. Both bind the same `release`, current `attempt`, `authorization: { "path": "...", "sha256": "..." }`, and nonempty executed `checks` with the same command/exit/result/observation format. Failed deployment checks remain honest observations; they cannot support PASS or `Done`. QA REWORK returns to G9 for candidate review and new explicit authorization before another attempt. Preserve approved recovery and do not silently retry under an earlier decision.

After all G10 independent reviewers PASS, a distinct coordinator records `complete` with evidence. This closes verification under G9's explicit authorization without another human gate. It does not deploy anything itself or grant merge permission. Installation, publication and merge retain their separate permissions.

The Python evaluator validates local bindings and declarations. It does not authenticate actors, enforce real-world permissions, prove source reading, verify remote truth or execute application checks on the author's behalf.
