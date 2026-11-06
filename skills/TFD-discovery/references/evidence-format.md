# Saída do Discovery

Grave os três arquivos na documentação do projeto. Reaproveite IDs estáveis.

- `sources.json` é uma lista de fontes com `id`, `location` (URL ou caminho), `revision` (versão, hash ou `UNKNOWN`) e `status` (`verified`, `stale` ou `missing`). Marque `verified` depois de abrir a fonte e conferir sua aplicabilidade à versão investigada. Registre a data da consulta em `checked_at` quando houver consulta.
- `evidence.json` é uma lista com `id`, `claim`, `class` e `limits`. Para `OBSERVED` e `INFERRED`, inclua `source_id` de uma fonte verificada e `locator` com a seção, caminho ou ponto da captura que sustenta o achado. Em `INFERRED`, explicite a dedução e seu limite. Em `UNKNOWN`, descreva a pergunta e o que falta em `limits` e inclua `essential` (booleano). Se houver fonte tentada, inclua seu `source_id`.
- `findings.md` resume o estado atual, riscos e lacunas por ID de evidência. Para uma lacuna essencial, registre a decisão bloqueada, a tentativa feita e a próxima ação. Cite a revisão dos artefatos ao entregar para spec e QA.

Uma tela observada sustenta afirmações sobre o fluxo visível. Regras do servidor, persistência e permissões precisam de evidência própria. O validador confere estrutura e vínculos. O QA confere o conteúdo contra as fontes.

Saídas do validador: `0` estrutura válida sem lacuna essencial, `1` registro inválido e `2` lacuna essencial registrada (`BLOCKED`).
