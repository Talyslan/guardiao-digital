"""
Testes unitários para o extrator de URLs
"""
import pytest
from src.utils.url_extractor import extract_urls


class TestUrlExtractor:
    """Testes para extração de URLs de texto"""

    def test_extract_single_http_url(self):
        """Testa extração de uma URL HTTP"""
        text = "Visite nosso site http://example.com para mais informações"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert "http://example.com" in urls[0]

    def test_extract_single_https_url(self):
        """Testa extração de uma URL HTTPS"""
        text = "Acesse https://secure-site.com agora"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert "https://secure-site.com" in urls[0]

    def test_extract_multiple_urls(self):
        """Testa extração de múltiplas URLs"""
        text = "Visite http://site1.com e também https://site2.com/path"
        urls = extract_urls(text)
        assert len(urls) == 2

    def test_extract_url_with_path(self):
        """Testa extração de URL com caminho"""
        text = "Clique em https://example.com/path/to/page"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert "/path/to/page" in urls[0]

    def test_extract_url_with_query_params(self):
        """Testa extração de URL com parâmetros"""
        text = "Link: https://example.com/search?q=test&page=1"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert "q=test" in urls[0]

    def test_extract_url_with_fragment(self):
        """Testa extração de URL com fragmento"""
        text = "Veja https://example.com/page#section"
        urls = extract_urls(text)
        assert len(urls) == 1

    def test_extract_no_urls(self):
        """Testa texto sem URLs"""
        text = "Este texto não contém nenhuma URL"
        urls = extract_urls(text)
        assert len(urls) == 0

    def test_extract_from_empty_string(self):
        """Testa extração de string vazia"""
        urls = extract_urls("")
        assert len(urls) == 0

    def test_extract_from_none(self):
        """Testa extração de None"""
        urls = extract_urls(None)
        assert len(urls) == 0

    def test_extract_url_with_port(self):
        """Testa extração de URL com porta"""
        text = "Servidor em http://localhost:8080/api"
        urls = extract_urls(text)
        assert len(urls) == 1
        assert ":8080" in urls[0]

    def test_extract_url_at_end_of_sentence(self):
        """Testa extração de URL no final da frase"""
        text = "Visite nosso site: https://example.com."
        urls = extract_urls(text)
        assert len(urls) == 1
        # O ponto final pode ou não ser incluído dependendo da regex

    def test_extract_url_case_insensitive(self):
        """Testa que extração é case-insensitive"""
        text = "Links: HTTP://EXAMPLE.COM e HtTpS://test.com"
        urls = extract_urls(text)
        assert len(urls) == 2
