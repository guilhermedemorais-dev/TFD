# Code Review: TASK-XXX / PR #YY

> Review é aprovação ou reprovação técnica do PR.
> Merge/Deploy só ocorre após review aprovado.

## Referências
- Task:
- PR:
- Specs seguidas:

## Resumo da mudança
O que o revisor entendeu que foi entregue.

## Aderência às specs
- [ ] Implementa o que a spec define (o contrato).
- [ ] Atende todos os critérios de aceite da task.
- [ ] Não foge do escopo nem altera o que estava fora do escopo.

## Qualidade de código
- [ ] Legível e consistente com o repositório.
- [ ] Sem duplicação desnecessária e sem código morto.
- [ ] Tratamento de erros e casos de borda.
- [ ] Sem segredos/tokens/dados sensíveis versionados.

## Por camada
- **Banco:** revisado (migração/rollback/índices) ou `N/A`.
- **API/Backend:** contratos, status, validação de input ou `N/A`.
- **Frontend/UI:** estados, acessibilidade, responsividade ou `N/A`.

## Testes
Conferir Sector Validation Matrix: todos REQUIRED têm receipt atual do owner,
N/A tem motivo, QA independente quando obrigatório. Code review não fabrica
PASS de UI/Security/DevOps/QA; Harness reconcilia todos os setores.

- [ ] Testes existem e cobrem o comportamento esperado.
- [ ] Suíte passa localmente/CI.
- Evidência:

## Segurança
- [ ] Sem nova superfície de risco; encaminhado a security-standard quando aplicável.

## Observabilidade
- [ ] Logs/métricas adequados.

## Comentários
Pontos a corrigir (bloqueantes) e sugestões (não bloqueantes).

## Resultado
APROVADO | APROVADO COM RESSALVAS | REPROVADO

## Justificativa
Motivo objetivo da decisão.
