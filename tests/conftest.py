"""Fixtures compartilhadas para os testes do TaskAnalyzer."""

import pytest
from typing import List, Dict, Any


@pytest.fixture
def fixture_tarefas_validas() -> List[Dict[str, Any]]:
    """Retorna 4 tarefas concluídas válidas (1 entregue com atraso)."""
    return [
        {
            "id_tarefa": "T1",
            "titulo": "Tarefa 1",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-01T12:00:00Z",  # 2h
            "prazo": "2026-09-02T10:00:00Z",
            "status": "concluida",
        },
        {
            "id_tarefa": "T2",
            "titulo": "Tarefa 2",
            "prioridade": "alta",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-01T15:00:00Z",  # 5h
            "prazo": "2026-09-02T10:00:00Z",
            "status": "concluida",
        },
        {
            "id_tarefa": "T3",
            "titulo": "Tarefa 3",
            "prioridade": "media",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-01T11:00:00Z",  # 1h
            "prazo": "2026-09-02T10:00:00Z",
            "status": "concluida",
        },
        {
            "id_tarefa": "T4",
            "titulo": "Tarefa Atrasada",
            "prioridade": "alta",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-05T14:00:00Z",  # 100h (Atrasada)
            "prazo": "2026-09-04T10:00:00Z",
            "status": "concluida",
        },
    ]


@pytest.fixture
def fixture_tarefa_data_invalida() -> List[Dict[str, Any]]:
    """Retorna lista contendo tarefa com data de conclusão anterior à criação."""
    return [
        {
            "id_tarefa": "T5",
            "titulo": "Anomalia Temporal",
            "prioridade": "baixa",
            "data_criacao": "2026-09-05T10:00:00Z",
            "data_conclusao": "2026-09-01T10:00:00Z",  # Erro: conclusão anterior
            "prazo": "2026-09-10T10:00:00Z",
            "status": "concluida",
        }
    ]


@pytest.fixture
def fixture_tarefas_todas_atrasadas() -> List[Dict[str, Any]]:
    """Retorna 3 tarefas concluídas com data_conclusao > prazo."""
    base = {
        "titulo": "Atrasada",
        "prioridade": "media",
        "data_criacao": "2026-09-01T10:00:00Z",
        "prazo": "2026-09-02T10:00:00Z",
        "data_conclusao": "2026-09-05T10:00:00Z",
        "status": "concluida",
    }
    return [
        {**base, "id_tarefa": "T6"},
        {**base, "id_tarefa": "T7"},
        {**base, "id_tarefa": "T8"},
    ]


@pytest.fixture
def fixture_tarefa_prioridade_invalida() -> List[Dict[str, Any]]:
    """Retorna lista com uma tarefa contendo prioridade fora do vocabulário."""
    return [
        {
            "id_tarefa": "T9",
            "titulo": "Prioridade Errada",
            "prioridade": "urgente",  # Erro
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-02T10:00:00Z",
            "prazo": "2026-09-10T10:00:00Z",
            "status": "concluida",
        }
    ]


@pytest.fixture
def fixture_tarefas_mistas() -> List[Dict[str, Any]]:
    """Retorna 2 tarefas concluídas e 2 pendentes (sem data_conclusao)."""
    return [
        {
            "id_tarefa": "T10",
            "titulo": "T Concluida 1",
            "prioridade": "alta",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-01T12:00:00Z",  # 2h
            "prazo": "2026-09-10T10:00:00Z",
            "status": "concluida",
        },
        {
            "id_tarefa": "T11",
            "titulo": "T Concluida 2",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": "2026-09-01T14:00:00Z",  # 4h
            "prazo": "2026-09-10T10:00:00Z",
            "status": "concluida",
        },
        {
            "id_tarefa": "T12",
            "titulo": "T Pendente 1",
            "prioridade": "media",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": None,
            "prazo": "2026-09-10T10:00:00Z",
            "status": "pendente",
        },
        {
            "id_tarefa": "T13",
            "titulo": "T Pendente 2",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "data_conclusao": None,
            "prazo": "2026-09-10T10:00:00Z",
            "status": "em_andamento",
        },
    ]


@pytest.fixture
def fixture_tarefa_id_vazio() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa sem ID preenchido."""
    return [
        {
            "id_tarefa": "",
            "titulo": "A",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "prazo": "2026-09-02T10:00:00Z",
            "status": "pendente",
        }
    ]


@pytest.fixture
def fixture_tarefas_id_duplicado() -> List[Dict[str, Any]]:
    """Retorna lista com duas tarefas com o mesmo ID."""
    base = {
        "titulo": "A",
        "prioridade": "baixa",
        "data_criacao": "2026-09-01T10:00:00Z",
        "prazo": "2026-09-02T10:00:00Z",
        "status": "pendente",
    }
    return [{**base, "id_tarefa": "T1"}, {**base, "titulo": "B", "id_tarefa": "T1"}]


@pytest.fixture
def fixture_tarefa_titulo_vazio() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa cujo título contém apenas espaços."""
    return [
        {
            "id_tarefa": "T2",
            "titulo": "   ",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "prazo": "2026-09-02T10:00:00Z",
            "status": "pendente",
        }
    ]


@pytest.fixture
def fixture_tarefa_status_invalido() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa contendo status fora do permitido."""
    return [
        {
            "id_tarefa": "T3",
            "titulo": "A",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "prazo": "2026-09-02T10:00:00Z",
            "status": "aguardando",
        }
    ]


@pytest.fixture
def fixture_tarefa_concluida_sem_data() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa marcada como concluída, mas sem data_conclusao."""
    return [
        {
            "id_tarefa": "T4",
            "titulo": "A",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00Z",
            "prazo": "2026-09-02T10:00:00Z",
            "status": "concluida",
        }
    ]


@pytest.fixture
def fixture_tarefa_formato_data_invalido() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa contendo string de data que não é ISO 8601."""
    return [
        {
            "id_tarefa": "T5",
            "titulo": "A",
            "prioridade": "baixa",
            "data_criacao": "01/09/2026 10:00",
            "prazo": "2026-09-02T10:00:00Z",
            "status": "pendente",
        }
    ]


@pytest.fixture
def fixture_tarefa_data_sem_tz() -> List[Dict[str, Any]]:
    """Retorna lista com tarefa contendo data sem fuso horário (naive)."""
    return [
        {
            "id_tarefa": "T6",
            "titulo": "A",
            "prioridade": "baixa",
            "data_criacao": "2026-09-01T10:00:00",
            "prazo": "2026-09-02T10:00:00",
            "status": "pendente",
        }
    ]
