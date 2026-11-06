# SPEC: Regras de validação e de negócio

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Centraliza regras transversais referenciadas por page/component specs.

## Status
Rascunho | Em revisão | Aprovada

## Contexto
Módulo/tela/feature ao qual estas regras se aplicam.

## Regras de negócio
Lista numerada. Para cada regra:

- **RN-XX:** descrição clara da regra.
  - Condição / gatilho.
  - Resultado esperado.
  - Exceções.

## Regras de validação de entrada
Por campo: formato, obrigatoriedade, limites, máscara e normalização.

## Mensagens
Texto exato de erro/sucesso por regra, quando aplicável.

## Camada de aplicação
Onde cada regra é aplicada e validada:

- **Banco** (constraints, checks). `N/A` + motivo se não houver.
- **API/Backend** (validação de servidor, fonte de verdade).
- **Frontend/UI** (validação imediata, não substitui o backend).

## Casos de borda
Valores limite, vazios, duplicados, concorrência, fuso/locale.

## Testes
Casos obrigatórios para cobrir cada regra (válido e inválido).

## Segurança
Regras com impacto em autorização, privacidade ou integridade de dados.

## Riscos
Conflitos de regras, ambiguidades e regressões possíveis.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Como verificar que as regras foram implementadas corretamente.

## Referências e decisão de fontes

Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando a consulta global do Harness.
