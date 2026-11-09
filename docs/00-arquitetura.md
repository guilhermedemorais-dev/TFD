# Arquitetura — The Factory Developer (TFD)

O TFD coordena PRD, Discovery, arquitetura, implementação e entrega com
evidências rastreáveis e aprovação humana em cada gate.

## 1. Nome e escopo

- Plugin `the-factory-developer` (TFD), com skills e agentes identificados pelo
  prefixo TFD.
- **Núcleo independente do host.** Os contratos e validadores Python são
  locais. O adaptador disponível registra skills e subagentes no Codex.
  [Adaptador Codex](../hosts/codex/README.md)
- Função do núcleo: orquestrar. Engenharia reversa, design system, análise de APK
  e afins são **plugins complementares** catalogados, chamados por id.
- O produto é código novo. Referência serve para entender e escrever melhor,
  nunca para clonar.

## 2. Princípios

1. Plugin = método; projeto = conhecimento.
2. Setorização é economia de contexto: o harness lê o todo; o setor lê a fatia.
3. Evidência vence prosa.
4. Regra determinística vira código; julgamento vira uma página.
5. Quem executa não aprova o próprio trabalho.
6. Humano aprova gate, escopo, prazo, merge e deploy.
7. Complementar é plugável, versionado e autorizado antes de instalar.

## 3. Setores

| # | Setor | Responsabilidade | Não faz |
|---|---|---|---|
| 1 | `product` | briefing, PRD, escopo, prioridade, perguntas ao cliente | arquitetura e código |
| 2 | `discovery` | fontes, as-is, engenharia reversa assistida, riscos, lacunas | decidir arquitetura |
| 3 | `architecture` | arquitetura, contratos, ADRs, plano de fases e autoria da spec | implementar ou aprovar a própria spec |
| 4 | `database` | modelo, migração, integridade, rollback | API e UI |
| 5 | `backend` | código, contrato de API, teste do próprio código | aprovar a si mesmo |
| 6 | `frontend` | código, estados, acessibilidade, teste do próprio código | aprovar a si mesmo |
| 7 | `ui_ux` | design system do projeto, guia vivo, revisão visual | codar produção |
| 8 | `qa_spec` | revisa PRD, discovery, contratos e spec antes de construir: ambiguidade, contradição, lacuna, testabilidade, rastreabilidade | implementar ou reescrever o artefato pelo autor |
| 9 | `qa_backend` | validação independente de API, dados e regra | corrigir pelo autor |
| 10 | `qa_ui` | validação independente de tela, fluxo e acessibilidade | corrigir pelo autor |
| 11 | `security` | ameaça, authn/authz, segredo, dependência, dado sensível | aprovar sozinho |
| 12 | `devops` | ambiente, repositório, CI/CD, observabilidade, rollback | codar produto |
| 13 | `documentation` | arquitetura da documentação, guia técnico e do usuário, HTML | inventar comportamento |

Fora do pipeline de produção:

- `harness`: orquestra, reconcilia evidência, não escreve produto.
- `translator` (Tradutor): comprime e traduz o pedido para o setor ativo, com resposta ao usuário em português do Brasil. Atua antes da delegação.
- `oficina`: plugin separado de manutenção e evolução do próprio harness. Só
  atua sob pedido do usuário ou por incidente detectado. Nunca durante task de
  cliente.

**Regra de QA:** a especificação é revisada pelo `qa_spec` **antes** da
implementação; backend e frontend testam o que escrevem; depois `qa_backend` e
`qa_ui` validam de forma independente, na revisão atual. Quem escreveu não pode
atestar o próprio PASS, seja spec, código ou documentação.

## 4. Pipeline

```
G0   Constituição do projeto            princípios e restrições
G0.5 Preparação do ambiente (devops)    repo, deps, MCP, auth, versões, SO
G1   Briefing + PRD (product)           escopo, não-escopo, referências
G2   Discovery (discovery)              fontes, as-is, riscos, lacunas
G3   Revisão inicial (qa_spec)          PRD e Discovery, com retorno à pesquisa se necessário
G4   Arquitetura e contratos            completo (seção 5)
G5   Plano de fases + estimativa        módulos, fases, prazo, aprovação
G6   Por fase: spec + Discovery → qa_spec → rework de pesquisa/spec → nova revisão
       → PASS do QA → aprovação humana da task → produção
G7   Por etapa da task:
       build + autoteste (backend/frontend)
       → QA independente (qa_backend/qa_ui)
       → segurança/UX/devops quando o gatilho aplicar
       → rework até cumprir a spec (no fim da etapa)
       → aprovação humana da etapa
G8   Pacote de revisão → revisão humana do PR e verificação local
       → documentação técnica e de usuário → aprovação final
       → merge e deploy sob autorizações separadas
```

