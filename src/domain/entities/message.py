from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class Message(BaseModel):
    text: Optional[str] = None
    url: Optional[HttpUrl] = None
    email: Optional[str] = None
    metadata: dict = {}
