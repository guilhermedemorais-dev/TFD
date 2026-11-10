> Contexto TFD · 1132 palavras · 2445 tokens (o200k_base)

# QA independente — entrega revisada

**PASS histórico — revisão 4** para `TFD-KNOWLEDGE-001`, branch
`office/reviewed-delivery`, base `38197b7730c9925207f1aea01c615e04daf23209`.
Revisor: agente nativo `qa_reviewed_implementation` / `TFD-qa_backend`, distinto
dos autores. Nenhum arquivo de implementação foi editado pelo revisor.

A rota canônica é `qa / MT-04`, cujo owner é `TFD-qa_backend`; o identificador
legado `qa` foi preservado. O recorte medido tinha 1.985 tokens. Foram lidas
integralmente as quatro referências obrigatórias, a skill ativa, as 14 skills
alteradas, o pipeline e suas regressões. A consulta Graphify retornou
`INDEX_STALE`, exit 0; a revisão usou fontes canônicas por leitura local,
sem reconstruir o índice.

## Evidência executada

Python usado: `C:/Users/teste/Documents/deepseek-harness/default-workspace/.venv-tfd/Scripts/python.exe`.
Comandos relativos à raiz desta worktree.

| Verificação | Resultado observado |
|---|---|
| `python -B -m unittest discover -s tests` | exit 0; **150 testes**, 6,659 s |
| `python -B scripts/render_task.py docs/reviewed-delivery/task.json --sector qa --microtask MT-04 --measure` | exit 0; rota resolvida |
| Script independente em memória: `validate_task`, `markdown_body == render_task`, revisão/path do parecer | exit 0; task/view/PASS revisão 4 correspondem |
| Script independente: medidas `o200k_base`, hashes dos 109 recursos e comparação com `git show HEAD:library/indexes/resources.json` | exit 0; biblioteca preservada, apenas SHA do procedimento atualizado |
| CLI real `scripts/pipeline.py <workflow-temporário> --project-root <projeto-temporário>` | quatro checkpoints abaixo, todos conforme esperado |

O CLI real chegou a G6 `AWAITING_SUBMISSION` com exit 0; após PASS estruturado,
permaneceu em `AWAITING_APPROVAL`, exit 0. Alterar somente a revisão do findings
para uma antiga gerou exit 1 com rejeição explícita. Um parecer backend BLOCKED
em G7 retornou exit 2 e reteve os demais revisores pendentes. Fixtures descartáveis
reutilizaram somente a preparação dos testes; os estados/exit codes foram
checados por chamadas independentes ao processo do CLI.

Um primeiro comparador auxiliar do revisor leu UTF-8 com o padrão CP1252 do
Windows e falhou com exit 1. O diagnóstico mostrou um falso positivo de metadados;
a repetição com `encoding='utf-8'` passou, sem alteração do produto.

## Critérios de aceite

| Critério | Evidência / conclusão |
|---|---|
| AC-01 | Product conserva perguntas de negócio pendentes, reaproveita respostas e não aprova G1; leitura integral e cenário de briefing. |
| AC-02 | As 14 skills têm responsabilidades específicas, link único para pesquisa compartilhada, até 150 linhas e descrições até 60 palavras. |
| AC-03 | Procedimento compartilhado aplica pesquisa também em design, implementação e QA; registra pergunta, dono, versão, decisões e limites no projeto. |
| AC-04 | Fontes obrigatórias sobrevivem a falha do grafo. MatthewKerns permanece URL externa, sem conteúdo vendorizado ou indexado. |
| AC-05/06 | Regressões cobrem opt-in fechado, autorização vazia/ausente/insegura, complete antecipado/stale, atores normalizados e gates proibidos; modo manual passa. |
| AC-07 | Regressões e CLI rejeitam texto/JSON inválido, verdict/path/revisão divergentes e task.spec ausente/diferente; PASS válido ainda aguarda humano. |
| AC-08 | Regressões preservam QA aplicável, reinício dos pareceres após rework, três substituições e aprovação humana de G6/G7/G8. |
| AC-09 | Referências compartilhadas, incluindo cabeçalho: procedimento 972 tokens; gates 991. Inventário das 14 skills: 4.458 tokens; carrega-se somente o setor ativo. |
| AC-10 | Schema existente válido, view regenerada equivalente e parecer de spec PASS revisão 4 verificados. |

## Cenários manuais de pesquisa

1. **PRD:** uma regra comercial não respondida retorna ao usuário; uma dúvida
   sobre comportamento técnico segue para Discovery. Product e procedimento
   compartilhado mantêm essa distinção sem inventar requisito.
2. **Arquitetura/backend:** diante de uma orientação de paralelismo de agentes,
   a pesquisa pode consultar capítulo externo fora de uma lista fixa de conceitos.
   Foram abertos na origem, somente em memória, LICENSE, COVERAGE_STANDARDS e
   PARALLEL_EXECUTION_PATTERNS na revisão `efdec594ac403754baea2bb04952dd1d68da35c7`.
   A licença MIT foi confirmada; o exemplo de cobertura deixa `return False`
   sem execução, e o conselho de paralelismo usa “ALWAYS” sem demonstrar isolamento.
   As ressalvas do procedimento são pertinentes; nenhuma ferramenta externa rodou.
