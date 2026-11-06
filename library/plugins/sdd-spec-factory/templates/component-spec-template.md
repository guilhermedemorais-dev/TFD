# SPEC: Nome do componente

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Deriva de uma Page/Feature Spec.

## Objetivo
O que este componente faz e por que existe.

## Onde é usado
Telas/contextos que consomem este componente.

## Origem e decisão de reuso
Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando a consulta global do Harness.

Para origem relevante, preservar ID biblioteca/ID fonte do PRD: repo/docs oficial,
versão/commit ou UNKNOWN, caminho/variante do componente, propósito/módulo, licença,
dependências, adaptações e estado da decisão. Reuso nativo primeiro, catálogo
compatível depois, pesquisa Context7/GitHub oficial apenas para lacunas. A Task
reutiliza o mesmo ID; somente dependências selecionadas exigem fontes REQUIRED.

## Props/entradas
Nome, tipo, obrigatório/opcional, valor padrão e descrição de cada entrada.

## Estados visuais
Default, hover, focus, ativo, desabilitado, loading, erro, vazio, selecionado.

## Comportamento
Interações, eventos emitidos e efeitos colaterais esperados.

## Validações
Regras de validação aplicadas pelo componente.

## Mensagens de erro
Textos e condições de cada mensagem de erro/feedback.

## Acessibilidade
Roles, labels, foco, navegação por teclado, contraste (validar com ui-ux-standard).

## Responsividade
Comportamento em mobile, tablet e desktop.

## Critérios de aceite
Critérios objetivos e testáveis do componente.

## Fora do escopo
O que este componente explicitamente não faz.

## Riscos
Riscos de reutilização, regressão ou acoplamento.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).
