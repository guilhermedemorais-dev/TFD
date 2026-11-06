# PRD — <nome do produto>

> Versão: 0.1 · Data: <aaaa-mm-dd> · Autor: TFD-product
> Fonte: briefing em `docs/prd/briefing.md`

## Problema

<Problema, para quem, como é resolvido hoje e o custo de não resolver. Cite a fonte.>

## Objetivos

| ID | Objetivo | Como medir |
|---|---|---|
| OBJ-01 | ... | ... |

## Usuários

| Ator | Papel | Necessidade principal |
|---|---|---|
| ... | ... | ... |

## Escopo

- ...

## Não-escopo

- ...

## Requisitos

| ID | Requisito | Fonte | Prioridade |
|---|---|---|---|
| REQ-01 | ... | ... | MUST |

Descrição verificável; prioridade MUST, SHOULD ou MAY. Requisito sem fonte não entra.

## Regras de negócio

| ID | Regra | Fonte |
|---|---|---|
| RULE-01 | ... | ... |

## Riscos

| ID | Risco | Impacto | Mitigação |
|---|---|---|---|
| R-01 | ... | ... | ... |

## Métricas de sucesso

| Métrica | Meta | Como coletar |
|---|---|---|
| ... | ... | ... |

## Referências

| ID | Caminho ou nome | Finalidade |
|---|---|---|
| REF-01 | ... | ... |

Se o usuário indicar software de referência, registre nome, versão conhecida,
acesso e finalidade para o `discovery`. Sem indicação, a nota de ausência é
opcional e o G1 segue normalmente.

## Perguntas abertas

| ID | Pergunta | Dono | Prazo | Bloqueia G1? |
|---|---|---|---|---|
| Q-01 | ... | ... | ... | sim / não |

## Esqueleto de docs/prd/briefing.md

```text
# Briefing — <produto>
Fonte e data:
Participantes:
Bloco 1 — problema e valor:
Bloco 2 — usuários e fluxo:
Bloco 3 — escopo e restrições:
Bloco 4 — requisitos e regras:
Bloco 5 — referências:
  Registre o software indicado ou, opcionalmente, a ausência de referência.
Bloco 6 — sucesso e riscos:
Respostas dadas:
Perguntas abertas (pergunta, dono, prazo, bloqueia G1):
```

Regra final: o que não foi respondido fica em "perguntas abertas" e nunca vira REQ.
