> Contexto TFD · 464 palavras · 1003 tokens (o200k_base)

# TFD-KNOWLEDGE-001 · Conhecimento seletivo e entrega de task revisada no TFD

Revisão 4 · draft

Agentes: abra o [JSON canônico](task.json) e execute somente sua rota e seus checklists.

## Problema

A preparação técnica exige pausas repetidas e o PASS de G6 não vincula estruturalmente o parecer à spec corrente.

## Solução

Preparar tasks tecnicamente revisadas com pesquisa seletiva e instruções por setor, preservando PRD interativo, evidências, economia de contexto e aprovação humana de cada fase implementada.

## Fases

- **P1 · Spec e revisão independente** · Arquitetura da manutenção
- **P2 · Política e implementação delimitadas** · harness, backend
- **P3 · QA e pacote de revisão humana** · qa

## Matriz por setor

| Setor | Dono | Aplicabilidade |
|---|---|---|
| database | `TFD-database` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [backend](#backend) | `TFD-backend` | REQUIRED |
| frontend | `TFD-frontend` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| ui_ux | `TFD-ui_ux` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [qa](#qa) | `TFD-qa_backend` | REQUIRED |
| security | `TFD-security` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| devops | `TFD-devops` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| observability | `TFD-observability` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| documentation | `TFD-documentation` | N/A · Sem mudança desse produto ou infraestrutura nesta manutenção. |
| [harness](#harness) | `TFD-harness` | REQUIRED |
| [Arquitetura da manutenção](#architecture) | `TFD-architecture` | REQUIRED |

<a id="backend"></a>
### backend

- **MT-03 · P2** Implementar preparação opt-in e vínculo do PASS · depende de MT-01
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Reproduzir falha antes de alterar o pipeline.
  - Testar complete permitido e proibido, autorização e atores.
  - Testar G6 com parecer válido, malformado, divergente ou stale.
  - Rejeitar task.spec ausente ou diferente de artifacts.spec mesmo com findings PASS válido e corrente.
  - Executar regressões preservando o modo manual.

[JSON](task.json) · `--sector backend`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="qa"></a>
### qa

- **MT-04 · P3** Verificar manutenção e consolidar evidência independente · depende de MT-02, MT-03
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Revisar requisitos e resultados na revisão entregue.
  - Executar checks e distinguir falha, limite e comportamento observado.
  - Verificar orçamento e registrar pendências para revisão humana.

[JSON](task.json) · `--sector qa`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="harness"></a>
### harness

- **MT-02 · P2** Integrar instruções e pesquisa compartilhada · depende de MT-01
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Preservar conhecimento existente e responsabilidades por setor.
  - Manter PRD interativo e leituras obrigatórias.
  - Medir orçamento das skills e referências sem alegar economia executada.

[JSON](task.json) · `--sector harness`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

<a id="architecture"></a>
### Arquitetura da manutenção

- **MT-01 · P1** Especificar contratos e preparar task canônica · depende de livre
  - ☐ Aprovado · ☐ Reprovado · Aguardando QA
  - Ler schema, implementação e testes existentes.
  - Documentar requisitos, compatibilidade e casos negativos.
  - Validar e enviar a revisão exata a QA spec.

[JSON](task.json) · `--sector architecture`
Feito: pendente · Bloqueios: a verificar · Tokens reais: indisponíveis

Escopo, aceite e testes no contrato JSON desta task.
