# Pull Request

> PR é a entrega revisável. Só é mergeado após review/QA aprovados.
> Deploy só acontece depois do PR aprovado.
> Selecionar somente checklists de setores REQUIRED, apontando receipt do owner.
> Nos demais, registrar N/A e motivo, sem exigir todos os especialistas por padrão.

## Task
Link da task (TASK-XXX) que originou este PR.

## Issue
Link da issue rastreada.

## Branch
Branch de origem -> branch de destino.

## Specs seguidas
Links das specs que este PR implementa (o contrato).

## O que foi feito
Resumo objetivo das mudanças.

## Fora do escopo respeitado
Confirmar que o que estava fora de escopo não foi alterado.

## Como testar
Passos para revisar/testar manualmente.

## Evidências
Screenshots, gravações, logs ou saídas que comprovam o resultado.

## Comandos executados
Build, testes, lint e migrações executados.

## Resultado dos testes
Resumo dos testes (passou/falhou) com evidência.

## Checklist de code review
- [ ] Código segue as specs e os critérios de aceite.
- [ ] Sem código fora do escopo da task.
- [ ] Nomes, padrões e estilo consistentes com o repositório.
- [ ] Sem segredos, tokens ou dados sensíveis versionados.
- [ ] Tratamento de erros adequado.
- [ ] Banco / API/Backend / Frontend/UI revisados separadamente.

## Checklist de QA
- [ ] QA funcional: receipt de qa-testing-standard quando requerido, ou N/A motivado.
- [ ] QA visual: telas conferem com o mockup aprovado (ui-ux-standard).
- [ ] Estados cobertos: loading, vazio, erro, sucesso, sem permissão.
- [ ] Responsividade e acessibilidade verificadas.

## Reconciliação dos setores
Link para matriz/ledger da Task. Todos REQUIRED precisam de owner, evidência e
receipts atuais; N/A exige motivo. Nenhum especialista atesta PASS de outro.
Planning, build ou código concluído não substituem QA final. Harness fecha seu
gate após todos os demais REQUIRED; aceite humano permanece separado.

## Checklist de segurança
- [ ] Authz/authn corretos (security-standard).
- [ ] Validação de input no servidor.
- [ ] Dados sensíveis protegidos e isolamento de tenant respeitado.
- [ ] Sem novas vulnerabilidades introduzidas.

## Riscos
Riscos desta entrega e plano de mitigação/rollback.

## Pendências
Itens conhecidos em aberto e follow-ups.
