"""
Testes unitários para o módulo de limpeza de texto
"""
import pytest
from src.utils.text_cleaner import normalize_text


class TestTextCleaner:
    """Testes para normalização de texto"""

    def test_normalize_simple_text(self):
        """Testa normalização de texto simples"""
        result = normalize_text("Hello World")
        assert result == "hello world"

    def test_normalize_with_accents(self):
        """Testa remoção de acentos"""
        result = normalize_text("Olá, tudo bem? Você está aí?")
        assert result == "ola, tudo bem? voce esta ai?"

    def test_normalize_with_special_chars(self):
        """Testa normalização com caracteres especiais"""
        result = normalize_text("Têst€ çom ñ e ã")
        assert "test" in result.lower()

    def test_normalize_with_extra_spaces(self):
        """Testa remoção de espaços extras"""
        result = normalize_text("texto    com     muitos      espaços")
        assert "  " not in result
        assert result == "texto com muitos espacos"

    def test_normalize_empty_string(self):
        """Testa normalização de string vazia"""
        result = normalize_text("")
        assert result == ""

    def test_normalize_none(self):
        """Testa normalização de None"""
        result = normalize_text(None)
        assert result == ""

    def test_normalize_with_newlines(self):
        """Testa normalização com quebras de linha"""
        result = normalize_text("linha1\nlinha2\tlinha3")
        assert "\n" not in result
        assert "\t" not in result
        assert result == "linha1 linha2 linha3"

    def test_normalize_with_unicode(self):
        """Testa normalização com caracteres unicode"""
        result = normalize_text("Emoji: 😀 e símbolos: ™®©")
        assert isinstance(result, str)

    def test_normalize_preserves_basic_punctuation(self):
        """Testa que pontuação básica é preservada"""
        result = normalize_text("Olá, tudo bem? Sim!")
        assert "," in result
        assert "?" in result
        assert "!" in result

    def test_normalize_strips_whitespace(self):
        """Testa que espaços nas bordas são removidos"""
        result = normalize_text("  texto com espaços  ")
        assert not result.startswith(" ")
        assert not result.endswith(" ")
