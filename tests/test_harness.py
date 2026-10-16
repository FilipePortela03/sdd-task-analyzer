"""Testes automatizados cobrindo os cenários de aceite do TaskAnalyzer."""

import pytest
from src.task_analyzer import analisar_tarefas
from src.exceptions import DataInvalidaError


def test_analisar_tarefas_retorna_metricas_corretas(fixture_tarefas_validas):
    """Cenário 1 - SUCESSO: cálculo correto com conjunto válido de tarefas."""
    resultado = analisar_tarefas(fixture_tarefas_validas)

    assert resultado["quantidade_tarefas"] == 4
    assert resultado["taxa_atraso_percentual"] == 25.0
    assert isinstance(resultado["tempo_medio_conclusao"], float)
    # Média: (2h + 5h + 1h + 100h) / 4 = 108 / 4 = 27.0h
    assert resultado["tempo_medio_conclusao"] == 27.0

    # Valida presença das prioridades
    indicadores = resultado["indicadores_por_prioridade"]
    assert set(indicadores.keys()) == {"baixa", "media", "alta"}
    assert indicadores["alta"]["total_tarefas"] == 2
    assert indicadores["baixa"]["total_tarefas"] == 1


def test_analisar_tarefas_data_conclusao_anterior_criacao_lanca_erro(
    fixture_tarefa_data_invalida,
):
    """Cenário 2 - EXCEÇÃO: data inválida gera erro específico."""
    with pytest.raises(DataInvalidaError) as exc_info:
        analisar_tarefas(fixture_tarefa_data_invalida)

    assert "T5" in str(exc_info.value)
    assert "data_conclusao" in str(exc_info.value) or "anterior" in str(exc_info.value)


def test_analisar_tarefas_lista_vazia_retorna_zerados():
    """Cenário 3 - BORDA: lista vazia de tarefas não quebra a execução."""
    resultado = analisar_tarefas([])

    assert resultado["quantidade_tarefas"] == 0
    assert resultado["tempo_medio_conclusao"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0
    assert set(resultado["indicadores_por_prioridade"].keys()) == {
        "baixa",
        "media",
        "alta",
    }

    # Verifica que as chaves internas por prioridade também existem zeradas
    assert resultado["indicadores_por_prioridade"]["baixa"]["total_tarefas"] == 0


def test_analisar_tarefas_todas_atrasadas_retorna_100_porcento(
    fixture_tarefas_todas_atrasadas,
):
    """Cenário 4 - BORDA: todas as tarefas concluídas estão atrasadas."""
    resultado = analisar_tarefas(fixture_tarefas_todas_atrasadas)

    assert resultado["taxa_atraso_percentual"] == 100.0


def test_analisar_tarefas_prioridade_invalida_lanca_erro(
    fixture_tarefa_prioridade_invalida,
):
    """Cenário 5 - BORDA: prioridade fora do vocabulário controlado."""
    with pytest.raises(ValueError, match="Prioridade inválida"):
        analisar_tarefas(fixture_tarefa_prioridade_invalida)


def test_analisar_tarefas_ignora_pendentes_no_calculo_de_tempo(fixture_tarefas_mistas):
    """Cenário 6 - MISTURA: tarefas sem data de conclusão ignoradas nas médias/taxas."""
    resultado = analisar_tarefas(fixture_tarefas_mistas)

    assert resultado["quantidade_tarefas"] == 4
    # Média real das concluídas (T10: 2h, T11: 4h) = 3.0h
    assert resultado["tempo_medio_conclusao"] == 3.0
    assert resultado["taxa_atraso_percentual"] == 0.0
    assert resultado["indicadores_por_prioridade"]["baixa"]["tarefas_concluidas"] == 1
    assert resultado["indicadores_por_prioridade"]["media"]["tarefas_concluidas"] == 0


def test_analisar_tarefas_id_vazio_lanca_erro(fixture_tarefa_id_vazio):
    """Garante que tarefas sem ID ou com ID vazio lançam ValueError."""
    with pytest.raises(ValueError, match="id_tarefa não pode ser vazio"):
        analisar_tarefas(fixture_tarefa_id_vazio)


def test_analisar_tarefas_id_duplicado_lanca_erro(fixture_tarefas_id_duplicado):
    """Garante que IDs repetidos na mesma coleção lançam ValueError."""
    with pytest.raises(ValueError, match="id_tarefa duplicado"):
        analisar_tarefas(fixture_tarefas_id_duplicado)


def test_analisar_tarefas_titulo_vazio_lanca_erro(fixture_tarefa_titulo_vazio):
    """Garante que tarefas com título vazio (ou só espaços) lançam ValueError."""
    with pytest.raises(ValueError, match="título vazio"):
        analisar_tarefas(fixture_tarefa_titulo_vazio)


def test_analisar_tarefas_status_invalido_lanca_erro(fixture_tarefa_status_invalido):
    """Garante que status fora do vocabulário lançam ValueError."""
    with pytest.raises(ValueError, match="Status inválido"):
        analisar_tarefas(fixture_tarefa_status_invalido)


def test_analisar_tarefas_concluida_sem_data_lanca_erro(
    fixture_tarefa_concluida_sem_data,
):
    """Garante que tarefas concluídas sem data de conclusão preenchida lançam erro."""
    with pytest.raises(ValueError, match="sem 'data_conclusao'"):
        analisar_tarefas(fixture_tarefa_concluida_sem_data)


def test_analisar_tarefas_formato_data_invalido_lanca_erro(
    fixture_tarefa_formato_data_invalido,
):
    """Garante que datas em formato não reconhecido lançam DataInvalidaError."""
    with pytest.raises(DataInvalidaError, match="Formato inválido"):
        analisar_tarefas(fixture_tarefa_formato_data_invalido)


def test_analisar_tarefas_data_sem_tz_lanca_erro(fixture_tarefa_data_sem_tz):
    """Garante que datas naive (sem indicativo de timezone) lançam DataInvalidaError."""
    with pytest.raises(DataInvalidaError, match="timezone-aware"):
        analisar_tarefas(fixture_tarefa_data_sem_tz)
def test_analisar_tarefas_prazo_anterior_criacao_lanca_erro(fixture_tarefa_prazo_anterior_criacao):
    """Garante que prazo anterior à data de criação lança DataInvalidaError."""
    with pytest.raises(DataInvalidaError, match="prazo é anterior à data_criacao"):
        analisar_tarefas(fixture_tarefa_prazo_anterior_criacao)

def test_analisar_tarefas_prazo_vazio_nao_quebra_execucao(fixture_tarefa_prazo_vazio):
    """Garante que ausência de prazo não quebra cálculos matemáticos."""
    resultado = analisar_tarefas(fixture_tarefa_prazo_vazio)
    assert resultado["taxa_atraso_percentual"] == 0.0
    assert resultado["quantidade_tarefas"] == 1