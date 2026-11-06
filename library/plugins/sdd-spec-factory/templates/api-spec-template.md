# SPEC: API/Backend - Nome do recurso/serviço

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Crie apenas quando houver backend. Não invente endpoints existentes (`HIPÓTESE:`).

## Status
Rascunho | Em revisão | Aprovada

## Objetivo
O que este serviço/endpoint resolve.

## Contexto
Módulo/feature e specs relacionadas.

## Endpoints
Para cada endpoint:

- **Método e rota:** `GET /recurso/:id`
- **Descrição:** o que faz.
- **Autenticação/Autorização:** quem pode chamar.
- **Parâmetros:** path, query, headers.
- **Request body:** schema/campos, tipos, obrigatoriedade.
- **Response:** schema de sucesso e exemplos.
- **Códigos de status:** 200/201/400/401/403/404/409/422/500 e quando ocorrem.
- **Erros:** formato de erro e mensagens.
- **Idempotência / paginação / rate limit:** quando aplicável.

## Contratos e tipos
Modelos de dados de entrada/saída (DTOs).

## Regras de negócio aplicadas
Referência às RN do validation-rules-spec.

## Banco
Tabelas/coleções lidas e gravadas. Detalhe no database-spec. `N/A` + motivo.

## Integrações externas
Serviços de terceiros, webhooks, filas.

## Segurança
Authz/authn, validação de input, dados sensíveis, segredos (validar com security-standard).

## Observabilidade/logs
Logs, métricas, tracing e auditoria esperados.

## Testes
Casos obrigatórios: sucesso, erro, autorização, borda.

## Performance
Latência esperada, volume, caching.

## Riscos
Quebra de contrato, regressão, compatibilidade.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Critérios objetivos e testáveis do backend.

## Referências e decisão de fontes

Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando a consulta global do Harness.
