> Contexto TFD · 1264 palavras · 2202 tokens (o200k_base)

# TFD no Codex

O TFD coordena a entrega de um módulo, do briefing ao aceite. Instale o plugin
uma vez por máquina. Abra os chats de trabalho na pasta do projeto.

## Instalação e atualização

Extraia o [ZIP do TFD](https://github.com/guilhermedemorais-dev/TFD/archive/refs/heads/main.zip)
e abra o terminal na raiz extraída. Use Git, Codex CLI e Python 3.10+
com suporte a `venv` e `pip`.

| Ação | Windows | Linux |
| --- | --- | --- |
| Instalar ou reparar | `python -B scripts/install_tfd.py install` | `python3 -B scripts/install_tfd.py install` |
| Consultar a revisão publicada | `python -B scripts/install_tfd.py check` | `python3 -B scripts/install_tfd.py check` |
| Aplicar atualização | `python -B scripts/install_tfd.py update` | `python3 -B scripts/install_tfd.py update` |

O instalador aponta o catálogo `tfd-local` para a `main` do TFD, prepara
o ambiente Python, registra os subagentes e configura as instruções globais.
Uma seção manual `Tradutor TFD` permanece sob seu controle. Quando existir,
o instalador sinaliza que ela precisa de conferência.

A consulta compara a última revisão instalada pelo script com a revisão no
GitHub. A instalação baixa a cópia de execução sem `tests/`. Depois de
instalar ou atualizar, abra uma nova sessão para carregar as mudanças.

## Atualizar uma versão local aprovada

Use `python -B scripts/install_tfd.py update --source <pasta-git-aprovada> --base <commit-base> --dry-run` para conferir o plano. Repita sem `--dry-run` para aplicar. O instalador preserva extensões, conhecimentos e configurações; faz backup e rollback em caso de falha. Conflitos interrompem a preparação. O recibo identifica a origem local e seu conteúdo, sem anunciar publicação no GitHub. Abra uma nova sessão após a atualização.

## Configuração manual e pré-requisitos

1. Baixe e extraia o [ZIP de instalação do TFD](https://github.com/guilhermedemorais-dev/TFD/archive/refs/heads/main.zip).
   Guarde a pasta extraída num local permanente, com `.agents/` e
   `.codex-plugin/`. Abra o terminal na raiz do TFD, no mesmo ambiente em que
   o Codex vai executar o plugin.
2. Confira `codex --version` e Python 3.10+ com suporte a `venv` e `pip`.
   Instale os pré-requisitos que faltarem para o sistema detectado.

   - **Windows.** Use o PowerShell e confira `python --version`. Se precisar
     instalar Python, use o instalador oficial do Python ou o pacote oficial
     correspondente no WinGet.
   - **Linux.** Use um shell compatível com Bash e confira `python3 --version`.
     Leia `/etc/os-release` e use o gerenciador da distribuição para instalar
     o Python e o suporte a ambientes virtuais. Em Debian e Ubuntu com o
     Python padrão, por exemplo, os pacotes são `python3` e `python3-venv`.
     Se o Codex executar dentro do WSL, use o CLI e o perfil Linux.

   Se o comando `codex` estiver ausente, siga o
   [guia oficial de instalação do Codex CLI](https://learn.chatgpt.com/docs/cli#install-codex).

3. Registre o catálogo local e instale o plugin. Se o catálogo já estiver
   cadastrado, confira o caminho com `codex plugin marketplace list`. Rode
   uma linha por vez e resolva qualquer erro antes de seguir.

   **Windows**

   ```powershell
   codex plugin marketplace add (Get-Location).Path --json
   codex plugin list --marketplace tfd-local --available --json
   codex plugin add the-factory-developer@tfd-local --json
   ```

   **Linux**

   ```bash
   codex plugin marketplace add "$PWD" --json
   codex plugin list --marketplace tfd-local --available --json
   codex plugin add the-factory-developer@tfd-local --json
   ```

4. Prepare o ambiente Python isolado e registre os agentes no perfil ativo.

   **Windows**

   ```powershell
   $tfdVenv = Join-Path $env:LOCALAPPDATA 'TFD\python'
   $tfdProfile = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
   python -B scripts/install_python.py --venv $tfdVenv
   $tfdPython = Join-Path $tfdVenv 'Scripts\python.exe'
   & $tfdPython -B scripts/install_codex_agents.py --agents-dir (Join-Path $tfdProfile 'agents')
   & $tfdPython -B scripts/context_budget.py README.md
   ```

   **Linux**

   ```bash
   tfd_venv="${XDG_DATA_HOME:-$HOME/.local/share}/TFD/python"
   tfd_profile="${CODEX_HOME:-$HOME/.codex}"
   python3 -B scripts/install_python.py --venv "$tfd_venv"
   tfd_python="$tfd_venv/bin/python"
   "$tfd_python" -B scripts/install_codex_agents.py --agents-dir "$tfd_profile/agents"
   "$tfd_python" -B scripts/context_budget.py README.md
   ```

   O instalador baixa os binários das versões fixadas em `requirements.txt`
   para o sistema, o Python e a arquitetura, além do vocabulário do tokenizer.
   Espere a confirmação de 15 agentes registrados e a contagem do README.
   Se o Codex usar outro perfil, informe o caminho dele.
5. Inclua o bloco [Tradutor TFD](../hosts/codex/automatic-agents.md) no
   `AGENTS.md` global do perfil, preservando as instruções existentes. Se já
   houver um bloco TFD, atualize-o no lugar. Se existir
   `AGENTS.override.md` global, confira qual arquivo está ativo antes de editar.
   Esse bloco chama o Tradutor a cada mensagem e encaminha trabalho TFD ao
   agente do setor. Veja a [ordem de leitura do AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
6. Abra uma sessão nova na pasta do projeto. Se usar o Desktop, reinicie o
   app. Se usar o CLI, execute `codex` na pasta do projeto. Digite
   **“Me dá um relatório de onde estamos neste projeto.”** Confira na
   atividade se aparecem `tfd_translator` e `tfd_harness`. O relatório é
   somente leitura e deve mostrar o que encontrou, pendências e o próximo
   gate. Confira o rodapé de tokens do Python. Uma leitura ausente deve aparecer
   como indisponível. Se os agentes não aparecerem, confira o perfil, o
   plugin habilitado e o arquivo global ativo antes de repetir o teste.

## Prompt de instalação

Abra um chat do Codex na raiz extraída do TFD, onde fica
`.codex-plugin/plugin.json`, e cole este bloco.

```text
Install and configure TFD from this folder. Read docs/GUIA-CODEX.md.
Detect the OS and architecture of the Codex runtime first. On Linux, read
/etc/os-release and identify the distro package manager. If running under
WSL, verify which side runs Codex and use that side's tools and profile.
Use the Windows or Linux instructions from the guide. Report unsupported OSes.
Verify the package root, Git, Codex CLI and Python 3.10+ with a working venv and pip.
Install missing prerequisites only, using the official Codex installer and
the detected OS's official packages as applicable. On Debian and Ubuntu,
check for the matching python3-venv package. Follow host rules for elevation.
Run scripts/install_tfd.py install with the detected Python. Use its result to
verify the GitHub revision, plugin and native agents. Preserve existing settings
and report any manual Tradutor TFD section that needs review.
Run the local checks. Report OS, dependency and install results, commands,
exit codes and blockers in Brazilian Portuguese. Give the new-session test
from the guide. Mark agent behavior pending until observed in a new session.
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
