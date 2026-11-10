> Contexto TFD · 927 palavras · 1707 tokens (o200k_base)

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

1. **Definir e pesquisar.** O Product faz perguntas sobre decisões de negócio
   pendentes e registra escopo e critérios no PRD. O Discovery reutiliza evidências
   do projeto e pesquisa lacunas técnicas na biblioteca e em fontes verificadas,
   além dos conceitos do PDF. A pesquisa pode ser retomada nas etapas seguintes.
2. **Especificar.** A Arquitetura traduz os requisitos em contratos, fases e
   testes. Cada módulo tem uma task JSON, que é a fonte de verdade, e uma
   visão Markdown gerada para leitura. O QA de spec revisa antes da implementação.
3. **Implementar e revisar.** O coordenador encaminha as microtarefas aos
   setores. Os QAs aplicáveis revisam a mesma revisão que foi entregue. Em
   caso de reprovação, o autor corrige o escopo apontado e o QA revisa de novo.
4. **Aprovar e documentar.** O TFD apresenta entregáveis, testes e bloqueios.
   Você aprova PRD, task e cada etapa implementada. A preparação técnica G2-G5
   pode avançar com autorização explícita e QA aplicável; G6 chega com spec e task
   correspondentes e PASS independente. A documentação técnica e a ajuda ao usuário
   registram o comportamento verificado.

O log do módulo fica no repositório do projeto. O validador local confere a
ordem das etapas, os arquivos de evidência, as revisões e as aprovações
registradas. [Contrato dos gates](skills/TFD-harness/references/gates.md)

A [spec desta melhoria e sua task](docs/reviewed-delivery/README.md) registram o
modo opcional, a avaliação do guia MatthewKerns e os limites de verificação.
O [repositório do guia](https://github.com/MatthewKerns/software-development-best-practices-guide.git)
é fonte externa para consulta sob demanda; o TFD guarda o ponteiro, sem distribuir
ou indexar seu conteúdo completo nos grafos.

## Contexto e medição

As skills usam instruções curtas em inglês e carregam referências conforme
a tarefa. O Tradutor prepara o repasse para o agente responsável. Os leitores
Python medem o tamanho dos arquivos e registram o consumo reportado pelo
Codex, com tokens em cache e ocupação da janela separados. O rodapé indica
`/compact` a partir de 80% de ocupação arredondada. [Recibos e limites de contexto](hosts/codex/README.md#token-receipts)

O adaptador Graphify recupera arquivos e relações do próprio TFD, com versão
fixa, proveniência e verificação de atualização do índice. As consultas têm
saída limitada e fallback local; as fontes canônicas continuam obrigatórias.
O ambiente isolado usa Linux ou WSL 2 no Windows. A instalação do TFD inclui
o adaptador; o runtime Graphify exige preparação e ativação separadas.
[Configuração e comandos](library/docs/operations/graphify.md)

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
- **Recuperação por grafos.** GraphRAG recupera contexto por
  relações entre entidades extraídas de documentos. RepoGraph estuda a
  navegação por grafos de código. GraphCoder usa recortes de dependências
  para selecionar contexto. Esses trabalhos orientam a arquitetura descritiva
  **Repository-Aware GraphRAG**. O adaptador local usa Graphify para extração
  e consulta do bundle TFD. A extensão ao código dos projetos e o benchmark
  comparativo continuam pendentes. O benchmark vai comparar a busca atual com a recuperação por
  grafo, medindo tokens, cobertura de evidências e afirmações sem suporte.
  [GraphRAG, Microsoft Research](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) ·
  [RepoGraph, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4a4a3c197deac042461c677219efd36c-Abstract-Conference.html) ·
  [GraphCoder, artigo dos autores](https://arxiv.org/abs/2406.07003) ·
  [Graphify](https://github.com/Graphify-Labs/graphify)
