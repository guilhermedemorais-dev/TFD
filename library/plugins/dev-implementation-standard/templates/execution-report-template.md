# Execution Report: TASK-XXX

> Preenchido pelo executor (dev-implementation-standard) e copiado para a seção
> "Resultado da execução" da task. Evidência é obrigatória para concluir.

## Status e rastreabilidade
- Status visual atual: [🟡 Em andamento | 🔴 Bloqueada | 🟢 Concluída]
- Status Kanban atual: [Backlog | Discovery / SDD | Ready for Dev | In Progress | Validation | In Review | Awaiting Final Approval | Done]
- Data/hora de início:
- Data/hora de conclusão:
- Executor:
- Task:
- Issue criada / vinculada:
- Branch:
- Responsável:
- Pronto para GitHub Projects: sim/não

## Referências
- Setor e fase executados:
- Revisão/artefato validado:
- sources_loaded: paths e propósito efetivamente usado
- conditional_sources_loaded: paths e condição observada
- validation_scope: cobertura e limites do setor
- Execution Contract utilizado:
- Specs obrigatórias seguidas:
- Docs obrigatórios seguidos:
- Arquivos/módulos permitidos:

## Prompt utilizado
Registre o bootstrap curto (`task_id` + `execution_contract_path`). Não copie o
conteúdo integral da task ou das specs.

## Skills aplicadas
Cole o `SKILL_RECEIPT` de cada skill e referência obrigatória.

## Inventário de reutilização
Cole o `REUSE_INVENTORY`, incluindo buscas, candidatos existentes, call sites e
a decisão `REUSE | EXTEND | REPLACE | CREATE`.

## Gate de código mínimo
Cole o `MINIMAL_CODE_GATE` com justificativa para cada nova abstração e
duplicações removidas ou explicitamente mantidas.

## Continuidade entre LLMs
- LLMs executores utilizados:
- Troca de LLM ocorrida: sim/não
- `EXECUTION_HANDOFF` utilizado: sim/não/N/A
- Execution Contract retomado:
- Motivo e checkpoint de continuidade:

## Relatório humano na Issue
- Checkpoints materiais reportados:
- Issue vinculada:
- Status de publicação: PUBLISHED | NOT PUBLISHED | N/A
- Evidência remota (URL/identificador retornado):
- Motivo quando não publicado:
- Último corpo idêntico verificado para evitar duplicação: sim/não/N/A

## Checklist executado
- [ ] Contrato validado e referências necessárias carregadas
- [ ] Skills obrigatórias carregadas
- [ ] Inventário de reutilização
- [ ] Gate de código mínimo
- [ ] Implementação
- [ ] Testes
- [ ] Validação
- [ ] Atualização do relatório
- [ ] Relatório humano preparado/publicado ou fallback registrado
- [ ] Handoff para review

## Resumo
O que foi implementado, em uma a três frases.

## Escopo respeitado
- [ ] Apenas o escopo da task foi implementado.
- [ ] Nada fora do escopo foi alterado.
- [ ] Nenhuma mudança de arquitetura sem aprovação.

## Arquivos alterados
Lista de arquivos criados / alterados / removidos.

## Evidências
Comandos, prints, logs, links de CI, screenshots ou saídas relevantes.

## Resultado detalhado por camada

Preencher somente resultados próprios. Demais setores apontam receipts dos
respectivos owners ou NOT_VALIDATED; nunca certificar outro especialista.
Harness consolida o ledger e o estado global da Task.

### Banco
Migrações, schema, seeds, queries, dados afetados ou `N/A`.

### API/Backend
Endpoints, serviços, validações, contratos, jobs, integrações ou `N/A`.

### Frontend/UI
Telas, componentes, estados visuais, responsividade, acessibilidade ou `N/A`.

### Validação
Testes automatizados, TDD quando aplicável, validação manual com evidência quando TDD completo não for viável, lint, build, checagens manuais e resultado de cada validação.

### Riscos/Lacunas
Riscos restantes, lacunas não resolvidas, limitações e follow-ups.

## Comandos executados
Build, lint, testes, migrações e validações executadas.

## Resultado dos testes
Saída/resumo (passou/falhou) com evidência. Se não houve teste automatizado, registrar validação manual e justificativa.

## Critérios de aceite
- [ ] Todos os critérios de aceite da task atendidos (listar item a item).

## Alterações fora do escopo
Deve ser `N/A`. Se não for `N/A`, a execução deveria ter parado e registrado bloqueio.

## Bloqueios
Impedimentos encontrados, status visual aplicado e a quem foi escalado.

## Observações
Decisões tomadas, follow-ups e pontos de atenção para o review.

## PR / Review
Link do PR ou pacote de review preparado (task, issue, branch e specs vinculados).
