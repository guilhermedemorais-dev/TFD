# TASK-XXX: Nome da task

> **Resumo:** resultado, usuário afetado e limite principal em uma frase que
> permita reconhecer a task sem abrir specs ou comentários.

> A GitHub Issue é o card humano completo para ordem de execução e
> acompanhamento. O Markdown local é somente espelho portátil quando existir;
> nunca substitui a Issue disponível. O Execution Contract JSON contém as
> mesmas regras normativas, estruturadas para a LLM. Card e JSON compartilham
> `contract_revision` e exigem equivalência normativa antes de executar.
> A matriz mostra o todo; somente o Harness lê a Task completa por padrão.
> Especialistas recebem setor, fase, revisão, referências e receipts necessários.
> Cada lista executável tem um prompt que aponta para o arquivo JSON único da
> Task e seu `list_id`. Não inserir JSON neste card. O Harness compara Task
> humana e JSON; especialistas executam pelo arquivo JSON, sem ler o card humano.
> Substitua todos os placeholders. N/A exige motivo verificado; o exemplo JSON
> inicial é docs-only, não um default para dispensar setores de outras mudanças.

## Status
A fazer | Em andamento | Em revisão | Concluída | Bloqueada

## Status visual
- Status visual: A definir | 🟡 Em andamento | 🔴 Bloqueada | 🟢 Concluída
- Status Kanban: Backlog | Discovery / SDD | Ready for Dev | In Progress | Validation | In Review | Awaiting Final Approval | Done
- Pronto para GitHub Projects: sim/não

## Tipo
Feature | Bugfix | Refactor | Chore | Spike | DevOps | Docs

## Prioridade
Alta | Média | Baixa

## Issue GitHub
Link da issue (ou "criar issue: <título sugerido>").

## Branch sugerida
`feat/<modulo>-<resumo>` | `fix/<modulo>-<resumo>` | `chore/<resumo>`

## PR
PR esperado (ou "abrir PR após primeiro checkpoint"). Aponta para esta task e a issue.

## Responsável
Quem executa (dev/IA) e quem revisa.

## Revisão do contrato
- contract_revision: 1
- Equivalência card/JSON: PENDING | VERIFIED | DIVERGENT

## Discovery / SDD colaborativo

Esta etapa é feita com o usuário por perguntas objetivas, pesquisa e
consolidação de contexto. Não mover para Ready for Dev sem aprovação humana.

### Perguntas e respostas
- Pergunta:
- Resposta do usuário:
- Impacto na solução:

### Pesquisa realizada
- Fonte:
- Evidência relevante:
- Decisão suportada:

### Decisões consolidadas
- Decisão:
- Alternativas descartadas e motivo:
- Hipóteses ainda abertas:

### Relatório de encerramento do Discovery / SDD
- [ ] Publicar comentário `DISCOVERY_SDD_COMPLETED` nesta Issue.
- [ ] Registrar URL/identificador retornado, tokens e superfície alterada.
- Se a publicação estiver disponível e falhar, manter Discovery / SDD e marcar
  BLOCKED; comentário apenas preparado não conta como publicado.
- [ ] Somente depois do comentário publicado solicitar aprovação humana.

## Objetivo da task
O que esta task entrega, em uma a três frases.

## Estado atual encontrado
Comportamento, evidência e limitações observadas antes da mudança.

## Resultado esperado
Comportamento observável e verificável depois da mudança.

## Resumo do escopo
O que está incluído, em linguagem adequada para acompanhamento humano.

## Specs obrigatórias
Links das specs que são contrato desta task (product/module/page/component/validation/database/api).

## Docs obrigatórios
PRD, arquitetura, mockups aprovados e demais documentos a seguir.

## Requisitos
- REQ-01, prioridade MUST: requisito verificável e sua fonte.

## Biblioteca de referências do projeto

Preservar o registro de consulta/seleção do PRD/spec com seus IDs e justificativas,
sem repetir pesquisas válidas nem converter candidatas em fontes REQUIRED.

