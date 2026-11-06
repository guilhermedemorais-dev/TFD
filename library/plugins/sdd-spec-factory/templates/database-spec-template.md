# SPEC: Banco de dados - Nome do escopo

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Crie apenas quando houver impacto em banco. Não invente schema existente (`HIPÓTESE:`).

## Status
Rascunho | Em revisão | Aprovada

## Objetivo
Que dado este escopo precisa armazenar/alterar e por quê.

## Contexto
Módulo/feature e specs relacionadas.

## Tabelas/coleções
Para cada tabela (nova ou alterada):

- **Nome:** `tabela`
- **Tipo de mudança:** nova | alteração | remoção (justificar remoção).
- **Colunas/campos:** nome, tipo, nulo?, default, descrição.
- **Chave primária:** ...
- **Chaves estrangeiras:** ... e ação ON DELETE/UPDATE.
- **Índices:** quais e por quê.
- **Constraints/checks:** unicidade, validação no nível do banco.

## Relacionamentos
Como as entidades se relacionam (1:1, 1:N, N:N).

## Migrações
Estratégia: criação, alteração, backfill, ordem e reversão (down).

## Compatibilidade e dados existentes
Impacto em dados atuais, migração de dados, breaking changes.

## Multi-tenant / isolamento
Como o dado é isolado por tenant/usuário, quando aplicável.

## Segurança e privacidade
Dados pessoais/sensíveis, criptografia, retenção, mascaramento (validar com security-standard).

## Performance
Volume esperado, crescimento, particionamento/índices.

## Observabilidade
Auditoria, soft delete, timestamps, rastreamento de alterações.

## Testes
Validação de migração, rollback e integridade referencial.

## Riscos
Perda de dados, lock, downtime, regressão.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Critérios objetivos e testáveis do banco.

## Referências e decisão de fontes

Registro de consulta: índices/metadados dos catálogos aplicáveis e revisão
consultados; ID da fonte escolhida ou reuso nativo; ou N/A com justificativa.
Evidência indisponível/desatualizada: NOT_VALIDATED, sem inventar consulta.
Consultar metadados não exige ler todas as fontes; somente fontes selecionadas
necessárias seguem como REQUIRED, preservando a consulta global do Harness.
