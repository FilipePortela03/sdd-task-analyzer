"""Módulo contendo as exceções customizadas do TaskAnalyzer."""


class DataInvalidaError(Exception):
    """Exceção lançada quando há inconsistência temporal ou formato de data incorreto.

    A mensagem de erro deve conter o ID da tarefa e o campo que causou a falha.
    """

    pass
