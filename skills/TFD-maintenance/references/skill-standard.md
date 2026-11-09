# Padrão de skill do TFD

Vale para toda skill criada ou alterada. Hoje, os testes de `product` e
`qa_spec` verificam frontmatter, tamanho e casos estáticos de roteamento.
Use a **Skill Creator V2 do projeto**, versão `2.1.0`. Confira a origem, a
versão e o SHA-256 da cópia antes de usar seu validador com `--profile codex`.
[Revisão verificada da Skill Creator V2](https://github.com/guilhermedemorais-dev/Biblioteca-skill/tree/d0a0af6e16152faf0ddbba3d906721d306559d6b/skills/skill-creator)

Rode `python -B -m unittest discover -s tests` a partir da raiz do TFD.
O verificador geral `scripts/check_skill.py` está planejado. Revise as
referências e o comportamento de roteamento no host separadamente.

## Frontmatter obrigatório

```yaml
---
name: tfd-<setor>
description: "<o que faz e quando aplica, em até 60 palavras>"
metadata:
  version: "1.0.0"
  owner: "<setor>"
---
```

- `name`: para skills novas, use minúsculas, hífen e prefixo `tfd-`.
  O nome deve coincidir com a pasta. Preserve os IDs já publicados.
- `description`: até 60 palavras; diz o que faz **e quando ativa**; inclui a
  fronteira (quando não ativar) se houver risco de roteamento errado.
- `version`: semver. Toda mudança de comportamento sobe a versão.

## Tamanho

| Parte | Limite |
|---|---|
| `SKILL.md` | 150 linhas |
| cada `references/*.md` | 1.000 tokens (~4 KB de prosa) |
| `scripts/*` | sem limite, mas testado |

Passou do limite: mover detalhe condicional para `references/` ou para script.

## Estrutura

```
skills/tfd-<setor>/
  SKILL.md
  scripts/        # determinístico, executável
  references/     # lido só quando a condição valer
```

## Escrita

Escreva a descrição e as instruções do `SKILL.md` em inglês direto.
Preserve exemplos de pedidos no idioma do usuário para verificar o roteamento.

1. Assuma que o agente já é capaz. Só escreva o que muda a decisão dele.
2. Um conceito por skill. Mais de dois modos → separe em referências.
3. Imperativo, direto, sem introdução motivacional.
4. Sem README, changelog, guia de instalação ou exemplo decorativo.
5. Referencie as regras comuns em [docs/00-arquitetura.md](../../../docs/00-arquitetura.md) em vez de repeti-las.
6. Use os contratos e caminhos vigentes no TFD. Cite fontes técnicas verificáveis.
7. Exemplo só quando muda a interpretação; nunca para preencher espaço.
8. Comprima o texto na autoria: remova repetição e preserve gatilhos,
   condições de parada, aprovações, entradas, saídas e referências exatas.
   Ao revisar uma skill, compare os tokens com o mesmo tokenizer e confira
   se os casos de uso continuam produzindo as mesmas decisões.

## Divulgação progressiva

- Nível 1: `name` + `description` (sempre no contexto).
- Nível 2: corpo do `SKILL.md` (quando a skill ativa).
- Nível 3: `references/` e `scripts/` (quando a tarefa pede).

Se o corpo já explica tudo, não crie referência. Se o script resolve, não
descreva o algoritmo em prosa.

## Teste de roteamento

Toda skill declara em `tests/` três casos:

- 2 pedidos que **devem** ativá-la;
- 1 pedido que **não deve** ativá-la.

Os casos estáticos conferem os gatilhos declarados. A descoberta efetiva da
skill precisa ser verificada no host.

## Definição de pronto

- [ ] frontmatter válido e `description` ≤ 60 palavras
- [ ] `SKILL.md` ≤ 150 linhas
- [ ] referências dentro do orçamento
- [ ] script executado com saída real registrada
- [ ] teste de roteamento (2 positivos, 1 negativo)
- [ ] suíte local e cenários de comportamento no host na mesma entrega: confira decisões, saídas e permissões e registre o que foi simulado
- [ ] contratos e caminhos vigentes, com configuração do host no adaptador
- [ ] versão atualizada
