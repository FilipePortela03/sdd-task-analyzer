<div align="center">

# 📊 SDD Task Analyzer

**Módulo Python para análise de métricas de produtividade e processamento de tarefas, guiado por Spec-Driven Development.**

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![Testes](https://img.shields.io/badge/testes-pytest-0A9EDC?logo=pytest&logoColor=white)
![Cobertura](https://img.shields.io/badge/cobertura-98%25-brightgreen)
![Code style](https://img.shields.io/badge/code%20style-black-000000)
![Linter](https://img.shields.io/badge/linter-ruff-D7FF64)

</div>

---

## 📑 Sumário

- [Visão Geral](#-visão-geral)
- [Arquitetura do Repositório](#️-arquitetura-do-repositório)
- [Pré-requisitos](#️-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Testes e Cobertura](#-testes-e-cobertura-homologação-dinâmica)
- [Qualidade Estática](#️-qualidade-estática-homologação-estática)
- [Autor](#-autor)

---

## 📖 Visão Geral

O **Task Analyzer** é um módulo Python desenvolvido para analisar métricas de produtividade e processamento de tarefas, seguindo estritamente as especificações do Contrato de Negócio (SDD) e as regras de governança de IA definidas em [`CONTEXT_RULES.md`](CONTEXT_RULES.md).

Este projeto faz parte da avaliação da **Fase 2**, com foco em:

- ✅ Boas práticas de engenharia de software
- ✅ Qualidade estática de código (Clean Code)
- ✅ Alta cobertura de testes automatizados

---

## 🏗️ Arquitetura do Repositório

A estrutura de diretórios foi implementada exatamente conforme a arquitetura aprovada na Fase 1:

```text
sdd-task-analyzer/
├── CONTEXT_RULES.md          # Regras de governança e restrições técnicas (IA)
├── README.md                 # Documentação principal do projeto
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git (ex: __pycache__)
├── specs/
│   └── task_analyzer_spec.md # Especificação executável completa (Contrato SDD)
├── src/
│   ├── __init__.py           # Define 'src' como um pacote Python
│   ├── task_analyzer.py      # Implementação principal da análise de tarefas
│   └── exceptions.py         # Exceções customizadas (ex: DataInvalidaError)
└── tests/
    ├── __init__.py           # Define 'tests' como um pacote Python
    ├── conftest.py           # Fixtures compartilhadas para os testes
    └── test_harness.py       # Casos de teste automatizados (pytest)
```

---

## ⚙️ Pré-requisitos

| Requisito | Versão    | Finalidade                       |
|-----------|-----------|----------------------------------|
| Python    | 3.11+     | Execução do módulo e dos testes  |
| Git       | qualquer  | Clonagem e controle de versões   |

---

## 🚀 Instalação e Configuração

**1. Clone o repositório:**

```bash
git clone https://github.com/FilipePortela03/sdd-task-analyzer.git
cd sdd-task-analyzer
```

**2. (Recomendado) Crie e ative um ambiente virtual:**

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
```

---

## 🧪 Testes e Cobertura (Homologação Dinâmica)

O projeto conta com **98% de cobertura de testes**, validando com sucesso os cenários ideais e os casos de borda estipulados no contrato SDD.

Para executar os testes e gerar o relatório de cobertura no terminal:

```bash
python -m pytest --cov=src --cov-report term-missing
```

---

## 🛠️ Qualidade Estática (Homologação Estática)

O código foi submetido a um processo de curadoria rigoroso para garantir o cumprimento das diretrizes da PEP-8 e a eliminação de importações não utilizadas.

| Ferramenta | Objetivo                  | Comando                                |
|------------|---------------------------|----------------------------------------|
| **Black**  | Verificação de formatação | `python -m black --check src tests`    |
| **Ruff**   | Análise de linting        | `python -m ruff check src tests`       |

---

## 👤 Autor
**Filipe Portela Silva**

Projeto desenvolvido para homologação técnica e avaliação de arquitetura de software orientada a especificações rigorosas (*Spec-Driven Development*).