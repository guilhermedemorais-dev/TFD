---
name: tfd-install
description: "Install or update the TFD plugin and check its GitHub revision. Use for TFD setup, reinstall, or update requests. Route project delivery tasks through the harness."
compatibility: "Codex CLI, Git and Python 3.10+ on Windows or Linux."
metadata:
  version: "1.0.0"
  owner: "install"
  required-files: "agents/openai.yaml"
---

# TFD installation

Resolve the plugin root. Run `python -B scripts/install_tfd.py check` with Python 3.10+ (`python3` on Linux). Report the recorded installation revision, published revision and status.

Use `install` for initial setup or repair and `update` for an authorized update. Apply changes only with user authorization. Read the plugin-root `docs/GUIA-CODEX.md` for missing prerequisites and the new-session check. Report an existing manual instruction section for review. On failure, report the observed error and stop.

- “Instala o TFD neste computador.” → `install`
- “Confere se saiu atualização do TFD.” → `check`
- “Abre o módulo de cadastro no TFD.” → harness

Reply in Brazilian Portuguese unless the user requests another language.
