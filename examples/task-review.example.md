<h1>DEMO-001 · Normalizar nome no cadastro de pessoas</h1>

<p><strong>Revisão</strong> · r1 · draft</p>

<p><strong>JSON canônico</strong> · task.example.json</p>

<p><strong>SHA-256 do JSON</strong> · d1704f84e3e7ede63511d8342aacd7bc0dd7b6cfcf5027f92ab1e1f19179e327</p>

<details open>
<summary>Checklist para aprovar a Task</summary>

<p>Registre o aceite ou os ajustes na Issue vinculada e identifique a revisão.</p>

- [ ] Conferi a revisão da Task, da spec e do Discovery.
- [ ] Conferi o QA independente e as evidências aplicáveis a esta revisão.
- [ ] Revisei as microtarefas, os responsáveis, as dependências e os entregáveis.
- [ ] Conferi os critérios de aceite, as regras de negócio e os testes previstos.
- [ ] Conferi os caminhos permitidos, as restrições e as condições de parada.
- [ ] Identifiquei as pendências que afetam meu aceite.

```mermaid
flowchart LR
    A[Entrega] --> B[QA independente]
    B -->|PASS| C[Revisão humana]
    B -->|REWORK| D[Correção]
    C -->|Ajustes| D
    D --> B
    C -->|Aceite| E[Registrar na Issue]
```

</details>

<details>
<summary>Pareceres e evidências da revisão</summary>

<p><strong>QA registrado no workflow</strong> · Nenhum registrado.</p>

</details>

<details>
<summary>Escopo, restrições e fases</summary>

<p><strong>Objetivo</strong> · Aceitar nome com acento, caixa variada e espaço duplicado sem quebrar a busca do cadastro.</p>
<p><strong>Complexidade</strong> · normal</p>
<p><strong>Escopo</strong></p><ul><li>normalização de nome no cadastro de pessoas</li></ul>
<p><strong>Fora do escopo</strong></p><ul><li>busca global</li><li>migração de dados existentes</li></ul>
<p><strong>Caminhos permitidos na Task</strong></p><ul><li>src/cadastro/**</li><li>tests/test_cadastro.py</li></ul>
<p><strong>Caminhos protegidos</strong></p><ul><li>migrations/**</li><li>.github/**</li></ul>
<p><strong>Condições de parada</strong></p><ul><li>escopo cresceu além de src/cadastro</li><li>contrato conflita com o comportamento atual</li><li>teste exige banco não disponível</li></ul>
<p><strong>Gates</strong></p><ul><li>implementation · testes verdes e diff dentro de allowed_paths</li><li>review · qa_backend valida independente</li><li>merge · aprovação humana no PR</li></ul>
<p><strong>Estimativa</strong> · 2 / 4 / 8 h (otimista / provável / pessimista) · low · sem histórico medido deste módulo; faixa por analogia</p>

</details>

<details>
<summary>Regras, critérios, testes e referências técnicas</summary>

<p><strong>Requisitos</strong></p><ul><li>REQ-01 · Nome com acento é normalizado para forma comparável. · MUST · docs/prd/cadastro.md#nome</li><li>REQ-02 · Nome vazio ou só com espaços retorna erro de validação. · MUST · docs/prd/cadastro.md#validacao</li></ul>
<p><strong>Regras de negócio</strong></p><ul><li>RULE-01 · O nome original é preservado para exibição; a forma normalizada serve à busca. · docs/prd/cadastro.md#regras</li></ul>
<p><strong>Critérios de aceite</strong></p><ul><li>AC-01 · Nome &#x27;  João   da  Silva &#x27; é aceito e buscável como &#x27;joao da silva&#x27;. · REQ-01 · TEST-01 · MT-01, MT-02</li><li>AC-02 · Nome vazio retorna erro de validação, não grava registro. · REQ-02 · TEST-02 · MT-01, MT-02</li></ul>
<p><strong>TEST-01</strong> · unit</p>
<p><strong>Comando ou procedimento</strong> · python -m unittest tests.test_cadastro -q</p>
<p><strong>Resultado esperado</strong> · exit 0 com os casos de normalização</p>
<p><strong>TEST-02</strong> · unit</p>
<p><strong>Comando ou procedimento</strong> · python -m unittest tests.test_cadastro -q</p>
<p><strong>Resultado esperado</strong> · exit 0 com o caso de nome vazio</p>
<h3>Referências técnicas</h3><ul><li>REF-01 · docs/specs/cadastro/spec.md · Contrato de normalização e casos de borda aprovados.</li></ul>

</details>

<details open>
<summary>Microtarefas</summary>

<details>
<summary>MT-01 · Implementar normalização e validação</summary>

<p><strong>Decisão humana · marque uma opção</strong> · </p>

- [ ] Aprovado
- [ ] Reprovado

<p><strong>Responsável e validador independente</strong> · @TFD-backend · @TFD-qa_backend</p>
<p><strong>Depende de</strong> · livre</p>
<p><strong>Caminhos permitidos</strong></p><ul><li>src/cadastro/**</li></ul>
<p><strong>Não pode</strong> · Editar fora da lista da microtarefa ou em caminhos protegidos, ampliar o escopo ou contornar gates. Consulte Escopo, restrições e fases.</p>
<p><strong>Checklist de execução</strong> · </p>

- [ ] escrever teste que falha sem a normalização
- [ ] implementar a menor mudança que passa
- [ ] rodar o teste de contrato

<p><strong>Entregáveis</strong></p><ul><li>src/cadastro/normalize.py</li></ul>
<p><strong>Concluído quando</strong> · Teste de contrato verde e nome original preservado</p>
<p><strong>Critérios, testes e requisitos vinculados</strong></p><ul><li>AC-01 · TEST-01 · REQ-01</li><li>AC-02 · TEST-02 · REQ-02</li></ul>
<p><strong>Referências da microtarefa</strong> · Consulte as referências da Task.</p>
<p><strong>Checkpoint de execução</strong> · Sem registro nesta visão.</p>
<p><strong>QA independente</strong> · Sem parecer de execução nesta visão.</p>

</details>

<details>
<summary>MT-02 · Cobrir casos de borda no teste</summary>

<p><strong>Decisão humana · marque uma opção</strong> · </p>

- [ ] Aprovado
- [ ] Reprovado

<p><strong>Responsável e validador independente</strong> · @TFD-backend · @TFD-qa_backend</p>
<p><strong>Depende de</strong> · MT-01</p>
<p><strong>Caminhos permitidos</strong></p><ul><li>tests/test_cadastro.py</li></ul>
<p><strong>Não pode</strong> · Editar fora da lista da microtarefa ou em caminhos protegidos, ampliar o escopo ou contornar gates. Consulte Escopo, restrições e fases.</p>
<p><strong>Checklist de execução</strong> · </p>

- [ ] cobrir acento, caixa e espaço duplicado
- [ ] cobrir vazio e só espaços

<p><strong>Entregáveis</strong></p><ul><li>tests/test_cadastro.py</li></ul>
<p><strong>Concluído quando</strong> · Todos os casos de borda cobertos e verdes</p>
<p><strong>Critérios, testes e requisitos vinculados</strong></p><ul><li>AC-01 · TEST-01 · REQ-01</li><li>AC-02 · TEST-02 · REQ-02</li></ul>
<p><strong>Referências da microtarefa</strong> · Consulte as referências da Task.</p>
<p><strong>Checkpoint de execução</strong> · Sem registro nesta visão.</p>
<p><strong>QA independente</strong> · Sem parecer de execução nesta visão.</p>

</details>

</details>