Gates que falham param o fluxo. Ferramenta faltando gera `BLOCKED` com comando e
pedido de autorização; nada instala sozinho.

## 5. G4 — Arquitetura e contratos (completo)

Nenhum item é opcional sem justificativa registrada.

1. **Drivers e atributos de qualidade**: desempenho, disponibilidade, segurança,
   custo, operabilidade, escalabilidade, compliance. Cada um com métrica.
2. **Contexto e fronteiras**: atores, sistemas externos, o que é nosso e o que não é.
3. **Visões C4**: contexto, containers, componentes; uma sequência de runtime para
   cada fluxo crítico.
4. **Dados**: modelo conceitual e físico, dono de cada entidade, ciclo de vida,
   retenção, migração, rollback, integridade e concorrência.
5. **Contratos de integração**: OpenAPI para HTTP, AsyncAPI/eventos, webhooks,
   idempotência, versionamento, erros, autenticação.
6. **Segurança**: fronteiras de confiança, authn/authz, sessão, segredo, upload,
   dado pessoal, ameaças (STRIDE) e mitigação.
7. **Implantação**: ambientes, topologia, configuração, CI/CD, rollback, backup.
8. **Observabilidade**: logs, métricas, traces, SLO, alerta, runbook.
9. **ADRs**: contexto, alternativas, decisão, consequência, critério de reversão.
10. **NFRs verificáveis** e *fitness functions* (teste automatizado da propriedade).
11. **Riscos e premissas** com impacto e mitigação.
12. **Rastreabilidade**: REQ → decisão → contrato → teste.

## 6. Estrutura da task por módulo

Campos obrigatórios:

- `goal`, `scope`, `out_of_scope`, `allowed_paths`, `protected_paths`
- `requirements` (REQ) com fonte e prioridade
- `business_rules`
- `references` com path e finalidade
- `microtasks` com `owner`, `checklist`, `deliverables`, `completion_condition`,
  `validator`
- `acceptance_criteria` (AC) com `validation` apontando para `TEST`
- `required_tests` com comando e esperado
- `stop_conditions`
- `gates` do módulo
- `estimate` (seção 7)

Regra de ouro: **o que fazer e o que não fazer**. Se a execução precisa decidir
algo que o contrato não cobre, ela para e pergunta; não inventa.

## 7. Prazo e estimativa

O cliente pergunta prazo. A resposta honesta tem três níveis:

| Momento | Precisão | O que dá para dizer |
|---|---|---|
| G1 (PRD) | ordem de grandeza (±50% a 2x) | faixa por módulo, com premissas |
| G5 (plano de fases) | ±25% a 40% | faixa por fase e data-alvo |
| Após 2 fases medidas | ±15% | ritmo real por setor |

Método: decompor em microtasks, estimativa de três pontos (otimista, provável,
pessimista) por microtask, PERT para o total, e **classe de referência** com o
histórico real dos seus projetos. A partir do G5, cada fase grava
`estimate.json` com faixa, base e confiança; ao fechar a fase, grava o realizado.
Sem histórico, a primeira estimativa é palpite estruturado, e deve ser dita assim.

## 8. Rework

O rework acontece **no fim de cada etapa da task**, não no meio.

Regra: repetir até entregar exatamente o que está na especificação — cada
microtask, cada critério de aceite, cada teste. Só quando a etapa cumpre a spec
ela segue adiante.

1. build + autoteste.
2. QA independente da etapa (`qa_spec` já aprovou a spec antes; `qa_backend`/`qa_ui`
   validam a implementação).
3. Se reprovar: rework **da etapa**, com o motivo objetivo.
4. Ao passar: aprovação humana da fase. A documentação oficial usa a revisão
   conferida no PR e na execução local.
5. No PR, o revisor do host aponta erros; você confere e pede correção. O rework
   continua até a spec estar cumprida e o PR aceito.

Limite: 3 ciclos automáticos por etapa; depois `BLOCKED` com diagnóstico e decisão
sua. Rework não é "refazer tudo": é fechar o gap entre o entregue e o especificado.

## 9. Evidência

```json
{"claim":"...","class":"OBSERVED|INFERRED|UNKNOWN","source":"...",
 "tool":"...","version":"...","target_hash":"...","limits":"..."}
```

