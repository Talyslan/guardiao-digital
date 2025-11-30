from src.domain.interfaces.i_classifier import IClassifier
import re
from src.utils.text_cleaner import normalize_text

RULES = [
    (r"\b(pix|transferir|depósito|urgente|ganhou|prêmio)\b", 0.9),
    (r"confirmar (dados|cpf|cart(o)ão|conta)", 0.8),
    (r"(clique|link) (aqui|abaixo)", 0.7),
    (r"\b[A-Z]{6,}\b", 0.2),
]

class RuleBasedClassifier(IClassifier):
    def classify(self, text: str) -> float:
        message = normalize_text(text)
        scores = []

        for pattern, weight in RULES:
            if re.search(pattern, message, flags=re.IGNORECASE):
                scores.append(weight)

        return max(scores) if scores else 0.0
