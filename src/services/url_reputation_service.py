from typing import Iterable
from src.domain.interfaces.i_reputation_service import IReputationService
from src.domain.entities.url_reports import UrlReport

class UrlReputationService:
    def __init__(self, providers: Iterable[IReputationService]):
        self.providers = list(providers)

    def check(self, url: str) -> UrlReport:
        reasons = []
        provider_results = {}
        safe = True

        for provider in self.providers:
            try:
                response: UrlReport = provider.check_url(url)
                provider_results[provider.__class__.__name__] = response.model_dump()

                if not response.safe:
                    safe = False
                    reasons.extend(response.reasons)

            except Exception as e:
                provider_results[provider.__class__.__name__] = {"error": str(e)}

        return UrlReport(url=url, safe=safe, reasons=list(set(reasons)), provider_results=provider_results)
