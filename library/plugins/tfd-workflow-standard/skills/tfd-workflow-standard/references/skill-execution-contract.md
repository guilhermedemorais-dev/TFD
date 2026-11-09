# Skill Execution Contract

Installing, listing or naming a skill does not apply its methodology. Every
orchestrator agent, executor agent or specialist LLM must prove activation.

`SKILL_RECEIPT` is a local evidence convention, not an official OpenAI, Codex,
or market standard.

## Mandatory Sequence

1. Detect applicable skills from the task, changed surfaces and repository rules.
2. Resolve the canonical path for every required `SKILL.md`.
3. Read each selected `SKILL.md` completely before acting.
4. Read every reference marked mandatory for the active phase.
5. Emit `SKILL_RECEIPT` before planning, coding, review or approval.
6. Stop when a required skill cannot be resolved or read. Do not imitate it from
   memory or silently replace it with general reasoning.

An entire SKILL.md is mandatory; an entire Human Task is not mandatory for
every specialist. Harness reads the full Task and resolves context under
`context-routing.md`. The specialist reads listed task_sections, relevant
global acceptance/constraints and required_sources; conditional_sources only
when their condition applies, optional_sources only with an actual purpose.
Missing required source/anchor stops the checkpoint. Disclosure never weakens
the active skill's mandatory rules.

## SKILL_RECEIPT

```text
SKILL_RECEIPT
- skill: <name>
  task_id: <task>
  sector: <routed ID when applicable>
  phase: <planning or validation>
  path: <canonical SKILL.md path>
  references_loaded: <exact paths or N/A>
  applied_rules: <short concrete rules>
  status: LOADED | BLOCKED
```

The receipt is execution evidence, not a summary of the entire skill. A final
handoff without receipts for all mandatory skills is `NOT VALIDATED`.

## Role Vocabulary

Use only role-neutral terms in methodology and handoffs:

- `orchestrator agent`
- `executor agent`
- `specialist LLM`

Codex, Claude Code, Antigravity, a CLI or another product may transport or host
an agent. Product names never define responsibility and never substitute for a
skill receipt.
