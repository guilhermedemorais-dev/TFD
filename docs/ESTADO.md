> Contexto TFD · 1284 palavras · 2117 tokens (o200k_base)

# Estado do TFD

Estado do plugin e registros de verificação para retomar o trabalho.

## Retomada rápida

**Versão do pacote.** TFD `0.1.6` para o Codex, conforme o [manifesto](../.codex-plugin/plugin.json).
A revisão distribuída depende do canal. O [histórico](CHANGELOG.md) identifica
os commits e o [instalador](GUIA-CODEX.md#canal-de-revisão) consulta o GitHub.

- **Disponível no canal de revisão.** Harness, task JSON por módulo, subagentes nativos, Tradutor, retomada por item, roteamento opcional e verificação de caminhos. O medidor separa tokens de entrada nova, cache e saída da ocupação da janela. A compactação automática é uma configuração opcional do Codex.
- **Complementar.** Oficina `0.1.1` faz auditoria e manutenção autorizada e tem instalação própria. Candidatos externos servem de referência para adaptações locais ao padrão TFD.
- **Em validação.** As verificações do plugin cobrem os contratos e cenários locais. A aceitação ponta a ponta de um projeto depende das evidências e aprovações daquele projeto.
- **Instalação.** O [guia](GUIA-CODEX.md) cobre Windows e Linux. O catálogo instalado exclui `tests/`. Os arquivos de teste continuam disponíveis no repositório para manutenção.

**Graphify.** O adaptador do bundle TFD inclui consulta nativa em Python no
Windows, runtime isolado para extração e fallback lexical sem reconstrução
automática. Seu índice cobre arquivos selecionados do bundle. Os achados de Discovery
de cada projeto são consultados no próprio projeto. [Verificação local](receipts/2026-11-09-graphify.md)

Para retomar, abra um chat novo na pasta do TFD, leia esta seção e execute apenas o próximo pedido do usuário.

## Método e fontes

Os contratos de entrega ficam na [arquitetura](00-arquitetura.md) e nas
skills do TFD. A biblioteca usada no Discovery fica em `library/`.
Os artigos científicos e a documentação oficial estão agrupados pelas
decisões que informam. [Fundamentos e fontes](00-arquitetura.md#fundamentos-e-fontes)

## Decisões de arquitetura

1. Nome: **The Factory Developer (TFD)**. Prefixo `TFD-` em agentes e skills.
2. O núcleo é independente do host. O adaptador em `hosts/codex/` resolve o perfil do Codex.
3. Plugin = método; projeto = conhecimento. Nada de artefato de cliente no plugin.
4. 13 setores, incluindo `qa_spec`, `qa_backend`, `qa_ui` e `documentation`.
5. Quem executa não aprova o próprio trabalho.
6. QA registra achados na revisão atual. Após três submissões de correção no gate, novo `REWORK` bloqueia a etapa.
7. Engenharia reversa e afins são plugins complementares, por catálogo.
8. `oficina` é plugin separado de manutenção, fora do pipeline, para o fim.
9. Referência não é clone: código novo, melhor quando possível.
10. Prazo: faixa e confiança, nunca data cravada no PRD.

## Etapas

| Etapa | Entrega | Estado |
|---|---|---|
| 0 | Arquitetura | aprovada |
| 1 | Núcleo: schemas, validadores, padrão de skills e CLI | implementado e coberto por testes locais |
| 2 | 13 setores | instruções e contratos de agente disponíveis para os 13 setores |
| 3 | Procedimentos | harness, autoria da spec, revisão e entregas por etapa disponíveis para execução guiada no host |
| 4 | Evidência e gates | CLI local verifica ordem, arquivos e hashes, revisão atual, rework e aprovação registrada |
| 5 | Plugin `oficina` | implementado em repositório separado, com auditoria, detector e verificação de manutenção |
| 6 | Instalação por host | Adaptador Codex disponível com guia para Windows e Linux |

## Núcleo disponível

- `scripts/validate_task.py` valida o contrato. Exige `gates`, verifica os vínculos entre requisitos, microtasks, aceites e testes, e rejeita ciclos e microtasks em que o autor é o próprio validador.
- `scripts/validate_estimate.py` valida o arquivo de estimativa por fase. Confere a ordem das horas e a data de calendário. A estimativa dentro da task usa a mesma regra de ordem.
- `scripts/tfd.py` oferece `plan`, `check` e `report`. O `check` executa testes e grava um recibo. Se o Git falhar ao levantar os caminhos alterados, o recibo registra que o escopo não foi verificado.
- `scripts/pipeline.py` verifica o log local do módulo. Ele indica o gate e a ação pendente. O host executa as ações e o usuário decide a aprovação. O [adaptador Codex](../hosts/codex/README.md) está disponível. O catálogo de complementares e os demais adaptadores seguem planejados.
- `scripts/resume_task.py` recupera o gate e o próximo item executável quando há uma task setorizada aprovada. `scripts/model_router.py` seleciona perfis autorizados e verifica observações do host em projetos que adotam roteamento.
- `scripts/token_usage.py` gera recibos de consumo real reportado pelo Codex
  por task, etapa e tentativa. Suporta eventos JSONL do CLI e turnos do
  Desktop. O CI e suas instruções específicas pertencem ao repositório do
  projeto. Veja a [coleta e o handoff de CI](../hosts/codex/README.md#token-receipts).

Para rodar a suíte local a partir da raiz do TFD, use `python -B -m unittest discover -s tests`.

## Fluxo em uso

O Discovery consulta o índice da biblioteca local do TFD em
`library/indexes/resources.json`,
registra as evidências no projeto e volta à pesquisa quando o QA aponta uma
lacuna na spec. O harness conduz o módulo no host e usa o CLI para validar
as transições registradas.

### Prompts e REA

- Os prompts ativos de Product, Discovery, QA de spec e retomada estão em
  inglês. Aplicamos compressão manual na autoria: remover repetição, manter
  regras e evidências, e consultar referências sob demanda. A execução usa
  os prompts revisados diretamente. [LLMLingua, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.825/)
- Medição do `SKILL.md` de QA de spec, da versão 1.1.0 para 1.2.0:
  990 → 435 tokens (−56,1%), com `tiktoken 0.14.0` e `o200k_base`.
  A contagem cobre o arquivo inteiro. A suíte local verifica estrutura e
  roteamento estático; a execução das regras no host é uma checagem separada.
- A ausência de software de referência pode ser registrada e não bloqueia G1.
  No Discovery, identifique o tipo de projeto. Se a engenharia reversa ajudar,
  pergunte se o usuário autoriza o REA e qual variante usar para aquele tipo.
  Confirme alvo e escopo antes de chamar. A pesquisa independente pode seguir.
  A integração de variantes fica nos plugins complementares.

O aceite da validação em projeto real depende do registro da execução e das
aprovações humanas no projeto.

### Registros históricos de verificação dos setores e gates

- `python -B -m unittest discover -s tests`: 64 testes, exit 0.
- `python -B scripts/pipeline.py examples/workflow.example.json`: exit 0, aguardando a constituição em G0.
- Codex CLI efêmero, com as skills fornecidas como entrada: autoria de spec fictícia de estoque, decisões dos setores e harness, e revisão independente. O QA devolveu a spec HTTP por lacunas de contrato e testabilidade. A revisão corrigiu o cálculo de p95 e continuou bloqueada pelo OpenAPI ausente. O reteste do QA retornou REWORK para o contrato ausente e PASS para uma spec de função isolada com evidência suficiente. Os dois JSONs finais passaram no validador.
- No teste da versão `0.1.0`, o Codex CLI instalou `the-factory-developer@tfd-local` e `codex debug prompt-input` confirmou 14 skills. O helper de shell daquela sessão falhou ao abrir a skill instalada.

### Tradutor

- O harness usa `tfd-translator` antes de delegar. O repasse fica em inglês, com resposta ao usuário em português do Brasil.
- `python -B -m unittest discover -s tests` passou 74 testes, saída 0. No Codex CLI efêmero, com a skill fornecida na entrada, passaram três casos fictícios. O repasse preservou a correção de caminho, a cópia literal e a exigência de aprovação. O pedido ambíguo gerou uma pergunta em português. A pergunta geral ficou fora do fluxo.
- O teste conjunto registrou 25.204 tokens de entrada e 172 de saída. A medição inclui o contexto do host. A execução pela instalação nativa e a comparação de custo total com e sem Tradutor continuam pendentes.

## Próximas verificações

- Validar outros provedores com os requisitos e permissões do projeto que adotar roteamento.
- Medir recuperação de contexto e qualidade em tarefas representativas antes de expandir o índice para código de projeto.
- Registrar resultados ponta a ponta nos projetos que adotarem o quadro por fases.
