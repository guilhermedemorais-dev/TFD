# SPEC: Nome da página/tela

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Deriva de um Module Spec. Referencia component specs.

## Objetivo
O que esta página/tela permite que o usuário faça.

## Usuário alvo
Quem usa esta tela e em que contexto/permissão.

## Fluxo principal
Passo a passo do caminho feliz.

## Layout esperado
Estrutura visual macro. Referenciar mockup aprovado (ui-ux-standard), não inventar.

## Componentes obrigatórios
Lista de componentes usados (cada um deve ter component-spec).

## Estados da tela
Loading, vazio, com dados, erro, sem permissão, sucesso.

## Regras de negócio
Regras que se aplicam nesta tela (detalhe em validation-rules-spec).

## Validações
Validações de entrada e de fluxo nesta tela.

## Navegação
De onde se chega, para onde vai, parâmetros e deep links.

## Banco
Dados lidos/gravados por esta tela. `N/A` + motivo se não houver.

## API/Backend
Endpoints consumidos, contratos e erros tratados. `N/A` + motivo se não houver.

## Frontend/UI
Comportamento de UI, responsividade e acessibilidade (detalhar com ui-ux-standard).

Bibliotecas selecionadas: preservar ID biblioteca/ID fonte do PRD, repo/docs
oficial, versão/commit ou UNKNOWN, componente/variante, propósito/módulo, licença,
dependências, adaptações e estado da decisão. Reuso nativo e catálogo compatível
primeiro; pesquisa oficial dirigida apenas para lacunas. Encaminhar o mesmo ID
à Task e às referências JSON necessárias, sem carregar candidatas não escolhidas.

## Segurança
Permissões necessárias, dados sensíveis exibidos, limites de acesso.

## Observabilidade/logs
Eventos de uso, métricas e erros que devem ser registrados.

## Critérios de aceite
Critérios objetivos e testáveis da tela.

## Fora do escopo
O que esta tela explicitamente não cobre.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Referências e decisão de fontes

Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando a consulta global do Harness.
