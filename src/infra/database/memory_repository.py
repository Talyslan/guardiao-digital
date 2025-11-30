from src.domain.interfaces.i_repository import IRepository
from src.domain.entities.analysis_results import AnalysisResult
from typing import List

class MemoryRepository(IRepository):
    def __init__(self):
        self._store: List[dict] = []

    def save_analysis(self, result: AnalysisResult) -> None:
        self._store.append(result.model_dump())

    def all(self):
        return list(self._store)
