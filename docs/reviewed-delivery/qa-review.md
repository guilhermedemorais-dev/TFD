> Contexto TFD · 767 palavras · 1639 tokens (o200k_base)

# QA independente — entrega revisada

**PASS** para `TFD-KNOWLEDGE-001`, spec e task revisão **4**, branch
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
