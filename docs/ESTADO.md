# Estado do TFD

Atualizado em 2026-11-05. Este arquivo é a fonte de verdade para retomar em outro chat.

## Retomada rápida

**Base do aviso de contexto:** `9c18914`. **Host:** TFD `0.1.6` no perfil local do Codex. A suíte passou 78 testes com saída `0`.

- **Pronto.** Harness, task única por módulo com JSON canônico e visão humana, subagentes nativos e Tradutor. Token Usage usa o Python para separar consumo acumulado da janela de contexto e indica `/compact` no rodapé a partir de 80% arredondados. O leitor confirmou 81% neste chat.
- **Complementar.** Oficina `0.1.1` instalada separadamente, commit local `318ca52`. Faz auditoria e manutenção autorizada. Candidatos externos servem de referência para adaptações locais ao padrão TFD.
- **Pendente.** Confirmar o aviso de contexto em um novo chat do Desktop e validar o fluxo completo do TFD em um módulo real no host. A Biblioteca-skill recebeu apenas as pastas de catálogo no commit `43bfd4b`. O código do TFD e da Oficina segue em repositórios locais.

Para retomar, abra um chat novo na pasta do TFD, leia esta seção e execute apenas o próximo pedido do usuário.

## Base da reconstrução

O **The Office** é o sistema de referência do TFD. Para cada etapa e setor,
analise o fluxo e os artefatos do The Office e reconstrua a capacidade no
TFD aplicando as melhorias consolidadas no histórico do DeepSeek e nesta
conversa. O histórico registra as decisões de melhoria. A biblioteca usada
na execução fica dentro do próprio TFD, em `library/`.

## Decisões travadas

1. Nome: **The Factory Developer (TFD)**. Prefixo `TFD-` em agentes e skills.
2. Host-agnóstico: nada de `CODEX_HOME`. Adaptadores em `hosts/`.
3. Plugin = método; projeto = conhecimento. Nada de artefato de cliente no plugin.
4. 13 setores, incluindo `qa_spec`, `qa_backend`, `qa_ui` e `documentation`.
5. Quem executa não aprova o próprio trabalho.
6. Rework no fim de cada etapa, até cumprir a spec; 3 ciclos e depois BLOCKED.
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
| 6 | Instalação por host e corte do V2 | Codex: pacote local instalado e 14 skills descobertas; outros hosts e corte do V2 pendentes |

## Núcleo disponível

- `scripts/validate_task.py` valida o contrato. Exige `gates`, verifica os vínculos entre requisitos, microtasks, aceites e testes, e rejeita ciclos e microtasks em que o autor é o próprio validador.
- `scripts/validate_estimate.py` valida o arquivo de estimativa por fase. Confere a ordem das horas e a data de calendário. A estimativa dentro da task usa a mesma regra de ordem.
- `scripts/office.py` oferece `plan`, `check` e `report`. O `check` executa testes e grava um recibo. Se o Git falhar ao levantar os caminhos alterados, o recibo registra que o escopo não foi verificado.
- `scripts/pipeline.py` verifica o log local do módulo. Ele indica o gate e a ação pendente. O host executa as ações e o usuário decide a aprovação. O [adaptador Codex](../hosts/codex/README.md) está disponível. O catálogo de complementares e os demais adaptadores seguem planejados.
- `scripts/token_usage.py` gera recibos de consumo real reportado pelo Codex
  por task, etapa e tentativa. Suporta eventos JSONL do CLI e turnos do
  Desktop. O CI e suas instruções específicas pertencem ao repositório do
  projeto. Veja a [coleta e o handoff de CI](../hosts/codex/README.md#token-receipts).

Para rodar a suíte local a partir da raiz do TFD, use `python -B -m unittest discover -s tests`.

## Próximo passo imediato

O Discovery consulta o índice da biblioteca local do TFD em
`library/indexes/resources.json`,
registra as evidências no projeto e volta à pesquisa quando o QA aponta uma
lacuna na spec. O harness conduz o módulo no host e usa o CLI para validar
as transições registradas.

### Prompts e REA

- Os prompts ativos de Product, Discovery, QA de spec e retomada estão em
  inglês. Aplicamos compressão manual na autoria: remover repetição, manter
  regras e evidências, e consultar referências sob demanda. O
  [LLMLingua](https://github.com/microsoft/LLMLingua) foi estudado como
  referência. A execução do TFD usa os prompts revisados diretamente.
- Medição do `SKILL.md` de QA de spec, da versão 1.1.0 para 1.2.0:
  990 → 435 tokens (−56,1%), com `tiktoken 0.14.0` e `o200k_base`.
  A contagem cobre o arquivo inteiro. A suíte local verifica estrutura e
  roteamento estático; a execução das regras no host é uma checagem separada.
- A ausência de software de referência pode ser registrada e não bloqueia G1.
  No Discovery, identifique o tipo de projeto. Se a engenharia reversa ajudar,
  pergunte se o usuário autoriza o REA e qual variante usar para aquele tipo.
  Confirme alvo e escopo antes de chamar. A pesquisa independente pode seguir.
  A integração de variantes fica nos plugins complementares.

Próxima verificação de integração: conduzir um módulo do projeto no host,
registrando a execução real e as aprovações humanas.

### Verificação dos setores e gates

- `python -B -m unittest discover -s tests`: 64 testes, exit 0.
- `python -B scripts/pipeline.py examples/workflow.example.json`: exit 0, aguardando a constituição em G0.
- Codex CLI efêmero, com as skills fornecidas como entrada: autoria de spec fictícia de estoque, decisões dos setores e harness, e revisão independente. O QA devolveu a spec HTTP por lacunas de contrato e testabilidade. A revisão corrigiu o cálculo de p95 e continuou bloqueada pelo OpenAPI ausente. O reteste do QA retornou REWORK para o contrato ausente e PASS para uma spec de função isolada com evidência suficiente. Os dois JSONs finais passaram no validador.
- O Codex CLI instalou `the-factory-developer@tfd-local` 0.1.0, e `codex debug prompt-input` confirmou as 14 skills, incluindo o harness. Na sessão efêmera de teste, o helper de shell falhou ao tentar abrir a skill instalada. A descoberta foi verificada. A leitura em execução e a validação de um módulo real continuam pendentes.

### Tradutor

- O harness usa `tfd-translator` antes de delegar. O repasse fica em inglês, com resposta ao usuário em português do Brasil.
- `python -B -m unittest discover -s tests` passou 74 testes, saída 0. No Codex CLI efêmero, com a skill fornecida na entrada, passaram três casos fictícios. O repasse preservou a correção de caminho, a cópia literal e a exigência de aprovação. O pedido ambíguo gerou uma pergunta em português. A pergunta geral ficou fora do fluxo.
- O teste conjunto registrou 25.204 tokens de entrada e 172 de saída. A medição inclui o contexto do host. A execução pela instalação nativa e a comparação de custo total com e sem Tradutor continuam pendentes.

## Decisões abertas

- Schema final da task e do `estimate.json`.
- Formato de `agent.json` e do `SKILL.md` por setor.
- Como o `converge` mede "entregue como especificado".
- Em que gate o guia HTML é gerado.
- Contrato do adaptador de host.
