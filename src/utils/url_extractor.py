import re
from typing import List

URL_RE = re.compile(r"https?://[^\s]+", re.IGNORECASE)

def extract_urls(text: str) -> List[str]:
    return URL_RE.findall(text or "")
