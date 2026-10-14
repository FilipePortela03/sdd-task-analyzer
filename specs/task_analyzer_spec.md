# TaskAnalyzer — Especificação Executável (SDD)
**Bootcamp III — Fase 1**

## 1. Visão Geral e Contrato de Negócio (SDD)

### 1.1 Identificação
| Item | Informação |
| :--- | :--- |
| **Nome completo** | Filipe Portela Silva |
| **Curso** | Ciência da Computação |
| **Turma**| A |
| **Atividade** | Bootcamp III (75h, EAD) — Projeto Cumulativo, Fase 1/3 |
| **Documento** | Especificação Executável (SDD) + Regras de Governança de IA (CONTEXT_RULES) |
| **Versão do documento** | 1.0.0 |

### 1.2 Propósito do Módulo TaskAnalyzer
O `TaskAnalyzer` é um módulo de análise de tarefas e produtividade que recebe uma coleção de tarefas de um usuário ou equipe e calcula métricas objetivas de desempenho na execução dessas tarefas. O módulo não gerencia estado, não persiste dados e não possui interface de usuário — ele é uma biblioteca de cálculo pura (funções de análise), pensada para ser consumida por outras camadas do sistema (API, CLI, dashboard, etc.) em fases futuras do bootcamp.

**Escopo funcional:**
- Calcular o tempo médio de conclusão das tarefas concluídas.
- Calcular a taxa de atraso percentual (tarefas concluídas após o prazo, em relação ao total de tarefas concluídas).
- Calcular indicadores de produtividade agrupados por prioridade (baixa, média, alta).

**A quem se destina:**
- À própria IA geradora de código (Fase 2), que usará este documento como contrato de interface e comportamento.
- Ao pipeline de CI/CD e à revisão ética/técnica (Fase 3), que validará a conformidade do código gerado com este contrato.
- Ao(à) desenvolvedor(a)/avaliador(a) humano(a), como fonte única de verdade sobre o comportamento esperado do sistema.

**Fora de escopo (explicitamente):**
- Persistência de dados (banco de dados, arquivos, cache).
- Autenticação, autorização ou multiusuário.
- Interface gráfica ou API HTTP (poderão ser tratadas em fases futuras, fora deste contrato).
- Notificações, alertas ou integrações externas.

### 1.3 Contrato Executável de Interface

#### 1.3.1 Tabela de ENTRADAS
Cada tarefa é um objeto/dicionário com os seguintes campos:

| Campo | Tipo | Obrigatório | Descrição / Restrição |
| :--- | :--- | :--- | :--- |
| `id_tarefa` | str | Sim | Identificador único da tarefa. Não pode ser vazio nem duplicado dentro da mesma lista. |
| `titulo` | str | Sim | Título descritivo da tarefa. Não pode ser string vazia após strip(). |
| `prioridade` | str | Sim | Um dos valores: "baixa", "media", "alta". Qualquer outro valor gera ValueError. |
| `data_criacao` | str (ISO 8601, UTC) | Sim | Data/hora de criação da tarefa. Deve ser anterior ou igual a `data_conclusao` (quando existir) e a `prazo`. |
| `data_conclusao` | str (ISO 8601, UTC) ou None | Não | Data/hora em que a tarefa foi concluída. `None` significa tarefa não concluída. |
| `prazo` | str (ISO 8601, UTC) | Sim | Data/hora limite estipulada para conclusão da tarefa. |
| `status` | str | Sim | Um dos valores: "pendente", "em_andamento", "concluida", "cancelada". Deve ser consistente com `data_conclusao`. |

*(A entrada completa da função principal de análise é uma lista de objetos com essa estrutura: `list[dict]`)*

#### 1.3.2 Tabela de SAÍDAS
O resultado da análise é um objeto/dicionário estruturado com, no mínimo, os seguintes campos:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `tempo_medio_conclusao` | float (horas) | Média do tempo decorrido entre criação e conclusão, em horas. 0.0 se não houver tarefas concluídas. |
| `taxa_atraso_percentual` | float (0–100) | Percentual de tarefas concluídas após o prazo. 0.0 se não houver tarefas concluídas. |
| `quantidade_tarefas` | int | Quantidade total de tarefas recebidas na entrada (concluídas ou não). |
| `indicadores_por_prioridade`| dict[str, dict] | Dicionário com chaves "baixa", "media", "alta", cada uma contendo: `total_tarefas`, `tarefas_concluidas`, `tempo_medio_conclusao` e `taxa_atraso_percentual`. |

