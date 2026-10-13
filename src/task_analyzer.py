"""Módulo de análise de tarefas e produtividade (TaskAnalyzer)."""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Set

from .exceptions import DataInvalidaError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STATUS_PERMITIDOS = {"pendente", "em_andamento", "concluida", "cancelada"}
PRIORIDADES_PERMITIDAS = {"baixa", "media", "alta"}


def analisar_tarefas(tarefas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analisa uma lista de tarefas e retorna métricas de produtividade.

    Args:
        tarefas: Lista de dicionários representando as tarefas.

    Returns:
        Um dicionário contendo o tempo médio de conclusão, taxa de atraso,
        quantidade total de tarefas e os indicadores agrupados por prioridade.
    """
    logger.info("Iniciando análise de %d tarefas", len(tarefas))
    _validar_colecao_tarefas(tarefas)

    concluidas = [t for t in tarefas if t.get("status") == "concluida"]

    resultado = {
        "tempo_medio_conclusao": _calcular_tempo_medio(concluidas),
        "taxa_atraso_percentual": _calcular_taxa_atraso(concluidas),
        "quantidade_tarefas": len(tarefas),
        "indicadores_por_prioridade": _agrupar_indicadores_por_prioridade(tarefas),
    }

    logger.info("Análise concluída com sucesso.")
    return resultado


def _validar_colecao_tarefas(tarefas: List[Dict[str, Any]]) -> None:
    """Valida todas as tarefas da lista, verificando duplicidades e regras.

    Args:
        tarefas: Lista de tarefas a serem validadas.
    """
    ids_vistos: Set[str] = set()
    for tarefa in tarefas:
        _validar_campos_basicos(tarefa, ids_vistos)
        _validar_datas_e_status(tarefa)


def _validar_campos_basicos(tarefa: Dict[str, Any], ids_vistos: Set[str]) -> None:
    """Valida IDs, títulos e prioridades de uma tarefa.

    Args:
        tarefa: Dicionário da tarefa.
        ids_vistos: Conjunto de IDs já processados na coleção.

    Raises:
        ValueError: Se houver campos básicos inválidos ou IDs duplicados.
    """
    id_tarefa = tarefa.get("id_tarefa", "")
    if not isinstance(id_tarefa, str) or not id_tarefa.strip():
        raise ValueError("id_tarefa não pode ser vazio.")
    if id_tarefa in ids_vistos:
        raise ValueError(f"id_tarefa duplicado encontrado: {id_tarefa}")
    ids_vistos.add(id_tarefa)

    titulo = tarefa.get("titulo", "")
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError(f"Tarefa {id_tarefa} tem título vazio.")

    prioridade = tarefa.get("prioridade")
    if prioridade not in PRIORIDADES_PERMITIDAS:
        raise ValueError(
            f"Prioridade inválida na tarefa {id_tarefa}: {prioridade}. "
            f"Aceitos: {', '.join(PRIORIDADES_PERMITIDAS)}."
        )


def _validar_datas_e_status(tarefa: Dict[str, Any]) -> None:
    """Valida a consistência de status e regras temporais de datas.

    Args:
        tarefa: Dicionário da tarefa.

    Raises:
        ValueError: Se o status for inválido ou inconsistente.
        DataInvalidaError: Se houver anomalias cronológicas ou falha de parse.
    """
    id_tarefa = tarefa["id_tarefa"]
    status = tarefa.get("status")

    if status not in STATUS_PERMITIDOS:
        raise ValueError(f"Status inválido na tarefa {id_tarefa}: {status}")

    dt_criacao = _parse_data(tarefa.get("data_criacao"), id_tarefa, "data_criacao")
    dt_prazo = _parse_data(tarefa.get("prazo"), id_tarefa, "prazo")
    dt_conclusao = None

    if tarefa.get("data_conclusao"):
        dt_conclusao = _parse_data(
            tarefa.get("data_conclusao"), id_tarefa, "data_conclusao"
        )

    if status == "concluida" and not dt_conclusao:
        raise ValueError(f"Tarefa {id_tarefa} está 'concluida' sem 'data_conclusao'.")

    if dt_conclusao and dt_conclusao < dt_criacao:  # type: ignore
        raise DataInvalidaError(
            f"Na tarefa {id_tarefa}, data_conclusao é anterior à data_criacao."
        )
    if dt_prazo and dt_prazo < dt_criacao:  # type: ignore
        raise DataInvalidaError(
            f"Na tarefa {id_tarefa}, prazo é anterior à data_criacao."
        )


def _parse_data(
    data_str: Optional[str], id_tarefa: str, campo: str
) -> Optional[datetime]:
    """Converte string ISO 8601 UTC para objeto datetime timezone-aware.

    Args:
        data_str: Data em formato string ISO 8601.
        id_tarefa: Identificador da tarefa para mensagens de erro.
        campo: Nome do campo da data para mensagens de erro.

    Returns:
        Objeto datetime ou None se a string original for vazia/nula.

    Raises:
        DataInvalidaError: Se a string não for uma data válida.
    """
    if not data_str:
        return None
    try:
        # Substitui o Z para parse nativo em Python 3.11 (que suporta fromisoformat)
        dt = datetime.fromisoformat(data_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise DataInvalidaError(
                f"Na tarefa {id_tarefa}, {campo} deve ser timezone-aware (UTC)."
            )
        return dt
    except ValueError:
        raise DataInvalidaError(f"Formato inválido em {campo} na tarefa {id_tarefa}.")


def _calcular_tempo_medio(tarefas_concluidas: List[Dict[str, Any]]) -> float:
    """Calcula o tempo médio de conclusão em horas.

    Args:
        tarefas_concluidas: Lista de tarefas com status 'concluida'.

    Returns:
        Média do tempo em horas, arredondada em 2 casas, ou 0.0 se vazia.
    """
    if not tarefas_concluidas:
        return 0.0

    horas_totais = 0.0
    for t in tarefas_concluidas:
        dt_criacao = _parse_data(t["data_criacao"], t["id_tarefa"], "data_criacao")
        dt_conclusao = _parse_data(
            t["data_conclusao"], t["id_tarefa"], "data_conclusao"
        )
        if dt_criacao and dt_conclusao:
            delta = dt_conclusao - dt_criacao
            horas_totais += delta.total_seconds() / 3600.0

    return round(horas_totais / len(tarefas_concluidas), 2)


def _calcular_taxa_atraso(tarefas_concluidas: List[Dict[str, Any]]) -> float:
    """Calcula o percentual de tarefas concluídas após o prazo.

    Args:
        tarefas_concluidas: Lista de tarefas com status 'concluida'.

    Returns:
        Taxa de atraso de 0.0 a 100.0, arredondada em 2 casas.
    """
    if not tarefas_concluidas:
        return 0.0

    atrasadas = 0
    for t in tarefas_concluidas:
        dt_conclusao = _parse_data(
            t["data_conclusao"], t["id_tarefa"], "data_conclusao"
        )
        dt_prazo = _parse_data(t["prazo"], t["id_tarefa"], "prazo")
        if dt_conclusao and dt_prazo and dt_conclusao > dt_prazo:
            atrasadas += 1

    return round((atrasadas / len(tarefas_concluidas)) * 100.0, 2)


def _agrupar_indicadores_por_prioridade(
    tarefas: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Gera indicadores de produtividade segmentados por prioridade.

    Args:
        tarefas: Lista de todas as tarefas da entrada.

    Returns:
        Dicionário com métricas agregadas por 'baixa', 'media' e 'alta'.
    """
    agrupamento = {
        p: {"total_tarefas": 0, "concluidas": []} for p in PRIORIDADES_PERMITIDAS
    }

    for t in tarefas:
        prio = t["prioridade"]
        agrupamento[prio]["total_tarefas"] += 1
        if t.get("status") == "concluida":
            agrupamento[prio]["concluidas"].append(t)

    indicadores = {}
    for prio in PRIORIDADES_PERMITIDAS:
        concluidas = agrupamento[prio]["concluidas"]  # type: ignore
        total = agrupamento[prio]["total_tarefas"]
        indicadores[prio] = {
            "total_tarefas": total,
            "tarefas_concluidas": len(concluidas),
            "tempo_medio_conclusao": _calcular_tempo_medio(concluidas),
            "taxa_atraso_percentual": _calcular_taxa_atraso(concluidas),
        }
    return indicadores
