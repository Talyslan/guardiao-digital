import sys
from pathlib import Path
import importlib

import pytest
from unittest.mock import Mock

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from src.core.container import Container
import src.main as main_app
from src.domain.entities.message import Message
from src.domain.entities.url_reports import UrlReport
from src.domain.entities.analysis_results import AnalysisResult


@pytest.fixture
def container(monkeypatch, mock_repository, mock_safe_url_report):
    test_container = Container()

    test_container.memory_repo = mock_repository
    test_container.analyzer_service.repository = mock_repository

    test_container.text_classifier_service.score = Mock(return_value=0.1)

    test_container.url_reputation_service.check = Mock(return_value=mock_safe_url_report)

    analysis_module = importlib.import_module('src.api.v1.analysis_router')
    phishing_module = importlib.import_module('src.api.v1.phishing_router')
    monkeypatch.setattr(analysis_module, 'container', test_container, raising=False)
    monkeypatch.setattr(phishing_module, 'container', test_container, raising=False)

    monkeypatch.setattr(main_app, 'container', test_container, raising=False)

    return test_container


@pytest.fixture
def client(container):
    try:
        from fastapi.testclient import TestClient
    except Exception as exc:  # httpx missing triggers RuntimeError from starlette
        pytest.skip(f"TestClient unavailable: {exc}")

    return TestClient(main_app.app)


@pytest.fixture
def mock_safe_url_report():
    return UrlReport(
        url="http://example.com",
        safe=True,
        reasons=[],
        provider_results={"test": "safe"}
    )


@pytest.fixture
def mock_malicious_url_report():
    return UrlReport(
        url="http://malicious-site.com",
        safe=False,
        reasons=["SOCIAL_ENGINEERING", "MALWARE"],
        provider_results={"test": "malicious"}
    )


@pytest.fixture
def safe_message():
    return Message(
        text="Reunião amanhã às 10h na sala 5",
        url="http://example.com",
        email="usuario@example.com"
    )


@pytest.fixture
def phishing_message():
    return Message(
        text="URGENTE! Você ganhou um prêmio de R$ 10.000! Clique aqui para confirmar seus dados de cartão",
        url="http://phishing-site.com/premio",
        email="golpista@fake.com"
    )


@pytest.fixture
def mock_repository():
    mock_repo = Mock()
    mock_repo.save_analysis = Mock()
    mock_repo.all = Mock(return_value=[])
    return mock_repo