Spec só cita `evidence_id`. `UNKNOWN` não vira requisito. Receipt é gerado por
quem executou, com exit code e commit; nunca escrito à mão.

## 10. Plugins complementares

Catálogo em `catalog/complementary.json`; contrato único de saída (`evidence.json`).
Exemplos: `source-analyzer` (repo com fonte), `rea-web`, `rea-apk`, `rea-native`
(Ghidra), `browser-capture`. O núcleo não conhece nenhum deles; chama por id.

**Referência não é clone.** O código de referência orienta a lógica; a
implementação é nova, com as palavras do projeto, mais simples, mais segura e mais
otimizada quando possível. Copiar trecho proprietário é proibido.

## 11. Hospedeiros (hosts) e sistemas operacionais

O núcleo é host-agnóstico. Nada de `CODEX_HOME` na arquitetura.

```
hosts/
  codex/      plugin.json, mapeamento de AGENTS.md e skills
  claude/     plugin + skills
  gemini/     extensão + skills
  cursor/     regras + skills
  generic/    MCP + CLI + AGENTS.md
```

Cada adaptador declara o que o host sabe fazer: subagente, MCP, shell, permissão,
paralelismo. O harness usa o que existe e registra o que não existe como
`NOT_AVAILABLE`; não inventa capacidade. O mesmo projeto pode ter dois hosts
ativos ao mesmo tempo, desde que o lock de task impeça escrita concorrente.

SO: Windows 10, Linux Mint e macOS. O detector de alvo identifica SO e arquitetura.
Comando de complementar declara variante por SO; caminho em artefato é POSIX; fim
de linha normalizado antes de hash.

Instalação: `TFD install --host <codex|claude|gemini|cursor|generic>`, sempre em
perfil isolado para teste antes do perfil real.

## 12. Plugin de manutenção — `oficina` (separado)

A manutenção não mora no TFD. É plugin próprio, instalado à parte, e a skill
global só o chama quando há motivo.

### Gatilhos

1. **Pedido do usuário**: "corrige a skill de QA", "audita os setores".
2. **Incidente detectado pelo harness**:
   - o mesmo gate reprovou 2 vezes pelo mesmo motivo;
   - rework passou de 2 ciclos na mesma etapa;
   - skill referenciada não existe ou mudou de hash (drift);
   - `BLOCKED` repetido por falta da mesma ferramenta;
   - spec aprovada gerou implementação que falhou no aceite.

### Ciclo

```
observar → registrar incidente → diagnosticar causa raiz → propor
→ autorização do usuário → corrigir → testar → registrar resultado
```

Cada incidente vira um registro em `docs/office/incidents/`:

```json
{
  "id": "INC-014",
  "when": "2026-11-05T00:10:00Z",
  "task": "DEMO-012",
  "symptom": "qa_spec reprovou 2x por AC sem teste",
  "root_cause": "skill spec não exige AC → TEST",
  "fix": "regra + checklist no skill spec",
  "status": "proposed|approved|fixed|verified",
  "evidence": "receipts/DEMO-012.json"
}
```

### Regras

- **Sempre reporta ao usuário**: sintoma, causa raiz, mudança proposta, risco e
  evidência. Nunca altera em silêncio.
- Modos **AUDIT** (só lê e propõe) e **CHANGE** (só com autorização explícita).
- Branch própria, sem merge automático, teste antes e depois.
- Fora de task de cliente: nunca autoaltera durante execução de projeto.
- Método: Skill Creator V2 verificada (versão + hash) + padrão do TFD
  (`references/skill-standard.md`): orçamento de tokens, versionamento,
  teste de roteamento, proibição de README e de referência legada.

### O que ele melhora

Não é "reescrever skill por opinião". É corrigir a causa de um incidente
registrado, com teste que falha antes e passa depois. Sem incidente, não há
mudança.

## 13. O que o TFD não faz

- Não clona produto de terceiro.
- Não instala ferramenta sem autorização.
- Não aprova o próprio trabalho.
- Não guarda conhecimento de cliente dentro do plugin.
- Não promete prazo sem faixa e premissa.
- Não fica presa a um host nem a um modelo.

## 14. Decisões abertas

1. Schema final da task e do `estimate.json`.
2. Formato de `agent.json` e do `SKILL.md` por setor.
3. Como o `converge` mede "entregue como especificado".
4. Em que gate o guia HTML (design e backend) é gerado.
5. Nome definitivo do plugin.
6. Contrato do adaptador de host (capacidades e fallback).
