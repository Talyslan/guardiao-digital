from src.domain.interfaces.i_reputation_service import IReputationService
from src.domain.entities.url_reports import UrlReport
from src.core.config import settings
import requests

class GoogleSafeBrowsingService(IReputationService):
    API_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    def check_url(self, url: str) -> UrlReport:
        key = settings.GOOGLE_SAFE_BROWSING_KEY
        
        if not key:
            return UrlReport(url=url, safe=True, reasons=[])

        payload = {
            "client": {"clientId": "guardian", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        params = {"key": key}
    
        response = requests.post(self.API_URL, json=payload, params=params, timeout=5)
    
        if response.status_code != 200:
            raise Exception("SafeBrowsing API error: %s" % response.text)
    
        data = response.json()
        matches = data.get("matches")
    
        if matches:
            reasons = [m.get("threatType") for m in matches]
            return UrlReport(url=url, safe=False, reasons=reasons, provider_results={"raw": data})
    
        return UrlReport(url=url, safe=True, reasons=[], provider_results={"raw": data})
