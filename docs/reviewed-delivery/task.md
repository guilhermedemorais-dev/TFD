> Contexto TFD · 1183 palavras · 2553 tokens (o200k_base)

# TFD-KNOWLEDGE-001 · Conhecimento seletivo e entrega de task revisada no TFD

Revisão 6 · draft

Coordenação: o agente principal usa a skill `TFD-harness` para coordenar e delegar as MTs conforme dependências, escopo e gates.
No Codex, o subagente `tfd_harness` é apenas de consulta/status; a delegação cabe ao agente principal.

Loop de implementação: execução e autotestes → QA independente → correções e nova revisão → PASS → aprovação humana.

Agentes: abra o [JSON canônico](task.json) e execute somente sua rota e seus checklists.

## Problema

A preparação técnica exige pausas repetidas e o PASS de G6 não vincula estruturalmente o parecer à spec corrente.

## Solução

Preparar tasks tecnicamente revisadas com pesquisa seletiva e instruções por setor, preservando PRD interativo, evidências, economia de contexto e aprovação humana de cada fase implementada.

<a id="limites-globais"></a>
## Limites globais

Fora do escopo: Novo schema de Task, novo motor de conhecimento ou novos agentes.; Instalar ou executar ferramentas do repositório MatthewKerns; importar suas instruções globais.; Alterar os projetos clientes, promover conhecimento privado ao plugin ou editar o checkout original.; Publicação remota, merge, deploy e remoção de aprovação humana do PRD ou da implementação.
Caminhos protegidos: `schemas/**`, `integrations/graphify/**`, `scripts/install*`, `library/plugins/**`

## Fases

- **P1 · Spec e revisão independente** · Arquitetura da manutenção
- **P2 · Política e implementação delimitadas** · harness, backend
- **P3 · QA e pacote de revisão humana** · qa

## Matriz por setor

