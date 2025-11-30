"""Testes de integração para as rotas de phishing.

Usam fixtures definidas em `tests/conftest.py`: `client`, `container`, `phishing_message`,
`mock_malicious_url_report`.
"""

def test_phishing_analyze_route(client, container, phishing_message, mock_malicious_url_report):
    """POST /api/v1/phishing/analyze deve retornar um AnalysisResult serializável.

    - configura o container para retornar um relatório malicioso
    - força um score alto para garantir `high_risk`
    - faz a requisição e valida o JSON de resposta
    """
    # preparar container para cenário malicioso
    container.url_reputation_service.check.return_value = mock_malicious_url_report
    container.text_classifier_service.score.return_value = 0.85

    payload = {
        "text": phishing_message.text,
        "url": str(phishing_message.url),
        "email": phishing_message.email,
    }

    response = client.post("/api/v1/phishing/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert data.get("status") == "high_risk"
    assert "score" in data
    assert "reasons" in data
    # o resultado deve conter relatório de URL (porque configuramos check como malicioso)
    assert data.get("url_report") is not None
