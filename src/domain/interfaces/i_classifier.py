from abc import ABC, abstractmethod

class IClassifier(ABC):
    @abstractmethod
    def classify(self, text: str) -> float:
        raise NotImplementedError
