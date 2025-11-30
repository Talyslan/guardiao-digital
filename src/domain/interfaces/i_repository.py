from abc import ABC, abstractmethod
from src.domain.entities.analysis_results import AnalysisResult

class IRepository(ABC):
    @abstractmethod
    def save_analysis(self, result: AnalysisResult) -> None:
        raise NotImplementedError
