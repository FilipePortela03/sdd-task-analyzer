# 3. Governança de Contexto e Regras para Agentes de IA (CONTEXT_RULES)

## 3.1 Diretrizes Arquiteturais Obrigatórias

1. **Python 3.11+** obrigatório em todo o código gerado.
2. **Type hints** em 100% das funções, métodos e atributos de classes (incluindo tipos de retorno).
3. **Princípio da Responsabilidade Única (SRP):** cada função/classe deve ter um único motivo para mudar; funções de cálculo, validação e formatação devem ser separadas.
4. **PEP 8** integralmente respeitado (nomes, indentação, comprimento de linha ≤ 99 caracteres).
5. **Docstrings** no padrão Google style em todos os módulos, classes e funções públicas, incluindo `Args`, `Returns` e `Raises`.
6. **Funções pequenas e coesas:** recomenda-se no máximo ~25 linhas por função; se ultrapassar, deve ser decomposta.
7. **Tratamento de exceções específico:** nunca usar `except Exception` genérico sem re-lançamento ou log; exceções customizadas (ex.: `DataInvalidaError`) devem herdar de `Exception` e ter mensagens claras e acionáveis.
8. **Logs estruturados** via módulo `logging` (nunca `print()`), com níveis apropriados (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
9. **Nomes descritivos:** proibido nomes genéricos como `x`, `data`, `temp`, `foo` em variáveis de lógica de negócio.
10. **Imutabilidade de entrada:** funções de análise não devem alterar a lista/dicionário de tarefas recebida como parâmetro.
11. **Sem estado global mutável:** o módulo não deve usar variáveis globais para armazenar resultados intermediários.

## 3.2 Proibições Explícitas

O agente de IA que gerar código a partir desta especificação não pode:

1. Utilizar bibliotecas externas não listadas em `requirements.txt` e não previamente autorizadas.
2. Alterar, remover ou "simplificar" os cenários de teste definidos na seção 2.1 e seus asserts.
3. Modificar a estrutura de pastas definida na seção 4.1 sem justificativa documentada e aprovação humana.
4. Persistir dados em arquivos, bancos de dados, cache em disco ou qualquer meio externo.
5. Alterar a assinatura de funções públicas (nome, parâmetros, tipos, ordem) definidas neste contrato sem autorização explícita do responsável humano.
6. Gerar qualquer função ou classe sem o teste automatizado correspondente.
7. Inserir código duplicado, morto ou trechos comentados "para depois".
8. Assumir comportamentos, regras de negócio ou formatos de dado não especificados neste documento — em caso de ambiguidade, o agente deve sinalizar a dúvida em vez de inferir silenciosamente.
9. Introduzir dependências de rede, chamadas de API externas ou operações de I/O não previstas no escopo.
10. Gerar código que quebre a cobertura mínima de testes definida (90%).

## 3.3 Regras de Interação com a IA

Ao interagir com o agente de IA nas próximas fases, o(a) desenvolvedor(a) deve:

1. **Fornecer contexto completo:** sempre anexar/colar este documento (`SDD` + `CONTEXT_RULES`) inteiro no início da sessão, nunca fragmentos isolados.
2. **Validar entendimento antes de gerar código:** pedir ao agente que resuma, em suas próprias palavras, o contrato de entrada/saída e as regras de negócio antes de escrever qualquer linha de código.
3. **Solicitar explicações:** para cada função gerada, pedir uma justificativa curta de por que aquela abordagem atende ao contrato e às diretrizes da seção 3.1.
4. **Revisar criticamente:** nunca aceitar código gerado sem leitura linha a linha e sem executar os testes localmente.
5. **Rejeitar respostas fora do contrato:** se o agente propuser mudanças na assinatura de função, novas dependências ou novas regras de negócio não previstas aqui, a resposta deve ser rejeitada e o agente deve ser instruído a se ater estritamente a este documento.
6. **Registrar decisões:** qualquer desvio aprovado deste contrato deve ser documentado em um changelog no próprio `specs/task_analyzer_spec.md`, com data e justificativa.