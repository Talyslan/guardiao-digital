# Injeção de dependências simples (manual). Troque por dependency-injector se quiser.
from src.services.analyzer_service import AnalyzerService
from src.services.url_reputation_service import UrlReputationService
from src.services.text_classifier_service import TextClassifierService
from src.infra.reputation.google_safebrowsing import GoogleSafeBrowsingService
from src.infra.reputation.virustotal import VirusTotalService
from src.infra.classifiers.rule_based_classifier import RuleBasedClassifier
from src.infra.classifiers.ml_classifier import MLClassifier
from src.infra.database.memory_repository import MemoryRepository
from src.core.config import settings

class Container:
    def __init__(self):
        # infra
        self.google_safe = GoogleSafeBrowsingService()
        self.virustotal = VirusTotalService()
        self.rule_classifier = RuleBasedClassifier()
        self.ml_classifier = MLClassifier()
        self.memory_repo = MemoryRepository()

        # services
        self.url_reputation_service = UrlReputationService([self.google_safe, self.virustotal])
        self.text_classifier_service = TextClassifierService([self.rule_classifier, self.ml_classifier])
        self.analyzer_service = AnalyzerService(
            url_reputation_service=self.url_reputation_service,
            text_classifier_service=self.text_classifier_service,
            repository=self.memory_repo
        )

    def wire(self):
        # hook for startup logic if needed
        pass
