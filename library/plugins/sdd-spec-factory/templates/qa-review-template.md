# QA Review: TASK-XXX / PR #YY

> Owner qa-testing-standard: valida comportamento independentemente da implementação.
> UI/UX, Security e DevOps atestam seus próprios setores; QA não fabrica seu PASS.

## Referências
- Execution Contract, setor qa, fase planning ou validation:
- Revisão/artefato e receipts das dependências:
- Task:
- PR:
- Seções roteadas da Task e critérios globais relevantes:
- Fontes REQUIRED: path/link + propósito
- Fontes CONDITIONAL: path/link + condição + propósito; ativada? evidência?
- Fontes OPTIONAL consultadas: motivo; nenhuma carga automática
- SKILL_RECEIPT:
- Mockups aprovados (ui-ux-standard): somente quando houver UI aplicável

## Ambiente testado
Branch, build, URL/ambiente e dados de teste usados.

## QA funcional
Selecionar somente cenários aplicáveis ao contrato: fluxo principal, negativo,
limite, estados, timeout/retry, idempotência, concorrência e regressão. Escolher
o menor nível suficiente de teste; não impor E2E ou checklist completo.
- QA_GUARDRAILS:
- TEST_SCENARIOS:
- REGRESSION_TARGETS:
- VALIDATION_REQUIREMENTS:
Planning produz cenários, não PASS da implementação.

| Cenário requerido | Esperado | Observado | Evidência | Resultado |
| --- | --- | --- | --- | --- |
| preencher | conforme fonte | somente após execução | link | NOT_VALIDATED |

## QA visual
Referenciar resultado do owner ui-ux-standard quando requerido. QA pode testar
fluxos/formulários/erros, sem substituir revisão visual ou de acessibilidade.

## Testes automatizados
- [ ] Suíte executada.
- [ ] Cobertura mínima atendida.
- Resultado:
Comando, exit code e artefato; separar PRODUCT_BUG, TEST_BUG,
ENVIRONMENT_FAILURE, FLAKY_TEST e TOOL_FAILURE. Não executado nunca é PASS.

## Segurança (gate)
Possível abuso vira SECURITY_CANDIDATE para security-standard. Referenciar seu
receipt quando requerido; QA não confirma vulnerabilidade nem severidade Security.

## Observabilidade
Conferir comportamento observável requerido e referenciar owner de operação
quando aplicável; healthcheck DevOps não é prova do fluxo funcional.

## Evidências
Screenshots, vídeos, logs e saídas de teste.

## Bugs encontrados
Para cada candidato: esperado, atual, reprodução, ambiente, revisão, evidência,
impacto e reprodutibilidade. Usar template do owner QA. CONFIRMED_BUG solicita
REWORK à Implementation; QA não corrige produto silenciosamente.
Fix exige reteste na revisão corrigida e regressão quando viável.

## Resultado
QA_STATUS: PASS | PARTIAL | BLOCKED | NOT_VALIDATED.
EXECUTION_RECEIPT existente: setor/fase/fontes/revisão/escopo, bugs/disposição,
regressões/retestes e limitações. Não criar outro tipo de receipt.

## Justificativa
PASS exige todos os casos obrigatórios executados/aprovados, bugs bloqueantes
resolvidos, regressões verificadas e limitações registradas. Não significa
software sem bugs nem aceite humano. Mudança material exige revisar/retestar
evidências afetadas. Motivo objetivo e próximos passos quando incompleto.
