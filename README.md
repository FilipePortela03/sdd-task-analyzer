<div align="center">

# 📊 SDD Task Analyzer

**Módulo Python para análise de métricas de produtividade, orquestrado com Docker e guiado por Spec-Driven Development.**

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![Testes](https://img.shields.io/badge/testes-pytest-0A9EDC?logo=pytest&logoColor=white)
![Cobertura](https://img.shields.io/badge/cobertura-100%25-brightgreen)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerizado-2496ED?logo=docker&logoColor=white)

</div>

---

## 📑 Sumário

- [Visão Geral](#-visão-geral)
- [Arquitetura do Repositório](#️-arquitetura-do-repositório)
- [Pré-requisitos](#️-pré-requisitos)
- [Instalação e Execução (Docker)](#-instalação-e-execução-docker)
- [Testes e Cobertura](#-testes-e-cobertura-homologação-dinâmica)
- [Qualidade Estática](#️-qualidade-estática-homologação-estática)
- [Autor](#-autor)

---

## 📖 Visão Geral

O **Task Analyzer** é um módulo Python desenvolvido para analisar métricas de produtividade e processamento de tarefas, seguindo estritamente as especificações do Contrato de Negócio (SDD) e as regras de governança de IA definidas em [`CONTEXT_RULES.md`](CONTEXT_RULES.md).

Este projeto faz parte da avaliação final da **Fase 3**, consolidando:

- ✅ Boas práticas de engenharia de software e Clean Code.
- ✅ **100% de cobertura** de testes automatizados.
- ✅ Esteira de Integração Contínua (CI/CD) via GitHub Actions.
- ✅ Isolamento e reprodutibilidade de ambiente via Docker.

---

## 🏗️ Arquitetura do Repositório

A estrutura foi expandida para suportar DevOps e containerização:

```text
sdd-task-analyzer/
├── .github/workflows/
│   └── ci.yml                # Esteira de CI/CD (GitHub Actions)
├── CONTEXT_RULES.md          # Regras de governança e restrições técnicas (IA)
├── Dockerfile                # Receita de containerização (python:3.11-slim)
├── docker-compose.yml        # Orquestração do ambiente de testes
├── README.md                 # Documentação principal do projeto
├── requirements.txt          # Dependências do projeto
├── specs/
│   └── task_analyzer_spec.md # Especificação executável completa (Contrato SDD)
├── src/
│   ├── __init__.py           # Define 'src' como um pacote Python
│   ├── task_analyzer.py      # Implementação principal da análise de tarefas
│   └── exceptions.py         # Exceções customizadas
└── tests/
    ├── conftest.py           # Fixtures compartilhadas para os testes
    └── test_harness.py       # Casos de teste automatizados (pytest)
```

---

## ⚙️ Pré-requisitos

| Requisito | Versão | Finalidade |
| :--- | :--- | :--- |
| **Git** | qualquer | Clonagem e controle de versões |
| **Docker** | Desktop | Execução isolada eliminando falhas locais |
| **Python** | 3.11+ | (Opcional) Execução local sem container |

---

## 🚀 Instalação e Execução (Docker)

A forma recomendada de executar o projeto é através do Docker, garantindo um ambiente idêntico ao da homologação em CI/CD.

**1. Clone o repositório:**

```bash
git clone https://github.com/FilipePortela03/sdd-task-analyzer.git
cd sdd-task-analyzer
```

**2. Execute a suíte de testes isolada:**

```bash
docker compose build
docker compose run test-runner
```

---

## 🧪 Testes e Cobertura (Homologação Dinâmica)

O projeto atingiu a marca de **100% de cobertura** de testes, validando com sucesso todos os **15 cenários** ideais e de borda exigidos.

Para executar localmente (sem Docker) e gerar o relatório no terminal:

```bash
python -m pytest --cov=src --cov-report term-missing
```

---

## 🛠️ Qualidade Estática (Homologação Estática)

O código cumpre as diretrizes da **PEP-8** e passa por curadoria contínua automatizada.

| Ferramenta | Comando (Ambiente Virtual Local) |
| :--- | :--- |
| **Black** | `python -m black --check src tests` |
| **Ruff** | `python -m ruff check src tests` |

---

## 👤 Autor

**Filipe Portela Silva**

Projeto desenvolvido para homologação técnica, governança de IA e arquitetura de software orientada a especificações rigorosas (Spec-Driven Development).