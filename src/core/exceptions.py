class ExternalServiceError(Exception):
    """Erro ao consumir serviço externo."""
    pass

class AnalysisError(Exception):
    """Erro na análise do payload."""
    pass
