"""
Testes unitários para as entidades de domínio
"""
import pytest
from pydantic import ValidationError
from src.domain.entities.message import Message
from src.domain.entities.analysis_results import AnalysisResult
from src.domain.entities.url_reports import UrlReport


class TestMessage:
    """Testes para a entidade Message"""

    def test_message_with_all_fields(self):
        """Testa criação de mensagem com todos os campos"""
        msg = Message(
            text="Texto de teste",
            url="http://example.com",
            email="test@example.com",
            metadata={"source": "whatsapp"}
        )
        assert msg.text == "Texto de teste"
        assert str(msg.url) == "http://example.com/"
        assert msg.email == "test@example.com"
        assert msg.metadata["source"] == "whatsapp"

    def test_message_with_optional_fields(self):
        """Testa criação de mensagem com campos opcionais"""
        msg = Message(text="Apenas texto")
        assert msg.text == "Apenas texto"
        assert msg.url is None
        assert msg.email is None
        assert msg.metadata == {}

    def test_message_empty(self):
        """Testa criação de mensagem vazia"""
        msg = Message()
        assert msg.text is None
        assert msg.url is None

    def test_message_invalid_url(self):
        """Testa validação de URL inválida"""
        with pytest.raises(ValidationError):
            Message(url="not-a-valid-url")

    def test_message_valid_url_formats(self):
        """Testa diferentes formatos válidos de URL"""
        urls = [
            "http://example.com",
            "https://example.com",
            "https://subdomain.example.com/path?query=1",
            "http://example.com:8080/path"
        ]
        for url in urls:
            msg = Message(url=url)
            assert msg.url is not None


class TestAnalysisResult:
    """Testes para a entidade AnalysisResult"""

    def test_analysis_result_safe(self):
        """Testa resultado de análise segura"""
        result = AnalysisResult(
            status="safe",
            score=0.1,
            reasons=[],
            url_report=None
        )
        assert result.status == "safe"
        assert result.score == 0.1
        assert result.reasons == []
        assert result.url_report is None

    def test_analysis_result_high_risk(self):
        """Testa resultado de análise de alto risco"""
        result = AnalysisResult(
            status="high_risk",
            score=0.95,
            reasons=["Padrão de phishing detectado", "URL suspeita"],
            url_report={"url": "http://bad.com", "safe": False}
        )
        assert result.status == "high_risk"
        assert result.score == 0.95
        assert len(result.reasons) == 2

    def test_analysis_result_to_dict(self):
        """Testa conversão para dicionário"""
        result = AnalysisResult(
            status="suspicious",
            score=0.5,
            reasons=["Termo suspeito encontrado"]
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["status"] == "suspicious"
        assert result_dict["score"] == 0.5


class TestUrlReport:
    """Testes para a entidade UrlReport"""

    def test_url_report_safe(self):
        """Testa relatório de URL segura"""
        report = UrlReport(
            url="http://example.com",
            safe=True,
            reasons=[],
            provider_results={}
        )
        assert report.safe is True
        assert len(report.reasons) == 0

    def test_url_report_malicious(self):
        """Testa relatório de URL maliciosa"""
        report = UrlReport(
            url="http://malicious.com",
            safe=False,
            reasons=["MALWARE", "PHISHING"],
            provider_results={"virustotal": {"malicious": 5}}
        )
        assert report.safe is False
        assert "MALWARE" in report.reasons
        assert "PHISHING" in report.reasons

    def test_url_report_with_provider_results(self):
        """Testa relatório com resultados de provedores"""
        report = UrlReport(
            url="http://test.com",
            safe=True,
            reasons=[],
            provider_results={
                "google_safe_browsing": {"status": "clean"},
                "virustotal": {"malicious": 0, "suspicious": 0}
            }
        )
        assert "google_safe_browsing" in report.provider_results
        assert "virustotal" in report.provider_results
