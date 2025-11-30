from bs4 import BeautifulSoup
import re

def sanitize_html(html: str) -> str:
    # remove scripts and unsafe tags
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "iframe"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    # strip multiple spaces
    return re.sub(r"\s+", " ", text).strip()