Guardar fontes validadas em `docs/biblioteca-referencias/`. Cada item deve
informar URL/origem, propósito, data de consulta e decisão sustentada. A task
deve apontar o arquivo e a seção exatos que cada microtarefa deve consultar.

| ID | Fonte | Arquivo e seção | Propósito | Microtarefas |
| --- | --- | --- | --- | --- |
| REF-01 | URL/origem | `docs/biblioteca-referencias/topico/fonte.md#secao` | decisão sustentada | MT-01 |

## Biblioteca de design e Design Guide

Quando houver interface, registrar Design Guide, tokens, biblioteca de
componentes, referências visuais e mockup aprovado em `docs/design/`. Quando
não houver impacto visual, marcar N/A com motivo verificado.

- Design Guide:
- Design tokens:
- Biblioteca de componentes:
- Fontes de bibliotecas selecionadas: manter ID biblioteca/ID fonte do PRD/spec,
  repo/docs oficial, versão/commit ou UNKNOWN, componente/variante, propósito/módulo,
  licença, dependências, adaptações e estado da decisão. Usar o mesmo ID em
  `references[].id` e fontes REQUIRED somente para dependências selecionadas e
  necessárias; candidatas não escolhidas não obrigam carregar todo o catálogo.
- Referências visuais:
- Mockup/frame aprovado:
- Aplicabilidade ou motivo N/A:

## Fontes globais da verdade
Liste somente fontes globais necessárias, com path/link e propósito. Specs
detalhadas permanecem nas fontes. O Harness distribui os critérios globais
relevantes para cada setor; não manda todos os documentos a todo especialista.

## Execution Contract
`docs/execution/TASK-XXX.json`

## Escopo
O que está incluído nesta task.

## Fora do escopo

<!-- Conditional: for operational infrastructure include devops-standard and
target_environment, impact, rollback_strategy, validation plan and human gates.
Omit this DevOps addition for unrelated work; keep installation state out. -->
O que NÃO deve ser feito aqui (evita PR inchado).

## Paths permitidos e protegidos
- Permitidos: caminhos que cada microtarefa pode alterar.
- Protegidos: caminhos/dados que não podem ser alterados.

## Arquivos prováveis
Caminhos prováveis a alterar (marcar `HIPÓTESE:` quando não confirmado).

## Microtarefas

Repita o bloco para cada recorte executável. Uma task pode usar skills
diferentes em microtarefas diferentes.

Declare aqui a selecao concreta feita na Discovery: skill/plugin executor,
capability, tool preferencial e ferramentas auxiliares necessarias, cada uma
com finalidade, condicao de uso e fallback aprovado quando houver. Resolva
referencias para arquivos/secoes; nao cole o catalogo inteiro nem corpos de
skills. No JSON, use os campos existentes de `microtasks`, `references` e
`execution_lists`: owner/tool nos campos proprios; ferramentas auxiliares e
condicoes nas instrucoes da lista, ou referencia obrigatoria com proposito.
Cada lista resolve seus `microtask_ids` no mesmo arquivo para obter o roteamento.
O executor parte dessa selecao, le sua skill canonica e as fontes obrigatorias;
so amplia descoberta diante de lacuna, falha, mudanca de disponibilidade ou
necessidade nova, respeitando os limites e retornando ao Harness se mudar o
contrato. Disponibilidade e receipts ficam nas evidencias, nao no JSON.

Todo checklist de etapa, microtarefa e setor deve usar caixas `- [ ]`.
Etapas complexas podem ser decompostas em subitens aninhados dentro da mesma
Task. Cada item deve ter conclusão verificável. Marque `- [x]` somente com
evidência do responsável; o item pai só termina após seus subitens aplicáveis.
Bloqueios e itens não validados permanecem desmarcados, com motivo. N/A exige
justificativa, não marcação de conclusão. Checkboxes não substituem validação
do setor nem aceite humano; seu estado não é copiado para o JSON normativo.

