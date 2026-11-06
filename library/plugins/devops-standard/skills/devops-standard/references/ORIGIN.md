# Origin and adaptation ledger

Audit date: 2026-09-23. Method: COPY → AUDIT → ADAPT → INTEGRATE.
The copy phase fetched source text read-only for inspection; no upstream script
was executed. Only the adapted artifacts below are distributed, not a raw
upstream mirror. Git blob IDs identify exact inspected file content.

## Pinned sources

| Source | Revision / inspected path | Result |
| --- | --- | --- |
| [Registry ops](https://github.com/majiayu000/claude-skill-registry/tree/9ba44de0d197c52eb94ecd0c12c8bb394c97d242/skills/devops/ops-devops-platform) | `9ba44de0d197c52eb94ecd0c12c8bb394c97d242`, `skills/devops/ops-devops-platform/` | Discovery source, contains SKILL.md and metadata, not referenced template assets; metadata points to original below |
| [Original ops](https://github.com/vasilyu1983/AI-Agents-public/tree/8dc5de47c1db00f8ba01806f5dddd798fc78cf22/frameworks/shared-skills/skills/ops-devops-platform) | `8dc5de47c1db00f8ba01806f5dddd798fc78cf22`, `frameworks/shared-skills/skills/ops-devops-platform/` | MIT; original SKILL and selected real assets fully inspected |
| [Original license](https://github.com/vasilyu1983/AI-Agents-public/blob/8dc5de47c1db00f8ba01806f5dddd798fc78cf22/LICENSE) | same revision, root LICENSE, blob `41884086c2495446a5a9d53a1cd71d56e782e5a0` | Complete notice preserved in [THIRD_PARTY_NOTICES](../../../THIRD_PARTY_NOTICES.md); copyright 2025-2026 Vasiliy Uvarov |
| [Registry review metadata](https://github.com/majiayu000/claude-skill-registry/blob/9ba44de0d197c52eb94ecd0c12c8bb394c97d242/skills/devops/devops-review/metadata.json) | `9ba44de0d197c52eb94ecd0c12c8bb394c97d242` | NOASSERTION/restricted; excluded, no text/scripts/templates adapted |
| [Anthropic structural example](https://github.com/anthropics/claude-code/blob/d78be9481b889e11186ec4578b4f5e9301396e25/plugins/plugin-dev/skills/plugin-structure/examples/advanced-plugin.md) | `d78be9481b889e11186ec4578b4f5e9301396e25` | Inspected as structural reference only, no code/text/assets copied; no MIT claim for this source |

The registry metadata's 2025 copyright is older than the original pinned
LICENSE's 2025-2026 notice. Preserve the original notice, not the shorter
metadata. Licensing is tracked per source, not inferred for the whole registry.

## Adapted content map

Original paths below are relative to
`frameworks/shared-skills/skills/ops-devops-platform/` at the original revision.

| Original source | Local destination | Substantive retained content | Adaptation |
| --- | --- | --- | --- |
| `SKILL.md` | `../SKILL.md` | Smallest viable toolchain; domain routing; separation of static, target, runtime and recovery evidence | Native Harness task/receipts, project-first choices, security ownership and human gates; removed unavailable sibling links, learning-write automation and unconditional IaC/GitOps policy |
| `assets/cicd-pipelines/template-ci-cd.md`, blob `1cfb8fca3ff704bfb4175ce24567d800fb0bd0f9` | `../templates/ci-cd-plan.md` | Service/pipeline/target/artifact overview, source-to-verification stages, build/test/promotion checklists, rollback trigger/method/steps/post-validation fields | Removed direct prod deploy/publish/GitOps push commands and invalid pip upload; no automatic staging assumption or fixed recovery-time promise; added actual command/exit evidence and explicit human gate |
| `assets/kubernetes/template-ha-dr.md`, blob `71da242bdcbfbe6ec337777d204a9691a9f8e686` | `../templates/backup-restore-plan.md` | Owner/service, RTO/RPO, component recovery map, isolated restore with integrity/application checks, post-restore validation | Removed disable-production-alerts instruction, automatic promotion/failover and forced multi-region/Kubernetes; added authorization, protected data, distinct backup/restore evidence states |

No upstream files are distributed unchanged. These meaningful adaptations are
covered by the complete upstream MIT notice, not claimed as wholly original.

## Audited but not copied

- `assets/docker/template-docker-ops.md`, blob
  `7dcf8728308ec3927ca258653e205fa46624d087`: rejected outdated hardcoded
  image examples, automatic push/latest flows and broad port bindings.
- `assets/monitoring-observability/template-alert-rules.md`, blob
  `dfeb8864b3fc1fe6e1965ed25e790cbd8c3b08a5`: did not copy the misleading
  latency annotation or global service-unscoped thresholds.
- Anthropic enterprise example: retained only organizational insight for
  resources beside a canonical skill. No second orchestrator, custom MCP
  servers, hooks, installation scripts or security scanner were imported.
- Restricted review source: omitted entirely. [review.md](review.md) and
  [finding template](../templates/finding.md) are independently authored from
  user requirements and local Harness contracts, not a disguised translation.

## Original local extensions and integration

The remaining domain references, operational-change/finding templates, tool
registry, human operational gates and ownership rules implement the approved
TASK-006/module-spec. Commands are conditional guidance, not evidence they ran.
Version-sensitive commands must be checked against current official docs and
actual runtime. Selected official references are linked in domain documents.

Reuse existing Harness capability routing, tool-state helper and receipts.
No new orchestration/installation subsystem, MCP catalog or security-tool owner.
Environment Bootstrap is absent from selected main base
`83e1c7296497c34267d85105f352b460136a09a7`; integration remains pending
NOT VALIDATED. Its separate branch/PR is not falsely reported as merged.
