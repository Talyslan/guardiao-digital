from pydantic import BaseModel, HttpUrl
from typing import Optional

class UrlReport(BaseModel):
    url: HttpUrl
    safe: bool
    reasons: list[str] = []
    provider_results: dict | None = None
