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

    def explain(self, text: str) -> list[str]:
        """Aggregate explanations from classifiers that implement `explain`.

        Returns a list of reason strings (may be empty).
        """
        reasons = []
        for classifier in self.classifiers:
            expl = None
            try:
                expl = getattr(classifier, 'explain', None)
                if callable(expl):
                    r = expl(text)
                    if r:
                        # extend with unique reasons
                        for reason in r:
                            if reason not in reasons:
                                reasons.append(reason)
            except Exception:
                # ignore explain errors to keep scoring robust
                continue
        return reasons
