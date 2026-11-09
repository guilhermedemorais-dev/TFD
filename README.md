# The Factory Developer (TFD)

O **The Factory Developer (TFD)** é um plugin para conduzir entregas de
software no Codex, do briefing à aprovação. Ele organiza o trabalho por
módulo, distribui as tarefas entre especialistas e reúne as evidências para
você decidir quando cada etapa pode avançar.

## Instalação

1. Cole o link do repositório no Codex: https://github.com/guilhermedemorais-dev/TFD. Não é necessário baixar nem extrair um ZIP.
2. Com Git, Codex CLI e Python 3.10+ disponíveis, execute
   `python -B scripts/install_tfd.py install` no Windows ou
   `python3 -B scripts/install_tfd.py install` no Linux. Você também pode
   usar o [prompt de instalação](docs/GUIA-CODEX.md#prompt-de-instalação).
3. Abra uma nova sessão na pasta do projeto. Para conferir a configuração,
   peça “Me dá um relatório de onde estamos neste projeto”. Para começar uma
   entrega, peça “Abra o módulo de cadastro no TFD e comece pelo briefing”.

Para consultar ou aplicar atualizações, use a skill `tfd-install` ou os
comandos `check` e `update` do instalador. [Guia do Codex](docs/GUIA-CODEX.md)

## Como funciona

1. **Definir e pesquisar.** O Product registra escopo e critérios no PRD. O
   Discovery consulta a biblioteca local e registra fontes e lacunas no
   projeto. Uma pesquisa complementar depende da autorização aplicável.
2. **Especificar.** A Arquitetura traduz os requisitos em contratos, fases e
   testes. Cada módulo tem uma task JSON, que é a fonte de verdade, e uma
   visão Markdown gerada para leitura. O QA de spec revisa antes da implementação.
3. **Implementar e revisar.** O coordenador encaminha as microtarefas aos
   setores. Os QAs aplicáveis revisam a mesma revisão que foi entregue. Em
   caso de reprovação, o autor corrige o escopo apontado e o QA revisa de novo.
4. **Aprovar e documentar.** O TFD apresenta entregáveis, testes e bloqueios.
   Você aprova cada etapa. A documentação técnica e a ajuda ao usuário
   registram o comportamento verificado.

O log do módulo fica no repositório do projeto. O validador local confere a
ordem das etapas, os arquivos de evidência, as revisões e as aprovações
registradas. [Contrato dos gates](skills/TFD-harness/references/gates.md)

## Contexto e medição

As skills usam instruções curtas em inglês e carregam referências conforme
a tarefa. O Tradutor prepara o repasse para o agente responsável. Os leitores
Python medem o tamanho dos arquivos e registram o consumo reportado pelo
Codex, com tokens em cache e ocupação da janela separados. O rodapé indica
`/compact` a partir de 80% de ocupação arredondada. [Recibos e limites de contexto](hosts/codex/README.md#token-receipts)

## Estado do projeto

O TFD está em validação em um projeto real. O [estado do projeto](docs/ESTADO.md)
registra as verificações já feitas e os resultados ainda pendentes.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [Arquitetura](docs/00-arquitetura.md) | Setores, fases, responsabilidades e revisão independente |
| [Tasks por setor](docs/sector-task.md) | Microtarefas, dependências, aceite e evidências |
| [Biblioteca do TFD](library/README.md) | Índice e fontes para Discovery |
| [Padrão de skills](skills/TFD-maintenance/references/skill-standard.md) | Autoria, tamanho e verificações |
| [Adaptador Codex](hosts/codex/README.md) | Integração, recibos de tokens e CI do projeto |

## Referências técnicas

- **Compressão de prompts.** Os estudos da série LLMLingua foram consultados
  para orientar a redução de contexto. O TFD aplica edição manual às skills
  e usa o Tradutor para condensar cada repasse. Os algoritmos dos artigos
  servem como referência de pesquisa. [LLMLingua, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.825/) ·
  [LLMLingua-2, Findings of ACL 2024](https://aclanthology.org/2024.findings-acl.57/)
- **Integração com o Codex.** O adaptador usa catálogos de plugins,
  subagentes nativos e instruções do perfil. [Plugins](https://learn.chatgpt.com/docs/developer-commands#codex-plugin) ·
  [Subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents) ·
  [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- **Pesquisa de documentação.** O Discovery começa no índice local. Quando
  for preciso complementar a pesquisa técnica e houver autorização, o
  Context7 é a primeira opção de consulta. [Context7 MCP](https://context7.com/docs/resources/all-clients)
- **Recuperação por grafos, em pesquisa.** GraphRAG recupera contexto por
  relações entre entidades extraídas de documentos. RepoGraph estuda a
  navegação por grafos de código. GraphCoder usa recortes de dependências
  para selecionar contexto. Esses trabalhos orientam a proposta
  **Repository-Aware GraphRAG**, com Graphify como candidato à extração do
  grafo de código. O benchmark vai comparar a busca atual com a recuperação por
  grafo, medindo tokens, cobertura de evidências e afirmações sem suporte.
  [GraphRAG, Microsoft Research](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) ·
  [RepoGraph, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4a4a3c197deac042461c677219efd36c-Abstract-Conference.html) ·
  [GraphCoder, artigo dos autores](https://arxiv.org/abs/2406.07003) ·
  [Graphify](https://github.com/Graphify-Labs/graphify)