3. **QA:** dúvida sobre efeitos de retry/webhook pode voltar à pesquisa e ao
   autor; o roteador técnico e a referência `technical-apis-jobs.md` exigem
   distinção entre ACK e efeito de negócio, duplicação e evidência real. O checklist
   de QA impede representar plano de teste como execução; o novo pipeline exige
   revisão atual após rework antes de liberar a etapa.

Esses cenários validam coerência das instruções por análise manual com fontes
reais; não constituem prova de seleção automática pelo host ou entrega autônoma
de uma aplicação cliente. Economia real de tokens permanece **NOT VALIDATED**.
O CLI verifica registros e separação dos atores declarados; não autentica pessoas.
Merge, deploy, publicação e atualização do cache instalado não fizeram parte do QA.

## Snapshot revisado

| Arquivo | SHA-256 |
|---|---|
| `scripts/pipeline.py` | `81e9969d9b753276d64b600a9b9a7c76d50b419775587ca243d4b255db782325` |
| `tests/test_reviewed_delivery.py` | `7086f39bb33eb2810575692821fd48f8dece4032764cb3fb2d9748a7628f7e3a` |
| `docs/reviewed-delivery/README.md` | `ed761ba8b2ff7f718b96a4e755a3ca5f0083cfe57511eed2e61fa997b17b758e` |
| `docs/reviewed-delivery/task.json` | `63aa296943e0dac1c63033106d3169a9527ac2cbc3bb3d70f3f8e30a72320221` |
| `docs/reviewed-delivery/task.md` | `56d6bc3bf296ff57539c7c8723aad9ae9939d1081e457823d5a24543ac07f077` |

Nenhum achado bloqueador ou major permanece aberto neste escopo. Este PASS é
técnico; a decisão humana de aceitar a entrega continua pendente.

## Adendo histórico — revisão 5 (INC-002)

**PASS independente — spec e task revisão 5.** O parecer da revisão 4 acima é
histórico; não foi reutilizado para aprovar a nova view. Autoria do renderer e
novos testes: coordenador; revisão independente: `qa_reviewed_implementation`.

AC-11: revisão do código, das views setorizada/legada e dos quatro novos testes
confirma que cada MT deriva `@owner` e `@validator` literais, checklist/caminhos
permitidos, proibições, resultados e condição específica de conclusão. Menções
não invocam agentes nem convertem aliases desconhecidos. “Pode” permanece
condicionado aos limites globais e ao gate; caminhos protegidos prevalecem.
Exclusões e proteção aparecem uma vez, sob âncora referenciada pelas MTs.
Checkboxes e pareceres PASS/REWORK/BLOCKED continuam preservados.

Verificação executada nesta revisão:

- `python -B -m unittest discover -s tests`: **exit 0; 154 testes; 7,304 s**.
- Comparador independente em memória, renderer da base `d134c38` versus atual,
  com a mesma Task revisão 5: **exit 0; cinco rotas JSON literalmente iguais**.
  View humana: **1.157 → 2.441 tokens** `o200k_base`; maior clareza visual,
  sem redução de contexto obrigatório nem alegação de economia real.
- `validate_task`, comparação view/render e vínculo do parecer de spec:
  **exit 0; revisão 5 válida e correspondente; zero campos de schema novos**.

Snapshot SHA-256: renderer `fff2b2db4a54313b364d3cc551f054a7d86a76158cf5fe0a78da609dca4f9e50`;
novos testes `e213df5bf3f724fc0198df0128279851657982d23d68381a8a43fe8d3c8916df`;
task `67f531066b3bd25cb43fdf675a453181ee81360244e54830a4582547e8e33f72`.
Nenhum achado bloqueador/major aberto. Aprovação humana, instalação e limites
NOT VALIDATED de runtime/host permanecem; sem merge ou deploy nesta verificação.


## Adendo atual — revisão 6

**PASS independente — revisão 6**, rota `qa / MT-04`, revisor
`header_runtime_qa` / `TFD-qa_backend`, distinto do autor. Os pareceres anteriores
permanecem históricos. Escopo: cabeçalho e ordenação visual, AC-10/AC-11.

`python -B -m unittest tests.test_mt_handoff tests.test_schemas tests.test_pipeline tests.test_reviewed_delivery`:
**exit 0; 53 testes; 1,592 s**, incluindo seis testes de handoff.
Comparador independente em memória com `validate_task`, `render_task` e
`sector_context`: **exit 0**; Task/view equivalentes na revisão 6, cinco rotas
inalteradas antes/depois da renderização, ausência de mutação, fases P1/P2/P3 e
dependências preservadas. Parecer de spec corrente: PASS, revisão 6.

Leitura confirma agente principal usando `TFD-harness`, subagente nativo
`tfd_harness` restrito a consulta/status, harness primeiro na matriz/seções e
loop autotestes → QA independente → correções/nova revisão → PASS → aprovação
humana. Nenhum achado bloqueador neste recorte. Implementação/testes não foram
editados pelo revisor. Aprovação humana permanece pendente; sem merge ou deploy.
