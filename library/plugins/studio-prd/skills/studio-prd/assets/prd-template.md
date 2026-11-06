# PRD do projeto

Revisão: preencher. Estado: DRAFT, aprovação pendente.
Briefing: [contexto](../briefing/briefing.md).
Planejamento interno separado: [MD](../planejamento/plano-de-execucao.md),
[JSON equivalente](../planejamento/plano-de-execucao.json).

## Objetivo, resultados e fronteiras

Problema e resultado mensurável, escopo completo aprovado, exclusões e restrições.
Arquitetura acordada e decisões existentes; monólito modular somente se confirmado.

## Atores, histórias e jornadas ponta a ponta

| Ator | Responsabilidade e permissões | Jornada e cenários | Regra/fonte | Aceite |
| --- | --- | --- | --- | --- |

História curta não substitui gatilho, pré-condições, fluxo principal, alternativas,
erros, recuperação e resultado. Incluir sistemas externos como atores.

## Inventário explícito de módulos

Quantidade de módulos aprovados: preencher após aprovação, não contar propostas.

| ID estável | Módulo e objetivo | Fronteira funcional | Atores | Dependências/capacidades | Task |
| --- | --- | --- | --- | --- | --- |

Uma task completa por módulo. Banco, backend, frontend, QA, segurança, UI/UX e
documentação permanecem microtarefas. Sem task por camada, fase ou especialista.

## Regras e requisitos transversais

Entidades/estados/invariantes e interfaces compartilhadas; requisitos funcionais,
segurança, desempenho, acessibilidade, observabilidade, dados e operação.
Classificar aprovado/proposto/desconhecido/excluído com fonte e justificativa.

## Reuso, referências e direção visual

Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando o roteamento seletivo vigente do Harness.

Inventário de sistema existente quando aplicável; evidências e limites, decisões
manter/completar/corrigir/refatorar/substituir/descontinuar, sem exclusão implícita.
Biblioteca de referências com origem/revisão. Quando houver UI, links ao Design
Guide MD, tokens e catálogo HTML vivo do projeto, mantidos durante cada SDD.

Somente bibliotecas/componentes relevantes: manter o mesmo ID da fonte do PRD
até spec e Task. Reuso nativo primeiro, catálogo compatível depois, pesquisa
Context7/GitHub oficial apenas para lacunas. PROPOSED/UNKNOWN são válidos antes
da decisão; não inventar versões nem instalar todas as candidatas.

| ID biblioteca / ID fonte | Repo/docs oficial | Versão/commit ou UNKNOWN | Componente/variante | Propósito/módulo | Licença | Dependências | Adaptações | Estado/decisão |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Rastreabilidade, riscos e decisões pendentes

Ator → cenário → regra → referência/decisão → aceite → módulo/task.
Lacunas materiais impedem declarar a respectiva especificação completa.

## Aprovações e passagem para SDD

Registrar aprovação real do PRD, módulos e sequência. Informar N módulos e pedir
início da primeira especificação. Não autoriza implementação, merge ou deploy.
SDD reutiliza o template completo existente e JSON equivalente, sem novo modelo.


## Fundamentação e impactos preliminares

Separar Banco de dados, API/Backend e Frontend/UI quando relevantes; registrar
entidades/regras/jornadas conceituais, qualidades observáveis, restrições e riscos.
Detalhes de implementação pertencem à Arquitetura/SDD/UX. N/A precisa de motivo.

Na tabela/seção existente de decisões, manter natureza FACT/HYPOTHESIS/PREFERENCE/
DECISION separada de APPROVED/PROPOSED/UNKNOWN/EXCLUDED. Incluir alternativas,
trade-offs, recomendação e fonte original consultada (caminho/URL, versão, seção,
data, o que sustenta e limites). Distinguir inferência de fato. Hipótese aprovada
não vira fato; fonte inacessível é NOT_VALIDATED, não consulta inventada.

Se houver proposta de MVP/primeira entrega, separar do escopo completo e das
futuras evoluções, sem reduzir compromisso aprovado automaticamente. Bloqueios
críticos impedem declarar consolidação concluída; rascunhos podem expô-los.
Registrar aprovação humana real e decisões revisitadas com justificativa/impacto.
