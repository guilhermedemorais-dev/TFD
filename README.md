# The Factory Developer (TFD)

**Primeira instalação no Codex Desktop?** Abra o
[guia de instalação e uso](docs/GUIA-CODEX.md) ou copie o
[prompt de instalação](docs/GUIA-CODEX.md#prompt-de-instalação).

Reconstrução do harness, setor por setor, a partir do que o V2 provou e do que ele
errou. O V2 fica **somente leitura** até o V3 passar em uma entrega real.

- **Função do TFD:** orquestrar o desenvolvimento — escopo, setores, gates,
  evidência e entrega. Nada além disso.
- **Engenharia reversa, design system, análise de APK e afins:** plugins
  complementares previstos na arquitetura. O catálogo e a integração estão
  planejados.
- **O produto:** código novo, escrito no projeto. Referência serve para entender,
  nunca para clonar.

## Status

Consulte [docs/ESTADO.md](docs/ESTADO.md) para ver o que está implementado,
o que foi verificado e o que está planejado.

## Documentação

| Documento | Conteúdo |
|---|---|
| [Biblioteca do TFD](library/README.md) | índice, referências e artefatos usados pelo Discovery |
| [docs/00-arquitetura.md](docs/00-arquitetura.md) | camadas, pipeline, gates, árvores, complementares, OS |
| [schemas/task.json](schemas/task.json) | contrato da task e vínculos entre requisitos, microtasks, aceites e testes |
| [schemas/estimate.json](schemas/estimate.json) | formato da estimativa por fase |
| [Padrão de skills](skills/TFD-maintenance/references/skill-standard.md) | formato, tamanho e verificações das skills |
| [Harness e gates](skills/TFD-harness/references/gates.md) | entregáveis, revisões, rework e aprovação humana |
| [Adaptador Codex](hosts/codex/README.md) | descoberta, instalação e execução das skills no Codex |

## Executar o fluxo

No host, carregue [TFD-harness](skills/TFD-harness/SKILL.md) para abrir ou
retomar um módulo. O roteiro seleciona os setores conforme a etapa.
Crie o log do módulo em `docs/` do projeto a partir do
[exemplo de workflow](examples/workflow.example.json) e valide antes de avançar:

```text
python <tfd-root>/scripts/pipeline.py <workflow.json> --project-root <project-root>
```

O CLI verifica a ordem, os artefatos, as revisões e as aprovações registradas.
O host conduz as chamadas aos setores. O usuário decide a aprovação.

## Regra de trabalho

Cada etapa começa com escopo declarado (arquivos, conteúdo, critério de aceite),
passa por revisão e só então vira código. O V3 não nasce de cópia do V2; nasce de
decisões registradas.
