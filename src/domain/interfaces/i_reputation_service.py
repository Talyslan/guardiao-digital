from abc import ABC, abstractmethod
from src.domain.entities.url_reports import UrlReport

class IReputationService(ABC):
    @abstractmethod
    def check_url(self, url: str) -> UrlReport:
        raise NotImplementedError
