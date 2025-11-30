from src.domain.interfaces.i_reputation_service import IReputationService
from src.domain.entities.url_reports import UrlReport
from src.core.config import settings
import requests
import time

class VirusTotalService(IReputationService):
    API_URL = "https://www.virustotal.com/api/v3"

    def check_url(self, url: str) -> UrlReport:
        key = settings.VIRUSTOTAL_KEY

        if not key:
            return UrlReport(url=url, safe=True, reasons=[])

        headers = {"x-apikey": key}

        # envia a url para análise
        creation_response = requests.post(
            f"{self.API_URL}/urls",
            data={"url": url},
            headers=headers,
            timeout=5
        )
        
        if creation_response.status_code not in (200, 201):
            return UrlReport(
                url=url,
                safe=True,
                reasons=[],
                provider_results={
                    "VirusTotalService": {"error": creation_response.text}
                }
            )
        
        analysis_id = creation_response.json().get("data", {}).get("id")

        if not analysis_id:
            return UrlReport(
                url=url,
                safe=True,
                reasons=[],
                provider_results={
                    "VirusTotalService": {"error": "No analysis ID returned"}
                }
            )

        # consulta a analise
        get_response = requests.get(
            f"{self.API_URL}/analyses/{analysis_id}",
            headers=headers,
            timeout=5
        )

        if get_response.status_code != 200:
            return UrlReport(
                url=url,
                safe=True,
                reasons=[],
                provider_results={
                    "VirusTotalService": {"error": get_response.text}
                }
            )
        
        analysis = get_response.json()

        stats = (
            analysis.get("data", {})
                    .get("attributes", {})
                    .get("stats", {})
        )

        malicious = stats.get("malicious", 0)

        safe = malicious == 0
        reasons = []

        if not safe:
            reasons.append(f"VirusTotal detected {malicious} malicious engines")

        return UrlReport(
            url=url,
            safe=safe,
            reasons=reasons,
            provider_results={
                "VirusTotalService": {
                    "malicious": malicious,
                    "stats": stats
                }
            }
        )
