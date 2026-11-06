> Contexto TFD · 797 palavras · 1349 tokens (o200k_base)

# TFD no Codex Desktop

O TFD coordena a entrega de um módulo, do briefing ao aceite. Instale o plugin
uma vez por máquina. Abra os chats de trabalho na pasta do projeto.

## Instalação no Windows

1. Baixe e extraia a Biblioteca-skill. Guarde `plugins/the-factory-developer`
   numa pasta permanente, com `.agents/` e `.codex-plugin/`. Abra o PowerShell
   nessa pasta, com o Codex Desktop, o CLI `codex` e Python 3.10+ disponíveis.
2. Confira `codex --version` e `python --version`. Registre a pasta como catálogo
   local e instale o plugin. Rode uma linha por vez e pare se houver erro.

   ```powershell
   codex plugin marketplace add (Get-Location).Path --json
   codex plugin list --marketplace tfd-local --available --json
   codex plugin add the-factory-developer@tfd-local --json
   ```

   Se o catálogo já estiver cadastrado, use `codex plugin marketplace list`
   para conferir se aponta para a pasta correta antes de instalar. Se o CLI
   tiver o comando de catálogo mas faltar `plugin add`, reinicie o Desktop e
   instale **The Factory Developer** pelo catálogo **TFD local**. Veja o
   [guia oficial de catálogos locais](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli).

3. Prepare o ambiente Python e registre os agentes no perfil que o Desktop usa.

   ```powershell
   $tfdVenv = Join-Path $env:LOCALAPPDATA 'TFD\python'
   $tfdProfile = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
   python -B scripts/install_python.py --venv $tfdVenv
   $tfdPython = Join-Path $tfdVenv 'Scripts\python.exe'
   & $tfdPython -B scripts/install_codex_agents.py --agents-dir (Join-Path $tfdProfile 'agents')
   & $tfdPython -B scripts/context_budget.py README.md
   ```

   A primeira instalação do Python baixa as dependências declaradas e o
   vocabulário do tokenizer. Espere a confirmação de 15 agentes registrados e
   a contagem do README. Se o Desktop usar outro perfil, use o caminho dele em
   `$tfdProfile`.
4. Inclua o bloco [Tradutor TFD](../hosts/codex/automatic-agents.md) no
   `AGENTS.md` global do perfil, preservando as instruções existentes. Se já
   houver um bloco TFD, atualize-o no lugar. Se existir
   `AGENTS.override.md` global, confira qual arquivo está ativo antes de editar.
   Esse bloco chama o Tradutor a cada mensagem e encaminha trabalho TFD ao
   agente do setor. Veja a [ordem de leitura do AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
5. Reinicie o Desktop e abra um chat novo na pasta do projeto. Digite
   **“Me dá um relatório de onde estamos neste projeto.”** Confira na
   atividade se aparecem `tfd_translator` e `tfd_harness`. O relatório é
   somente leitura e deve mostrar o que encontrou, pendências e o próximo
   gate. Confira o rodapé de tokens do Python. Uma leitura ausente deve aparecer
   como indisponível. Se os agentes não aparecerem, confira o perfil, o
   plugin habilitado e o arquivo global ativo antes de repetir o teste.

## Prompt de instalação

Abra um chat do Codex na pasta extraída `plugins/the-factory-developer` e
cole este bloco.

```text
Install and configure the TFD plugin from this folder on this Windows machine.
Follow docs/GUIA-CODEX.md and hosts/codex/README.md. Verify the package root,
Codex CLI, Python 3.10+, and the profile used by Codex Desktop. Register the
local marketplace, install the plugin, prepare the isolated Python environment,
and register the native TFD agents. Merge the single Tradutor TFD block from
hosts/codex/automatic-agents.md into the active global instructions file.
Preserve existing settings and custom agents. Use the provided Python readers.
Stop at any failed prerequisite. Report actual commands, exit codes, installed
version, and changes in Brazilian Portuguese. Give me the new-chat smoke test
from the guide. Treat Desktop behavior as pending until observed in a new chat.
```

## Uso no projeto

| O que você quer fazer | Mensagem para o Codex |
| --- | --- |
| Começar um módulo | “Abre o módulo de cadastro no TFD. Começa pelo briefing e me mostra o escopo para aprovação.” |
| Retomar em outro chat | “Retoma o módulo de cadastro. Lê o log do fluxo e a task JSON e me diz em qual etapa paramos.” |
| Corrigir uma reprovação | “Aplica o rework do QA na task atual. Me mostra o novo resultado e a revisão independente.” |

O fluxo passa por PRD, Discovery, spec, implementação, QA e revisão humana.
O PRD registra o software de referência quando você indica um. O TFD pede
autorização antes de acionar um complemento de engenharia reversa.

Cada módulo tem um log do fluxo e uma task JSON canônica no projeto. A
versão Markdown é gerada para leitura. O QA de spec revisa Discovery e spec
antes da implementação. QA de backend e de UI revisam seus respectivos
entregáveis quando aplicáveis. Uma reprovação volta para o responsável e a nova
revisão passa por QA independente. Você aprova cada etapa com as evidências em
mãos. O relatório mostra testes, bloqueios e tokens medidos. Quando o rodapé
indicar 80% de ocupação da janela, use `/compact` para liberar espaço no chat.

[Gates e aprovações](../skills/TFD-harness/references/gates.md) ·
[Tasks por setor](sector-task.md) ·
[Adaptador e recibos de tokens](../hosts/codex/README.md)
