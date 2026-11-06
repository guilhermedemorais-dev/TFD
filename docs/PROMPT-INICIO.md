# TFD sector handoff prompt

Copy this prompt into the next chat. Replace `SECTOR`.

```text
Build one The Factory Developer (TFD) sector from the plugin root.

SECTOR: <sector>

Read README.md, docs/00-arquitetura.md, docs/ESTADO.md, and
skills/TFD-maintenance/references/skill-standard.md. Consult the closest
existing sector and only relevant library entries.

Propose files, scope, and acceptance criteria. Wait for approval before editing.
Use the architecture's sector name, TFD- prefix, and host-agnostic paths.
Follow the skill standard: concise English, required frontmatter, and size limits.
Use the TFD library for references; keep project knowledge in project docs.
Put deterministic checks in Python. Keep evidence and output paths explicit.
The author cannot approve their own work.

Deliver agent.json, SKILL.md, any needed scripts, and routing tests
(two positive, one negative). Run the local suite and host behavior cases in
the same pass. Check decisions, outputs, and permissions. Label mocked tools.
Update docs/ESTADO.md. Report changed files, test commands, exit codes, and
open work. Stop after this sector.
```
