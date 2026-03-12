"""
news_fetcher.py
───────────────
Fetches news articles from NewsAPI.org.
NewsAPI gives us headlines + descriptions for free.

Free tier limit: 100 requests/day
Sign up at: https://newsapi.org/register
"""

import requests
from config import (
    NEWS_API_KEY,
    NEWS_API_BASE,
    NEWS_API_SEARCH,
    CATEGORIES,
    ARTICLES_PER_CATEGORY,
    NEWS_COUNTRY,
)


# ── Helper: clean up article data ──────────────────────────────────────────
def _clean_article(article: dict, category: str) -> dict | None:
    """
    Takes a raw NewsAPI article dict and returns a clean version.
    Returns None if the article is missing key fields.
    """
    title = (article.get("title") or "").strip()    
    description = (article.get("description") or "").strip()
    url = (article.get("url") or "").strip()
    source = (article.get("source") or {}).get("name", "Unknown")
    image = article.get("urlToImage") or ""


    # Skip articles with missing data or placeholder titles
    if not title or not description or not url:
        return None
    if "[Removed]" in title or "[Removed]" in description:
        return None

    return {
        "title":       title,
        "description": description,   # raw text — will be summarized later
        "url":         url,
        "source":      source,
        "image":       image or "",
        "category":    category,
        "summary":     None,          # filled in by summarizer
    }


# ── Fetch by category ───────────────────────────────────────────────────────
def fetch_by_category(category: str) -> list[dict]:
    """
    Fetches top headlines for a given category.
    category must be one of the keys in config.CATEGORIES.
    Returns a list of cleaned article dicts.
    """
    if category not in CATEGORIES:
        return []

    api_category = CATEGORIES[category]  # e.g. "technology"

    params = {
        "apiKey":   NEWS_API_KEY,
        "category": api_category,
        "country":  NEWS_COUNTRY,
        "pageSize": ARTICLES_PER_CATEGORY,
    }

    try:
        response = requests.get(NEWS_API_BASE, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for raw in data.get("articles", []):
            cleaned = _clean_article(raw, category)
            if cleaned:
                articles.append(cleaned)

        return articles

    except requests.RequestException as e:
        print(f"[NewsAPI Error] Category={category}: {e}")
        return []


# ── Fetch all categories ────────────────────────────────────────────────────
def fetch_all_categories() -> dict[str, list[dict]]:
    """
    Fetches news for ALL categories.
    Returns a dict: { "technology": [...], "sports": [...], ... }
    """
    all_news = {}
    for category in CATEGORIES:
        all_news[category] = fetch_by_category(category)
    return all_news


# ── Search news ─────────────────────────────────────────────────────────────
def search_news(query: str) -> list[dict]:
    """
    Searches NewsAPI for articles matching the query string.
    Returns a list of cleaned article dicts.
    """
    if not query or not query.strip():
        return []

    params = {
        "apiKey":   NEWS_API_KEY,
        "q":        query.strip(),
        "pageSize": 12,
        "sortBy":   "relevancy",
        "language": "en",
    }

    try:
        response = requests.get(NEWS_API_SEARCH, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = []
        for raw in data.get("articles", []):
            cleaned = _clean_article(raw, "search")
            if cleaned:
                articles.append(cleaned)

        return articles

    except requests.RequestException as e:
        print(f"[NewsAPI Error] Search={query}: {e}")
        return []


# ── Demo: run directly to test ──────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing news fetcher...")
    articles = fetch_by_category("technology")
    for a in articles:
        print(f"  • {a['title'][:60]}...")
