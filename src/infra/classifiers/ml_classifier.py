from src.domain.interfaces.i_classifier import IClassifier
from transformers import pipeline
import os

class MLClassifier(IClassifier):
    def __init__(self):
        try:
            self.classifier = pipeline(
                "text-classification",
                model="mrm8488/bert-tiny-finetuned-fake-news",
                top_k=None
            )
        except Exception:
            self.classifier = None

    def classify(self, text: str) -> float:
        if not self.classifier:
            return 0.0

        try:
            result = self.classifier(text)[0]

            label = result.get("label", "").lower()
            score = float(result.get("score", 0.0))

            if "fake" in label:
                return score
            elif "real" in label:
                return 1 - score
            else:
                return 0.5

        except Exception:
            return 0.0
