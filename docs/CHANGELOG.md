# Histórico de mudanças do TFD

O [manifesto](../.codex-plugin/plugin.json) informa a versão do pacote. O commit
identifica a revisão exata. O [instalador](GUIA-CODEX.md#canal-de-revisão) compara
a revisão instalada com a do canal consultado.

## Como registrar uma atualização

Inclua a entrada neste arquivo na mesma mudança que altera o TFD. Registre a data,
o canal, a **motivação**, o que a atualização **corrige**, o que **melhora** e a
**verificação** feita. Aponte para o contrato, ADR ou incidente quando houver.
Enquanto estiver em revisão, mantenha a entrada em **Em revisão**. Ao publicar,
associe a entrada à versão do manifesto e inclua o link do commit ou PR. Confira
a versão, a revisão publicada no canal e o link deste histórico no topo do
[README](../README.md). Atualize a [tabela de mudanças recentes](../README.md#atualizações-recentes)
quando a mudança afetar quem instala ou usa o framework. [Referência de estrutura](https://keepachangelog.com/en/1.1.0/)

## Em revisão

### Modelo de revisão humana da Task

- **Motivação.** Permitir que o revisor confira a entrega e cada microtarefa com o contexto técnico necessário.
- **Corrige.** Exibe critérios, testes, referências e restrições junto aos checklists. Mostra o estado de QA e de checkpoint conforme os registros disponíveis.
- **Melhora.** O Harness gera a revisão em seções recolhíveis para a Issue e uma versão HTML com **Copiar Markdown**. O exemplo é genérico. A aprovação continua registrada na revisão correspondente da Issue. [Modelo e comandos](sector-task.md#human-review)
- **Verificação.** A suíte local passou, exit 0. No Edge, o teste conferiu o conteúdo entregue à API de clipboard simulada, a seleção manual quando o clipboard é bloqueado e a marcação exclusiva da revisão. A API Markdown do GitHub reconheceu as seções, os checklists e o bloco Mermaid do exemplo genérico.

### Governança GitHub por projeto e instalação por prompt

- **Motivação.** Evitar consultas ao repositório errado e decisões de permissão antes de confirmar o destino e a responsabilidade. Facilitar a instalação em um chat novo.
- **Corrige.** G0.5 vincula a conta, os repositórios, as branches e o Project a um contrato com aceite humano. Cada ação tem responsável, permissão verificada e autorização própria. Pedidos de conferência ficam em leitura.
- **Melhora.** O Harness separa os bloqueios de quadro, Issue, Git e deploy. O card só avança após o PASS aplicável da revisão atual e o registro na mesma Issue. O prompt obtém a fonte oficial e o README aponta da versão para o histórico completo. [Contrato](../skills/TFD-devops/references/project-governance.md) · [Quadro](delivery-board.md)
- **Verificação.** A consulta do instalador confirmou o canal oficial em um clone temporário. O teste de G0.5 confirmou o vínculo entre snapshot, hash e aceite e detectou alteração posterior no artefato, exit 0.

### Documentação de uso, arquitetura e histórico

- **Motivação.** Facilitar a instalação e o primeiro uso e explicar por que o TFD adota cada bloco.
- **Corrige.** Atualiza comandos, canais e limites. Remove da descrição atual adaptadores e etapas que ainda não estavam disponíveis.
- **Melhora.** Prompt de instalação no topo, guia da primeira entrega, mapa dos blocos, fontes ligadas às decisões e histórico por revisão.
- **Escopo.** Documentação da versão `0.1.6`.
- **Verificação.** Links internos, commits e versão conferidos. Validador da Task, consulta do fluxo inicial e suíte local passaram, exit 0.

## 0.1.6

### 2026-11-11 · Retomada, roteamento e atualização do Codex

Canal `office/reviewed-delivery`. [Commit `10eb0f2`](https://github.com/guilhermedemorais-dev/TFD/commit/10eb0f28818165381ae1196da9dcb46f57947ffd)

- **Motivação.** Retomar entregas após interrupções e reduzir a releitura de contexto entre agentes.
- **Corrige.** Vincula checkpoints à revisão aprovada, detecta alterações fora do recorte e invalida evidências dependentes quando houver correção de uma microtarefa.
- **Melhora.** Retomada por item, reaproveitamento de achados do projeto, escolha de perfis autorizados com fallback, medição de compactação do Codex, prontidão DevOps inicial, quadro por fases com etiquetas de QA e consulta de atualizações por branch.
- **Verificação.** 163 testes e 245 subtestes, exit 0, com QA independente. Codex nativo e compactação foram exercitados localmente. Os cenários de provedor alternativo usaram dados simulados. [Execução](../skills/TFD-harness/references/execution.md) · [Quadro](delivery-board.md)

### 2026-11-11 · Contrato de Task nativa

Canal `office/reviewed-delivery`. [Commit `e138636`](https://github.com/guilhermedemorais-dev/TFD/commit/e1386369b6f9d529d7850b0d27a6c41045c545fa)

- **Motivação.** Dar a autores, executores e revisores uma referência única para a Task de módulo.
- **Corrige.** Explicita o JSON canônico e a relação da spec e da visão Markdown com ele.
- **Melhora.** Orienta autoria por setor, validação e geração da visão humana a partir do mesmo contrato. [Task por setor](sector-task.md)

### 2026-11-10 · Coleta da suíte no Windows

Canal `office/reviewed-delivery`. [Commit `91e92f4`](https://github.com/guilhermedemorais-dev/TFD/commit/91e92f4efb310bcf3a83094004ef40601359a562)

- **Motivação.** Tornar a suíte executável em uma instalação Windows limpa.
- **Corrige.** Adiciona o marcador de pacote de testes para resolver imports de fixtures compartilhadas no pytest.
- **Melhora.** Documenta pytest como dependência de manutenção e registra a reprodução. [Incidente INC-003](office/incidents/INC-003.json)

### 2026-11-10 · Handoffs e atualização preservadora

[Commit `aed39a8`](https://github.com/guilhermedemorais-dev/TFD/commit/aed39a843c74851f658e1e85a63a65b2946dadba)

- **Motivação.** Identificar quem coordena e executa cada microtarefa e atualizar instalações com conteúdo local.
- **Corrige.** Explicita o papel do coordenador no topo da Task. O atualizador aplica o delta revisado sobre a instalação e interrompe em conflitos.
- **Melhora.** Mostra responsáveis, limites, entregáveis e aceite por microtarefa. Permite simular a atualização e cria backup para rollback. [Incidente INC-002](office/incidents/INC-002.json) · [Guia de atualização local](GUIA-CODEX.md#atualizar-uma-versão-local-aprovada)

### 2026-11-09 · Preparação revisada e Discovery por lacuna

[Commit `d134c38`](https://github.com/guilhermedemorais-dev/TFD/commit/d134c3887f79937d413172fedfe418ecb97024ed)

- **Motivação.** Apresentar uma Task revisada para aceite humano com menos repasses e pesquisa repetida.
- **Corrige.** Exige que o parecer de QA corresponda à spec e à revisão submetidas e preserva as leituras obrigatórias.
- **Melhora.** Com autorização registrada, o coordenador conclui G2–G5 após as verificações aplicáveis. O Discovery consulta fontes por lacuna, incluindo o guia externo de Matthew Kerns na origem. [Spec e critérios](reviewed-delivery/README.md) · [QA](reviewed-delivery/qa-review.md)

### 2026-11-09 · Graphify no bundle do TFD

[Commit `38197b7`](https://github.com/guilhermedemorais-dev/TFD/commit/38197b7730c9925207f1aea01c615e04daf23209)

- **Motivação.** Recuperar referências da biblioteca com fonte identificável e custo de contexto limitado.
- **Corrige.** Sinaliza índice desatualizado e fornece consulta lexical de contingência. Migra nomes internos legados para TFD.
- **Melhora.** Integra consulta local ao bundle, extração isolada e suporte de consulta Windows/WSL. [Operação](../library/docs/operations/graphify.md) · [Verificação local](receipts/2026-11-09-graphify.md)

### 2026-11-09 · Instalação e atualização pelo Codex

[Commit `e3c442f`](https://github.com/guilhermedemorais-dev/TFD/commit/e3c442fbb30595bc4629e8b3ac5eaac8eeddeccd)

- **Motivação.** Instalar e conferir o framework em outras máquinas com um procedimento reproduzível.
- **Corrige.** Centraliza o preparo de Python, catálogo, subagentes e instruções do perfil no instalador.
- **Melhora.** Introduz consulta de revisão, atualização e guia para Windows e Linux. [Guia do Codex](GUIA-CODEX.md)

### 2026-11-06 · Primeira publicação neste repositório

[Publicação `50376ea`](https://github.com/guilhermedemorais-dev/TFD/commit/50376ea2636b70cbf5f11a8eabdfecbf7f35e656) · [Uso no Desktop `d3dd925`](https://github.com/guilhermedemorais-dev/TFD/commit/d3dd9256c71ce90abbfe0c5ef4a75f008f6e7d25) · [Pacote `0c10d00`](https://github.com/guilhermedemorais-dev/TFD/commit/0c10d008c168bf10ce618e847cf6cd6b90f6cf01) · [SO `abac181`](https://github.com/guilhermedemorais-dev/TFD/commit/abac18196b2cafa0ae41a28de9576e0c360dfecb) · [Origem `ba76644`](https://github.com/guilhermedemorais-dev/TFD/commit/ba76644cd328974c3b54b34c9ea5064c693345d0)

- **Motivação.** Distribuir o método, os agentes e os contratos da fábrica de software em um repositório dedicado.
- **Corrige.** Ajusta o caminho da origem, a identificação do sistema operacional e o conteúdo do pacote de instalação.
- **Melhora.** Disponibiliza a versão `0.1.6` do plugin e orienta o uso no Codex Desktop.
