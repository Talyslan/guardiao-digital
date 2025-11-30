"""Testes para o `AnalyzerService` usando o `container` de teste.

Verifica que o serviço persiste o resultado chamando o repositório mockado.
"""

def test_analyzer_service_persists_result(container, phishing_message):
    """AnalyzerService.analyze deve salvar o resultado via repository quando houver repository.

    - ajusta o score para um valor alto
    - chama `analyze` e verifica que `repository.save_analysis` foi chamado
    """
    # forçar score alto (high_risk)
    container.text_classifier_service.score.return_value = 0.9

    result = container.analyzer_service.analyze(phishing_message)

    assert result.status == "high_risk"
    # o AnalyzerService usa analyzer_service.repository para salvar
    saved_repo = container.analyzer_service.repository
    saved_repo.save_analysis.assert_called_once()
