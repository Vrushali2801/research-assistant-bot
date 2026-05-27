import os
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> list[dict]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "url": r["href"],
                "title": r["title"],
                "snippet": r["body"],
            })
    return results


def read_page(url: str, max_chars: int = 3000) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line for line in text.splitlines() if line.strip()]
    clean = "\n".join(lines)
    return clean[:max_chars]


def write_report(filename: str, content: str) -> str:
    os.makedirs("reports", exist_ok=True)
    if not filename.endswith(".md"):
        filename += ".md"
    filepath = os.path.join("reports", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath
