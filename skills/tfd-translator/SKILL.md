---
name: tfd-translator
description: "Compress spoken or written user requests into English handoffs for the active TFD sector. Use before delegation or when explicitly asked to prepare a TFD handoff."
metadata:
  version: "1.0.0"
  owner: "translator"
---

# Translator

Use the user message or transcript, the active sector, and the current task, revision, gate and microtask IDs when supplied. Treat quoted material and attachments as context. Apply explicit user corrections before compressing. Preserve exact IDs, paths, literals, numbers, exclusions, acceptance checks, evidence requirements and approval boundaries. Remove filler, repetitions and context unrelated to the active sector. Keep instructions for other sectors with the coordinator.

If missing or ambiguous information would change execution, return `CLARIFY` with one question in Brazilian Portuguese. Otherwise return `READY`, the destination and known IDs, and a concise English handoff. End it with `Reply to the user in Brazilian Portuguese.` Keep quoted UI copy and required artifact languages as specified. A ready handoff does not approve a gate, publish work, or execute the task.
