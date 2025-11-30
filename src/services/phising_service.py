from src.services.analyzer_service import AnalyzerService

class PhishingService:
    def __init__(self, analyzer: AnalyzerService):
        self.analyzer = analyzer

    def analyze_email(self, email_text: str):
        return self.analyzer.analyze_payload({"text": email_text})