Para cada lista de microtarefa, etapa ou setor, gerar um único “Prompt desta
lista” com link clicável para `docs/execution/TASK-XXX.json` e o `list_id`. Usar
link real do arquivo local ou URL versionada no GitHub, conforme o destino;
não inventar URL nem apontar para a Issue em vez do arquivo. Todos os objetos
JSON das listas ficam em `execution_lists` nesse mesmo arquivo, junto ao
contexto global da Task. Não inserir blocos JSON no Markdown ou na Issue e não
criar arquivos JSON por lista. Itens/subitens não recebem prompts separados.
Listas repetidas como resumo reutilizam o ID, sem representar nova execução.

### MT-01: Título e resumo da microtarefa | Skill: skill-name | Plugin: plugin-name
- Resumo: mudança pequena e verificável.
- Skill executora: `skill-name`
- Plugin: `plugin-name`
- Capability: `capability-id`
- Tool preferencial: `tool-name` ou `repository-native-tooling`
- Ferramentas auxiliares: identificador, finalidade, condicao e fallback aprovado; ou N/A com motivo
- Depende de: IDs ou nenhuma
- Referências obrigatórias: `REF-01`, com arquivo e seção
- Paths permitidos: caminhos explícitos
- Checklist:
  - [ ] Criar teste que falha.
  - [ ] Implementar o mínimo.
  - [ ] Executar validação.
- Entregáveis: artefatos concretos
- Condição para concluir: resultado observável e evidência
- Validador independente: skill/owner aplicável

#### Prompt desta lista
Abra o [JSON da Task](../execution/TASK-XXX.json) e selecione em `execution_lists` a lista com
`list_id = MT-01/checklist`. Execute somente essa lista, incluindo subitens.
Valide task, revisão, owner, contexto global e receipt atual do Harness. Leia
sua skill, fontes obrigatórias e código relevante. Execute os itens e subitens
da lista dentro dos limites do contrato e devolva evidências por item. Não leia
a Task humana como entrada de execução; contexto ausente ou divergente deve
voltar ao Harness. Não aprove gates humanos, faça merge ou deploy.

## Matriz de Validação por Setor
Sector Validation Matrix: preencher todos os dez setores, inclusive em TRIVIAL.
Setores N/A ficam apenas nesta matriz, com motivo; detalhar somente REQUIRED.
Substitua owners genéricos por uma skill concreta. Extensões materiais têm ID,
owner e justificativa explícitos, sem criar especialistas por cerimônia.

| Setor / ID | Aplicável | Responsável | Status | Dependências finais | Motivo N/A |
| --- | --- | --- | --- | --- | --- |
| Banco / database | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| API / Backend / backend | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| Frontend / frontend | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| UI / UX / ui_ux | REQUIRED ou N/A | ui-ux-standard | PENDING ou N/A | definir | se N/A, justificar |
| QA / Testes / qa | REQUIRED ou N/A | qa-testing-standard | PENDING ou N/A | definir | se N/A, justificar |
| Segurança / security | REQUIRED ou N/A | security-standard | PENDING ou N/A | definir | se N/A, justificar |
| DevOps / Infraestrutura / devops | REQUIRED ou N/A | devops-standard | PENDING ou N/A | definir | se N/A, justificar |
| Observabilidade / observability | REQUIRED ou N/A | definir skill de instrumentação/operação | PENDING ou N/A | definir | se N/A, justificar |
| Documentação / documentation | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| Gate Final do Harness / harness | REQUIRED | dev-workflow-standard | PENDING | todos os demais REQUIRED | não se aplica |

Reutilizar PENDING, READY, RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
PASS exige evidência do owner; PARTIAL/NOT_VALIDATED não fecham REQUIRED.
N/A é aplicabilidade. Um owner solicita retrabalho, nunca atesta PASS de outro.

## Bloco de setor REQUIRED
Repita este bloco somente para cada setor REQUIRED, com âncora HTML única e ID
correspondente ao contrato (`database`, `backend`, `frontend`, `ui_ux`, `qa`,
`security`, `devops`, `observability`, `documentation`, `harness`).

<!-- Exemplo de bloco a preencher, não é resultado executado. -->
<a id="documentation"></a>
## Documentação
- Status: PENDING
- Responsável: dev-implementation-standard
- Depende de (validação final): definir
- Pré-requisitos de planejamento: definir separadamente, quando houver