| Setor | Dono | Aplicabilidade |
|---|---|---|
| [harness](#harness) | `TFD-harness` | REQUIRED |
| database | `TFD-database` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [backend](#backend) | `TFD-backend` | REQUIRED |
| frontend | `TFD-frontend` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| ui_ux | `TFD-ui_ux` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [qa](#qa) | `TFD-qa_backend` | REQUIRED |
| security | `TFD-security` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| devops | `TFD-devops` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| observability | `TFD-observability` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| documentation | `TFD-documentation` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [Arquitetura da manutenção](#architecture) | `TFD-architecture` | REQUIRED |

<a id="harness"></a>
### harness

- **MT-02 · P2** Integrar instruções e pesquisa compartilhada · depende de MT-01
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Responsável: `@TFD-harness` · Validador independente: `@TFD-qa_spec`
  - Caminhos permitidos: `README.md`, `docs/00-arquitetura.md`, `docs/sector-task.md`, `library/architecture/technical-decision-procedure.md`, `library/indexes/resources.json`, `skills/TFD-architecture/SKILL.md`, `skills/TFD-backend/SKILL.md`, `skills/TFD-database/SKILL.md`, `skills/TFD-devops/SKILL.md`, `skills/TFD-discovery/SKILL.md`, `skills/TFD-documentation/SKILL.md`, `skills/TFD-frontend/SKILL.md`, `skills/TFD-harness/SKILL.md`, `skills/TFD-harness/references/gates.md`, `skills/TFD-product/SKILL.md`, `skills/TFD-qa_backend/SKILL.md`, `skills/TFD-qa_spec/SKILL.md`, `skills/TFD-qa_spec/references/review-checklist.md`, `skills/TFD-qa_ui/SKILL.md`, `skills/TFD-security/SKILL.md`, `skills/TFD-ui_ux/SKILL.md`, `tests/test_discovery_skill.py`, `tests/test_qa_spec_skill.py`, `tests/test_product_skill.py`
  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.
    - Preservar conhecimento existente e responsabilidades por setor.
    - Manter PRD interativo e leituras obrigatórias.
    - Medir orçamento das skills e referências sem alegar economia executada.
  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).
  - Resultado esperado: library/architecture/technical-decision-procedure.md; skills/TFD-harness/references/gates.md; library/indexes/resources.json
  - Concluído quando: Instrucoes e biblioteca preservadas, PRD interativo e pesquisa delimitada; limites de contexto medidos e restricoes documentadas.

[JSON](task.json) · `--sector harness`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="backend"></a>
### backend

- **MT-03 · P2** Implementar preparação opt-in e vínculo do PASS · depende de MT-01
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Responsável: `@TFD-backend` · Validador independente: `@TFD-qa_backend`
  - Caminhos permitidos: `scripts/pipeline.py`, `tests/test_pipeline.py`, `tests/test_reviewed_delivery.py`
  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.
    - Reproduzir falha antes de alterar o pipeline.
    - Testar complete permitido e proibido, autorização e atores.
    - Testar G6 com parecer válido, malformado, divergente ou stale.
    - Rejeitar task.spec ausente ou diferente de artifacts.spec mesmo com findings PASS válido e corrente.
    - Executar regressões preservando o modo manual.
  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).
  - Resultado esperado: scripts/pipeline.py; tests/test_pipeline.py; tests/test_reviewed_delivery.py
  - Concluído quando: Regressoes do modo manual, preparacao opt-in e vinculo do PASS em G6 aprovadas com comandos e exits observados.
- **MT-05 · P2** Explicitar agentes, limites e resultados de cada microtarefa · depende de MT-01
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Responsável: `@TFD-backend` · Validador independente: `@TFD-qa_backend`
  - Caminhos permitidos: `scripts/render_task.py`, `tests/test_mt_handoff.py`
  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.
    - Derivar @owner e @validator literais dos campos canonicos, sem invocar agentes.
    - Expor checklist, caminhos permitidos e negacao de trabalho fora do escopo ou sem gate.
    - Mostrar entregaveis e condicao de conclusao especifica de cada MT.
    - Exibir exclusoes e caminhos protegidos globais uma vez e vincular cada MT.
    - Preservar tasks legadas, recibos, checkboxes e JSON roteado por setor.
    - Explicitar coordenacao pelo agente principal no cabecalho e mostrar harness primeiro, preservando dependencias e loop de QA.
  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).
  - Resultado esperado: scripts/render_task.py; tests/test_mt_handoff.py
  - Concluído quando: Cada MT apresenta responsavel, limites, entregaveis, conclusao e validador; testes do formato atual e legado passam e o JSON roteado permanece equivalente.

[JSON](task.json) · `--sector backend`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="qa"></a>
### qa

- **MT-04 · P3** Verificar manutenção e consolidar evidência independente · depende de MT-02, MT-03, MT-05
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Responsável: `@TFD-qa_backend` · Validador independente: `@TFD-harness`
  - Caminhos permitidos: `docs/reviewed-delivery/qa-review.md`, `docs/reviewed-delivery/verification.md`, `docs/reviewed-delivery/context-budget.json`
  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.
    - Revisar requisitos e resultados na revisão entregue.
    - Executar checks e distinguir falha, limite e comportamento observado.
    - Verificar orçamento e registrar pendências para revisão humana.
  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).
  - Resultado esperado: docs/reviewed-delivery/qa-review.md; docs/reviewed-delivery/verification.md; docs/reviewed-delivery/context-budget.json
  - Concluído quando: Criterios da revisao entregue verificados independentemente; parecer PASS ou bloqueios/rework acionaveis com comandos, exits e limites.

[JSON](task.json) · `--sector qa`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="architecture"></a>
### Arquitetura da manutenção

- **MT-01 · P1** Especificar contratos e preparar task canônica · depende de livre
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Responsável: `@TFD-architecture` · Validador independente: `@TFD-qa_spec`
  - Caminhos permitidos: `docs/reviewed-delivery/README.md`, `docs/reviewed-delivery/task.json`, `docs/reviewed-delivery/task.md`
  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.
    - Ler schema, implementação e testes existentes.
    - Documentar requisitos, compatibilidade e casos negativos.
    - Validar e enviar a revisão exata a QA spec.
  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).
  - Resultado esperado: docs/reviewed-delivery/README.md; docs/reviewed-delivery/task.json; docs/reviewed-delivery/task.md
  - Concluído quando: Spec e Task da revisao atual validas, view equivalente ao JSON e parecer independente de spec para essa revisao.

[JSON](task.json) · `--sector architecture`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

Escopo, aceite e testes no contrato JSON desta task.
