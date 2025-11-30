import re
import unicodedata

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()