### Objetivo do setor
O que este owner precisa garantir dentro do escopo.

### Fontes obrigatórias
- REQUIRED `path#anchor`: propósito concreto da leitura.

### Fontes condicionais
- CONDITIONAL `path#anchor`: condição observável; propósito da leitura.
- OPTIONAL `path#anchor`: propósito de consulta complementar, sem carga automática.

### O que fazer
- [ ] Executar ação contextual do setor, sem copiar a spec.
- [ ] Validar o resultado e registrar a evidência do responsável.

### Evidência esperada
Revisão/artefato, comandos e critérios que autorizam o resultado deste setor.

### Resultado
NOT_VALIDATED até execução. Links de SKILL_RECEIPT/EXECUTION_RECEIPT, revisão,
fontes carregadas e limitações; nunca inventar execução.

## Regras de negócio
RN aplicáveis (referência ao validation-rules-spec).

<a id="criterios-de-aceite"></a>
## Critérios de aceite
- [ ] Critério objetivo e testável, associado à evidência de aceite.

## TDD / Testes obrigatórios
- [ ] Executar os testes aplicáveis (unit, integração, e2e) e registrar resultados.
- [ ] Verificar a cobertura mínima definida pela Task.

## Validação e tools previstas
- Skill responsável:
- Capability:
- Tool preferencial (se aplicável):

O estado de instalação é local ao runtime e não pertence à task.

## Ordem de Execução
Discovery / SDD colaborativo, comentário `DISCOVERY_SDD_COMPLETED`, aprovação
humana, prontidão de ambiente/capabilities, implementação, testes do executor,
validações independentes, rework/reteste, gate do PR, Gate Final do Harness,
aceite e merge humanos. Deploy exige autorização separada.

## Implementação
Resumo: produzir os artefatos aprovados por microtarefa e camada.
- [ ] Banco: microtarefas e evidências, quando REQUIRED.
- [ ] Backend: microtarefas e evidências, quando REQUIRED.
- [ ] Frontend: microtarefas e evidências, quando REQUIRED.
- [ ] Documentação: microtarefas e evidências, quando REQUIRED.

## Testes do executor
Resumo: verificar os próprios artefatos antes da validação independente.
- [ ] Executar TDD, testes unitários, integração e demais checagens do implementador.
- Teste do executor não substitui validação independente.

## QA funcional independente
Resumo: reproduzir os cenários e verificar regressões do comportamento entregue.
- Owner: `qa-testing-standard`.
- [ ] Executar cenários e regressão; registrar evidência observável e resultado próprio.

## QA de segurança
Resumo: verificar riscos e controles dentro do escopo autorizado.
- Owner: `security-standard` quando REQUIRED.
- [ ] Executar threat/risk review e verificações autorizadas; registrar limites e resultado próprio.

## QA UI / UX
Resumo: comparar o resultado renderizado com o Design Guide e os estados aprovados.
- Owner: `ui-ux-standard` quando REQUIRED.
- [ ] Validar Design Guide, estados, responsividade e acessibilidade com evidência visual/runtime.

## DevOps e observabilidade
Resumo: verificar operação, diagnóstico de falhas e recuperação quando aplicáveis.
- Owner: `devops-standard` ou owner explícito quando REQUIRED.
- [ ] Verificar CI/CD, configuração, operação, métricas, logs e rollback aplicáveis com evidência runtime.

## Rework e reteste
- Toda falha retorna ao owner da mudança e depois ao mesmo validador.
- [ ] Registrar causa, correção, nova revisão e evidência do reteste quando houver falha.

## Checklist de execução
- [ ] Leitura da fatia e fontes obrigatórias pelo owner; Task completa pelo Harness.
- [ ] Execução do escopo.
- [ ] Testes e validação material.
- [ ] Evidências e resultado do próprio setor.
- [ ] Reconciliação dos setores.
- [ ] Handoff para review.

