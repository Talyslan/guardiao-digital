from pydantic import BaseModel
from typing import Optional

class AnalysisResult(BaseModel):
    status: str
    score: float
    reasons: list[str]
    url_report: Optional[dict] = None

    def to_dict(self):
        return self.model_dump()
