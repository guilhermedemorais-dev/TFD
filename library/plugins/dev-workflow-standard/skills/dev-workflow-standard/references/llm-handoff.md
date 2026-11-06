# LLM Handoff And Continuity

Agent roles are stable; LLM providers are replaceable execution resources. A
task must continue from repository evidence when the current LLM loses quota,
tokens, authentication, connectivity, context or availability.

`EXECUTION_HANDOFF` and the availability labels below are local continuity
conventions. They are not claimed as provider standards.

## Availability States

- `AVAILABLE`
- `LLM_TOKEN_EXHAUSTED`
- `LLM_CONTEXT_EXHAUSTED`
- `LLM_AUTH_UNAVAILABLE`
- `LLM_NETWORK_UNAVAILABLE`
- `LLM_TOOL_UNAVAILABLE`

Provider failure does not automatically block the task. The orchestrator agent
may select another authorized LLM capable of the same executor role.

## Mandatory Handoff

Before switching LLMs, persist:

```text
EXECUTION_HANDOFF
- previous_llm:
- availability_state:
- task_id:
- execution_contract_path:
- sector_and_phase:
- branch_and_revision:
- completed_scope:
- changed_files:
- commands_and_results:
- active_failures:
- remaining_scope:
- mandatory_skills_and_references:
- skill_receipts:
- reuse_inventory:
- minimal_code_gate:
- next_safe_action:
```

The replacement executor agent must:

1. read `EXECUTION_HANDOFF` and validate the referenced Execution Contract
2. resolve its Task sections and sources through `context-routing.md`; Harness
   reads the complete Task, specialist reads its slice and relevant global rules
3. inspect git status, diff and changed call sites
4. read all mandatory skills and emit its own `SKILL_RECEIPT`
5. verify the previous `REUSE_INVENTORY` against the current revision
6. continue from `next_safe_action`; do not restart the task
7. never create a parallel implementation to avoid understanding existing work
8. check revision/artifact freshness of dependency receipts and rerun affected
   validation before claiming completion; planning receipts do not close final gates

If repository state and handoff evidence disagree, stop and return `BLOCKED`
with the exact conflict. Conversation memory is never the source of truth.
