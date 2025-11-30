from typing import Iterable
from src.domain.interfaces.i_classifier import IClassifier

class TextClassifierService:
    def __init__(self, classifiers: Iterable[IClassifier]):
        self.classifiers = list(classifiers)

    def score(self, text: str) -> float:
        scores = []
    
        for classifier in self.classifiers:
            try:
                score = classifier.classify(text)
                scores.append(float(score))
            except Exception:
                scores.append(0.0)

        return max(scores) if scores else 0.0
