from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import Container

router = APIRouter()
container = Container()

class AnalyzeRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    analyzer = container.analyzer_service
    payload = req.model_dump()
    analysis = analyzer.analyze_payload(payload)
    return analysis.to_dict()
