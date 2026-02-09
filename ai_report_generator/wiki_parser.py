import wikipediaapi
from typing import List, Dict

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="AI-Report-Generator/1.0 (contact@example.com)"
)


def search_wikipedia(topics: List[str]) -> Dict[str, str]:
    """Ищет статьи по теме и смежным понятиям"""
    results = {}
    for topic in topics:
        page = wiki_wiki.page(topic)
        if page.exists():
            results[topic] = page.fullurl
    return results


def parse_article(url: str) -> str:
    """Извлекает чистый текст из статьи по URL"""
    title = url.split('/')[-1].replace('_', ' ')
    page = wiki_wiki.page(title)
    if page.exists():
        return page.text
    return ""


def extract_key_facts(text: str, max_facts: int = 20) -> List[str]:
    """Отбирает наиболее значимые факты (упрощённо — первые предложения абзацев)"""
    sentences = [s.strip() for s in text.split('. ') if len(s) > 30]
    return sentences[:max_facts]