#### 1.3.3 Regras de Negócio e Restrições
1. Apenas tarefas com status == "concluida" e `data_conclusao` preenchida entram no cálculo de tempo médio e atraso.
2. Datas inválidas devem lançar uma exceção específica e nomeada (ex.: `DataInvalidaError`), nunca uma exceção genérica.
3. Nenhuma divisão deve ocorrer sem checagem prévia do denominador (evitar divisão por zero).
4. Todas as datas devem ser tratadas como UTC (timezone-aware).
5. Toda saída numérica deve ser arredondada para 2 casas decimais.
6. A função principal não deve ter efeitos colaterais (não deve alterar a lista de entrada — tratá-la como somente leitura).
7. Prioridades ou status fora do vocabulário controlado devem gerar `ValueError`.

## 2. Especificação de Cenários de Aceite e Test Harness

### 2.1 Cenários de Teste (Dado–Quando–Então)

*   **Cenário 1 — SUCESSO: cálculo correto com conjunto válido de tarefas**
    *   **Dado** uma lista com 4 tarefas concluídas, com prioridades variadas e datas consistentes, sendo 1 concluída após o prazo.
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** o resultado deve conter tempo médio correto, taxa de atraso de 25.0, quantidade igual a 4, e indicadores corretos por grupo.

*   **Cenário 2 — EXCEÇÃO: data inválida gera erro específico**
    *   **Dado** uma tarefa com `data_conclusao` anterior à `data_criacao`.
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** o sistema deve lançar a exceção `DataInvalidaError`.

*   **Cenário 3 — BORDA: lista vazia de tarefas**
    *   **Dado** uma lista vazia de tarefas.
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** o resultado deve conter métricas zeradas, sem lançar exceções.

*   **Cenário 4 — BORDA: todas as tarefas atrasadas**
    *   **Dado** uma lista de 3 tarefas concluídas, todas com data_conclusao > prazo.
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** taxa_atraso_percentual deve ser igual a 100.0.

*   **Cenário 5 — BORDA: prioridade ausente ou inválida**
    *   **Dado** uma tarefa com prioridade "urgente".
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** o sistema deve lançar `ValueError`.

*   **Cenário 6 — BORDA: tarefas sem data_conclusao misturadas com concluídas**
    *   **Dado** uma lista com 2 tarefas concluídas e 2 pendentes.
    *   **Quando** a função analisar_tarefas() é chamada.
    *   **Então** quantidade_tarefas deve ser 4, mas métricas de tempo calculadas apenas sobre as 2 concluídas.

### 2.2 Planejamento do Test Harness (pytest)

| Cenário | Função de teste sugerida | Fixtures necessárias | Asserts esperados |
| :--- | :--- | :--- | :--- |
| **1 — Sucesso** | `test_analisar_tarefas_retorna_metricas_corretas` | `fixture_tarefas_validas` | `resultado["quantidade_tarefas"] == 4`, `taxa_atraso_percentual == 25.0` |
| **2 — Exceção** | `test_analisar_tarefas_data_conclusao_anterior_criacao` | `fixture_tarefa_data_invalida` | `with pytest.raises(DataInvalidaError):` |
| **3 — Lista vazia** | `test_analisar_tarefas_lista_vazia_retorna_zerados` | (lista `[]` inline) | `quantidade_tarefas == 0`, chaves presentes e zeradas |
| **4 — Atrasadas** | `test_analisar_tarefas_todas_atrasadas_retorna_100` | `fixture_tarefas_todas_atrasadas` | `taxa_atraso_percentual == 100.0` |
| **5 — Prio. inválida**| `test_analisar_tarefas_prioridade_invalida` | `fixture_tarefa_prioridade_invalida`| `with pytest.raises(ValueError, match="prioridade"):` |
| **6 — Mistas** | `test_analisar_tarefas_ignora_pendentes_no_calculo` | `fixture_tarefas_mistas` | `quantidade_tarefas == 4`, tempo médio > 0 |

**Observações de implementação:**
- Todas as fixtures devem residir em `tests/conftest.py`.
- Nenhum teste deve depender de `datetime.now()` — todas as datas devem ser fixas.
- Cobertura mínima exigida: 90% para o módulo `src/task_analyzer.py`.