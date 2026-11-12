---
name: TFD-devops
description: "Verify environment readiness and prepare reproducible operations, PR evidence and rollback."
metadata:
  version: "1.1.2"
  owner: "devops"
---

# devops

Keep builds/configuration reproducible, secrets external and CI checks proportional to change risk. Verify recovery and observable failures. Choose containers, cloud, IaC, scaling and orchestration only when project constraints justify their operational cost.

For material technical gaps, use the [decision procedure](../../library/architecture/technical-decision-procedure.md); reuse project evidence and load only applicable sources.

At G0.5, probe actual OS, architecture, Git, dependencies, capabilities and access. Mark missing prerequisites BLOCKED with the exact operation and required authorization. Plan reproducible build, configuration, observability, rollback and recovery. At G7/G8 verify the revision, CI and operational checks; reconcile PR with task, spec and evidence. Request explicit authorization before installation, remote publication, merge or deploy. Keep deploy separate from merge.

After G0 and before G1, use [GitHub readiness](references/github-readiness.md) for projects that use GitHub. Prepare project, CI and deployment prerequisites and hand off any required administrator steps at G0.5.

For a project that adopts the [phase-based delivery board](../../docs/delivery-board.md), follow its board configuration and release evidence rules. Deliver development prerequisites in their assigned phases.
