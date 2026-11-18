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

[PR #6](https://github.com/guilhermedemorais-dev/TFD/pull/6), atualização sobre a `main`.

### Diagnóstico de acesso ao GitHub e CI pelo DevOps

- **Motivação.** Quando uma operação falha depois da configuração inicial, o DevOps precisa dizer quem corrige o acesso e em qual tela.
- **Corrige.** A skill aciona o diagnóstico em qualquer fase. O roteiro distingue a conta do `gh`, a instalação do GitHub App, o acesso do colaborador, o Project e as permissões do job do Actions. A matriz de governança agora inclui criação de Issues.
- **Melhora.** Cada bloqueio retorna o erro observado, o ajuste mínimo e como confirmar a recuperação. Em Projects, o DevOps distingue permissão ausente no registro do App de concessão pendente na instalação. O roteiro é consultado só quando necessário. [Roteiro](../skills/TFD-devops/references/github-access-recovery.md)
- **Compatibilidade.** A conciliação com a `main` preserva o ciclo por etapa da PR #8 e publica a skill DevOps como `1.2.2`. O diagnóstico distingue permissão insuficiente em GraphQL (401) e REST (403), sem inferir a causa apenas pelo status. Para Issues, o mantenedor solicita a permissão no registro do App e o dono da instalação aprova a atualização pendente antes de conferir a concessão efetiva.
- **Verificação.** A revisão conciliada passou 11 testes focados e 290 testes da suíte completa, exit 0. Após o ajuste documental de Issues e a versão `1.2.2`, os 11 testes focados passaram novamente, exit 0. A auditoria da Oficina passou, exit 0; a referência de recuperação usa 997 tokens e preserva as fontes oficiais. O validador genérico da Skill Creator rejeita o ID legado `TFD-devops`, preservado pelo padrão do TFD. Os 165 testes da revisão anterior permanecem como evidência histórica. A ativação no OpenBot ainda não foi validada.

## 0.1.6 · Pacote por etapa — 2026-11-18

Canal de integração: `main`. [PR #8 e estado da revisão](https://github.com/guilhermedemorais-dev/TFD/pull/8).

### Vínculos históricos de QA e perfis alternativos

- **Motivação.** O code review final apontou que revisões G6 de fases anteriores podiam deixar de conferir o inventário aprovado e que a geração de agentes ignorava o perfil de destino na rota Graphify.
- **Corrige.** Cada fase conserva os vínculos do QA com seu inventário e evidências históricos, também nos fluxos com `review_version: 1` sem `stage_loop_version`. A revisão histórica usa o snapshot autêntico ou a Task ainda idêntica ao hash aprovado; sem esses bytes, registra erro em vez de aceitar um inventário sem comprovação. Os agentes usam a configuração e o índice do perfil em que foram instalados. O tradutor continua sem ferramentas e os perfis personalizados continuam protegidos.
- **Melhora.** O prompt de instalação e os exemplos do README selecionam a `main`. Canais de revisão continuam opcionais e instalações personalizadas exigem atualização preservadora.
- **Verificação.** Regressões falharam antes e passaram após a correção; a primeira solução foi reprovada pelo QA por não cobrir o protocolo anterior e foi corrigida. A suíte completa passou com 288 testes, exit 0. O QA independente conferiu omissões e IDs inventados de requisitos/regras em fases antigas, falta de evidência histórica, compatibilidade dos fluxos sem `review_version`, os 15 perfis gerados e a proteção de perfis personalizados. Esta mudança não aplica atualizações locais nem comprova um novo turno nativo do OpenBot. [INC-010](office/incidents/INC-010.json).

### Bloqueio fundamentado no QA de especificação

- **Motivação.** O code review da PR #8 encontrou um conflito entre o pipeline, que aceita `BLOCKED`, e o validador de findings, que aceitava apenas `PASS` e `REWORK`.
- **Corrige.** O parecer de bloqueio pode identificar um pré-requisito ausente com achado `blocker`, evidência e recomendação. Os vínculos com o artefato e a revisão continuam obrigatórios em G3/G6; o bloqueio não autoriza avanço nem aceite humano.
- **Preserva.** O contrato JSON mantém seus campos, `PASS` e `REWORK` mantêm suas regras e nenhuma instalação ou configuração do OpenBot é alterada por esta publicação na PR #8.
- **Verificação.** A reprodução anterior falhou em G3 e G6; após a correção, passou com exit 0. Os 59 testes focados e os 281 testes da suíte completa passaram, exit 0. Os casos conferem bloqueio válido, CLI exit 2, rejeição de avanço, campos obrigatórios e vínculos de artefato, revisão e consulta. A skill 1.8.1 passou na auditoria estática; skill e duas referências somam 2.524 tokens, contra 2.353 da base, com cada referência abaixo de 1.000 tokens. O validador genérico da Skill Creator continua rejeitando o ID legado `TFD-qa_spec`; esse ID publicado foi preservado conforme o padrão do TFD. A veracidade do pré-requisito continua sendo julgamento do QA, não prova do validador estrutural. [INC-009](office/incidents/INC-009.json).

### Graphify compartilhado entre hosts da mesma máquina

- **Motivação.** Evitar que Codex e OpenBot consultem bundles diferentes contra um índice padrão comum, provocando consultas desatualizadas e contexto divergente.
- **Corrige.** As rotas de navegação fixam o mesmo entrypoint, bundle canônico, configuração de runtime e índice. A geração dos perfis Codex explicita esses caminhos; o roteador OpenBot resolve os resultados no bundle retornado.
- **Preserva.** Skills, conhecimentos, modelos, permissões e aceites próprios dos hosts permanecem preservados. Não há nova dependência, indexação de projetos clientes ou reconstrução automática durante consultas.
- **Verificação.** A regressão falhou antes e passou após a correção; 273 testes locais passaram, exit 0, com QA independente de preservação. O índice compartilhado foi reconstruído explicitamente após backup. O primeiro teste nativo OpenBot R1 falhou com `GRAPHIFY_UNAVAILABLE`; um trace separado comprovou timeout interno de 20 segundos. Consultas posteriores inalteradas e o reteste nativo R2 retornaram `GRAPHIFY`, contexto preenchido, mesmo fingerprint e configuração/índice preservados. A causa subjacente do atraso não foi reproduzida nem comprovada; não houve alteração especulativa do IPC ou dos limites do worker. A execução nativa foi iniciada pelo usuário no TFD; o ID da mensagem não foi exposto. [INC-008](office/incidents/INC-008.json).

### REAP completo como plugin externo da Discovery

- **Motivação.** Disponibilizar a capacidade completa solicitada, sem reduzir o REA-Prompts a três referências dentro do TFD.
- **Melhora.** A Discovery 1.10.0 delega ao executor nativo usando o plugin externo completo e recebe achados, evidências e limites. Todos os 26 packs permanecem disponíveis; o executor carrega a skill aplicável à tarefa.
- **Distribuição.** Origem fixada em `9756618f25af1920c8965f8969820eed22247936`, todos os arquivos upstream e licença preservados fora do bundle TFD. O empacotador expõe a coleção inteira e corrige apenas as descrições YAML inválidas nas cópias carregáveis, mantendo corpos e nomes completos. O manifesto não instala outro motor REA.
- **Governança.** Discovery mantém a responsabilidade; QA independente e aceites continuam obrigatórios. Instalação, reconstrução e execução de alvos dependem da autorização da operação, não da presença de um prompt.
- **Verificação.** Consulte o [INC-007](office/incidents/INC-007.json) para o recorte de testes e evidências. A integração parcial anterior foi retirada e preservada apenas como diagnóstico externo.

### Ciclo completo de consulta, execução e QA em cada etapa

- **Motivação.** O fluxo visual exigia entrega revisada em cada etapa, mas o pipeline não exigia QA antes de prontidão, PRD, planejamento e documentação e encerrava o log antes da preparação/publicação.
- **Corrige.** O protocolo `stage_loop_version: 1` vincula consulta seletiva ou reutilização comprovada, fontes canônicas, verificações do autor e do revisor independente à revisão e aos artefatos atuais. O aceite depende dos pareceres aplicáveis. G7 também confere snapshots dos checkpoints e pareceres das microtarefas. Cada microtarefa citada em uma área técnica precisa de critério de aceite naquela área.
- **Melhora.** G2 transfere a pesquisa internamente a G3 para revisar a cobertura sem duplicar QA. G9 registra candidato, operação, rollback e autorização humana de deploy; G10 exige execução e verificações posteriores compatíveis com essa autorização. Correções preservam histórico, revalidam dependências afetadas e respeitam os limites de tentativas.
- **Economia de contexto.** As skills encaminham a uma referência curta por etapa. As bibliotecas permanecem consultáveis, com fontes lidas seletivamente e reutilização de registros aplicáveis. Não há cópia integral do guia nem carregamento de todos os setores.
- **Compatibilidade e limites.** Logs antigos continuam no seu protocolo; não se fabrica consulta ou PASS retroativo. O principal coordena os agentes no host. O CLI valida registros e não autentica pessoas, comprova leitura semântica ou executa deploy por conta própria. Instalações personalizadas e a adaptação OpenBot não são sobrescritas por esta PR; uma atualização delas precisa conciliar seus contratos e schemas extras.
- **Verificação.** A base anterior passou 226 testes, exit 0. A regressão do novo gate falhou antes e passou depois da correção. A suíte final passou 261 testes com `unittest`, exit 0; `pytest -q -p no:cacheprovider` passou 261 testes e 393 subtestes, exit 0. O QA independente encontrou e retestou duas falhas históricas: checkpoints de fases anteriores e vínculos da Task com a spec/cobertura aprovadas. No fechamento, oito casos próprios dessa família e 88 testes aplicáveis passaram, exit 0. Dois casos positivos e um negativo foram executados no Codex com dados sintéticos do protocolo; isso não comprova Discovery de um produto real nem o fluxo nativo do OpenBot. As 17 skills passaram na auditoria estática, com referências de até 993 tokens. [Protocolo](stage-loop.md) · [INC-005](office/incidents/INC-005.json)

### Conferência independente do QA e reconciliação da instalação

- **Motivação.** Uma reprodução sintética avançou para G4 com um requisito aprovado omitido e um PASS sem registro próprio de consulta do revisor. A instalação Codex também carregava skills anteriores às melhorias já presentes na fonte e na biblioteca compartilhada do OpenBot.
- **Corrige.** Novos workflows habilitam `review_version: 1`. G3/G6 exigem o registro independente do QA, vinculado ao PRD aprovado, aos inventários e à revisão exata dos artefatos. O QA consulta capítulos pertinentes do guia e fontes oficiais para afirmações técnicas decisivas, registra contradições e devolve lacunas materiais ao autor. O atualizador preservador aceita conteúdo instalado igual à base mesmo quando há trechos repetidos; conflitos reais continuam interrompendo a aplicação.
- **Melhora.** A conferência deixa evidências verificáveis de requisitos, regras, fontes, limites e decisões sem carregar o guia inteiro. Atualizações preservam personalizações e distinguem versão instalada de comportamento efetivamente executado.
- **Compatibilidade.** Pareceres e workflows anteriores permanecem válidos no protocolo que usavam. A task JSON e o formato de quatro campos de findings não mudam. Não há migração silenciosa de um PASS antigo.
- **Verificação.** A base desta melhoria passou 226 testes, exit 0. A regressão externa falhou antes e passou depois da correção; revisão independente de código e teste semântico isolado foram registrados no INC-004. Uma sessão nova do Harness confirmou a carga instalada e rejeitou o workflow sem consulta exigida. A prova nativa completa do OpenBot continua pendente. [Contrato](discovery-coverage.md#independent-qa-evidence) · [Incidente INC-004](office/incidents/INC-004.json)

### Discovery com cobertura e geração autônoma de tasks

- **Motivação.** Evitar que regras de negócio e contratos de interface, frontend ou backend sejam descobertos somente durante a implementação.
- **Corrige.** Discovery registra cobertura por área e fluxo. G3 exige revisão independente da cobertura antes da spec. G6 confere os inventários de requisitos/regras, a revisão de Discovery e os vínculos entre áreas técnicas, microtarefas, critérios e testes.
- **Melhora.** Com preparação revisada autorizada, o principal coordena pesquisa, spec, tasks e correções até o aceite humano. As dúvidas técnicas ficam com os agentes. Perguntas ao usuário tratam decisões materiais de negócio ou escopo ainda pendentes. O contexto de execução leva somente a cobertura e as fontes aplicáveis.
- **Compatibilidade.** Tasks e workflows legados continuam legíveis. Novos workflows são inicializados com cobertura versão 1. A revisão recolhível e os checklists existentes foram mantidos.
- **Verificação.** A suíte local passou com 211 testes, exit 0. O QA independente deu PASS após conferir vínculos de revisão, omissões de requisitos/regras, compatibilidade e recorte de fontes. As referências das skills ficaram abaixo de 1.000 tokens cada. A execução do novo fluxo no OpenBot ainda não foi validada. [Contrato e comandos](discovery-coverage.md)

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
