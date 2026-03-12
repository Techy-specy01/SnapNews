import os
from dotenv import load_dotenv


load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# --- News Categories ---
# Each category maps to a NewsAPI topic keyword
CATEGORIES = {
    "technology": "technology",
    "business":   "business",
    "world":      "general",
    "science":    "science",
    "sports":     "sports",
    "entertainment": "entertainment",
}


CATEGORY_META = {
    "technology":    {"label": "Tech",          "emoji": "💻", "color": "#4ade80"},
    "business":      {"label": "Business",      "emoji": "📈", "color": "#facc15"},
    "world":         {"label": "World",         "emoji": "🌍", "color": "#34d399"},
    "science":       {"label": "Science",       "emoji": "🔬", "color": "#a3e635"},
    "sports":        {"label": "Sports",        "emoji": "⚽", "color": "#fbbf24"},
    "entertainment": {"label": "Entertainment", "emoji": "🎬", "color": "#86efac"},
}

# How many articles to fetch per category
ARTICLES_PER_CATEGORY = 6

# NewsAPI base URL
NEWS_API_BASE = "https://newsapi.org/v2/top-headlines"
NEWS_API_SEARCH = "https://newsapi.org/v2/everything"

# Country for news (us = international English news)
NEWS_COUNTRY = "us"
