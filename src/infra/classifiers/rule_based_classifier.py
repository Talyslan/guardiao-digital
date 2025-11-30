from src.domain.interfaces.i_classifier import IClassifier
import re
from src.utils.text_cleaner import normalize_text

RULES = [
    # (pattern, weight, reason)
    (r"(envie sua|envie .* (foto|rg|documento|cpf|senha|codigo))", 0.95, "Pede que você envie documentos ou códigos (ex.: foto, RG, código SMS)."),
    (r"(problema|identificad).*\b(cpf|documento|conta)\b", 0.95, "Alega um problema com seu CPF ou documento, solicitando ação."),
    (r"(conta).*bloquead", 0.95, "Ameaça bloqueio de conta para pressionar ação imediata."),
    (r"\b(login|verify|verific|atualiz|atualiza|update|segur|secure)\b", 0.9, "Usa termos relacionados a login/atualização que sugerem páginas falsas."),
    (r"\b(pix|transferir|dep[oó]sito|urgente|ganhou|pr[eê]mio)\b", 0.9, "Solicita ações financeiras ou usa urgência para coagir o usuário."),
    (r"confirmar (dados|cpf|cart(o|ao)n|conta|senha)", 0.88, "Solicita confirmação de dados sensíveis (CPF, cartão, senha)."),
    (r"(clique|link)\s+(aqui|abaixo)", 0.8, "Instrui o usuário a clicar em um link possivelmente malicioso."),
    (r"\b[A-Z]{6,}\b", 0.2, "Uso excessivo de CAIXA ALTA — tom agressivo ou SPAM."),
]

class RuleBasedClassifier(IClassifier):
    def classify(self, text: str) -> float:
        message = normalize_text(text)
        scores = []

        for pattern, weight, _reason in RULES:
            if re.search(pattern, message, flags=re.IGNORECASE):
                scores.append(weight)

        return max(scores) if scores else 0.0

    def explain(self, text: str) -> list[str]:
        """Return a list of human-readable reasons (rules matched) for the given text."""
        message = normalize_text(text)
        reasons = []
        for pattern, _weight, reason in RULES:
            if re.search(pattern, message, flags=re.IGNORECASE):
                reasons.append(reason)
        return reasons
