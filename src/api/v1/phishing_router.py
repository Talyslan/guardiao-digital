from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from src.core.container import Container

router = APIRouter()
container = Container()

class PhishingRequest(BaseModel):
    text: str | None = None
    url: HttpUrl | None = None
    email: str | None = None

class PhishingResponse(BaseModel):
    status: str
    score: float 
    reasons: list[str]
    url_report: dict | None = None

@router.post("/phishing/analyze", response_model=PhishingResponse)
async def analyze_phishing(payload: PhishingRequest):
    analyzer = container.analyzer_service
    try:
        result = analyzer.analyze_payload(payload.model_dump())
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