## Registro de Evidências
| Setor | Fase | Owner | Revisão/artefato | Receipt/evidência | Resultado/limites |
| --- | --- | --- | --- | --- | --- |
| preencher após execução | planning ou validation | owner real | revisão testada | link | resultado observado |

## Gate do PR
Task/Issue/specs/revisão consistentes; validações e documentação requeridas
evidenciadas. Sem publicação presumida a partir de Markdown local.
- [ ] Conferir consistência e evidências antes do handoff do PR.

<a id="harness"></a>
## Gate Final do Harness
Responsável dev-workflow-standard; status PENDING; depende de todos REQUIRED.
Fonte REQUIRED: Task completa e contrato, para reconciliar escopo e owners.
O que fazer: conferir critérios, resultados, receipts atuais e bloqueios.
- [ ] Reconciliar critérios e resultados dos setores REQUIRED com receipts atuais.
- [ ] Registrar decisão fundamentada e bloqueios restantes.
Evidência esperada: reconciliação de cada setor e decisão fundamentada.
Resultado: NOT_VALIDATED até execução. CODE_COMPLETE != TASK_COMPLETE;
NO_EVIDENCE != PASS. N/A motivado não bloqueia. Nenhum REQUIRED pendente,
BLOCKED, REWORK, PARTIAL ou NOT_VALIDATED permite concluir a Task.

## Aceite e merge humanos
Decisão, responsável e evidência quando ocorrer; PASS não autoriza merge.
Deploy é outro gate e exige autorização humana separada.
- [ ] Registrar aceite humano observado, sem presumir aprovação.
- [ ] Registrar merge humano observado, somente quando autorizado e realizado.

## Riscos/Lacunas
Contexto insuficiente, validação não executada e decisões pendentes explícitas.

## Condições de parada
- mudança de arquitetura não aprovada
- expansão de escopo
- referência obrigatória ausente
- conflito entre fontes da verdade
- divergência entre card e JSON
- ação que exige nova autorização

## Prompt para o executor
Execute a TASK-XXX usando o contrato:
`docs/execution/TASK-XXX.json`

Leia primeiro `docs/execution/TASK-XXX.json`. Confirme `task_id`,
`contract_revision`. O Harness confere a equivalência normativa com a Issue e
fornece um prompt por lista de microtarefa, etapa ou setor, apontando para este
mesmo arquivo JSON e para o `list_id` correspondente em `execution_lists`.
O especialista verifica identidade da lista,
revisão e receipt do Harness sem ler a Task humana. Se houver divergência,
pare e reporte `human_task_json_divergence`. Para cada lista, carregue a skill
executora e somente as fontes, código e paths roteados no JSON. Execute apenas
o escopo aprovado, produza testes e receipts, e
publique os comentários materiais com URL/identificador, uso de tokens e
superfície alterada. Não faça merge nem deploy sem autorização humana explícita.

## Continuidade entre LLMs
- LLM executor atual:
- Estado de disponibilidade:
- Execution Contract: `docs/execution/TASK-XXX.json`
- `EXECUTION_HANDOFF`: obrigatório ao trocar de LLM

## Relatórios humanos na Issue
- Checkpoints materiais: DISCOVERY_SDD_COMPLETED | RUNNING | VALIDATING | REWORK | BLOCKED | COMPLETED
- Último status de publicação: PENDING | PUBLISHED | NOT PUBLISHED | N/A
- Evidência remota (URL/identificador):
- Motivo quando não publicado:
- Uso de tokens: input_tokens, output_tokens, total_tokens, measurement_source
- Superfície alterada: changed_files, mudanças na Issue/card, JSON/specs/fontes,
  remote_mutations, code_changed, branch, commit e PR

## Resultado da execução

### Resumo
O que foi feito.

### Arquivos alterados
Lista de arquivos criados/alterados/removidos.

### Comandos executados
Comandos de build/teste/lint executados.

### Resultado dos testes
Saída/resumo dos testes (passou/falhou, evidência).

### Bloqueios
Impedimentos encontrados.

### Observações
Notas adicionais, decisões tomadas e follow-ups.
