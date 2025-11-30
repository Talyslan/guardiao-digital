from src.domain.entities.message import Message
from src.domain.entities.analysis_results import AnalysisResult
from src.domain.entities.url_reports import UrlReport
from src.domain.interfaces.i_repository import IRepository
from src.services.url_reputation_service import UrlReputationService
from src.services.text_classifier_service import TextClassifierService
from src.core.logger import logger

class AnalyzerService:
    def __init__(self, url_reputation_service: UrlReputationService,
                 text_classifier_service: TextClassifierService,
                 repository: IRepository | None = None):
        self.url_reputation_service = url_reputation_service
        self.text_classifier_service = text_classifier_service
        self.repository = repository

    def analyze_payload(self, payload: dict) -> AnalysisResult:
        msg = Message(**payload)

        return self.analyze(msg)

    def analyze(self, message: Message) -> AnalysisResult:
        # 1) score textual
        text = message.text or ""
        score = self.text_classifier_service.score(text)

        reasons = []
        url_report = None

        # 2) If url present, check reputation
        if message.url:
            try:
                url_report = self.url_reputation_service.check(str(message.url))
                if not url_report.safe:
                    reasons.append("URL marcada como suspeita")
            except Exception as e:
                logger.error("Erro ao checar reputação: %s", e)

        # 3) Build status
        status = "safe"
        if score >= 0.7 or (url_report and not url_report.safe):
            status = "high_risk"
        elif score >= 0.4:
            status = "suspicious"

        result = AnalysisResult(
            status=status,
            score=score,
            reasons=reasons,
            url_report=url_report.model_dump() if url_report else None
        )

        # 4) persistir histórico (se existir repo)
        if self.repository:
            try:
                self.repository.save_analysis(result)
            except Exception as e:
                logger.warning("Falha ao salvar resultado: %s", e)

        return result
