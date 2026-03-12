"""
app.py
──────
Main Flask application for SnapNews.
Run this file to start the web server.

Usage:
    python app.py

Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from news_fetcher import fetch_by_category, fetch_all_categories, search_news
from summarizer import summarize_articles
from config import CATEGORIES, CATEGORY_META

app = Flask(__name__)


# ════════════════════════════════════════════════════════════════
#  HOME PAGE  –  /
#  Shows a few cards from each category
# ════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    """
    Homepage: fetches top 3 articles from every category,
    summarizes them, and passes them to index.html.
    """
    all_news = {}

    for category in CATEGORIES:
        articles = fetch_by_category(category)
        articles = articles[:3]  # only 3 per category on homepage
        summarize_articles(articles)
        all_news[category] = articles

    return render_template(
        "index.html",
        all_news=all_news,
        category_meta=CATEGORY_META,
        categories=list(CATEGORIES.keys()),
    )


# ════════════════════════════════════════════════════════════════
#  CATEGORY PAGE  –  /category/<name>
#  Shows all articles for one specific category
# ════════════════════════════════════════════════════════════════
@app.route("/category/<category_name>")
def category_page(category_name):
    """
    Category page: fetches and summarizes all articles for
    the chosen category (e.g., /category/sports).
    """
    # Validate the category
    if category_name not in CATEGORIES:
        return render_template("404.html"), 404

    articles = fetch_by_category(category_name)
    summarize_articles(articles)

    return render_template(
        "category.html",
        articles=articles,
        current_category=category_name,
        category_meta=CATEGORY_META,
        categories=list(CATEGORIES.keys()),
        meta=CATEGORY_META.get(category_name, {}),
    )


# ════════════════════════════════════════════════════════════════
#  SEARCH  – 
#  Called by the search bar
# ════════════════════════════════════════════════════════════════
@app.route("/search")
def search():
    """
    Search page: user submits a query via the search bar.
    Results are fetched from NewsAPI and summarized by Gemini.
    """
    query = request.args.get("q", "").strip()

    articles = []
    if query:
        articles = search_news(query)
        summarize_articles(articles, is_search=True)

    return render_template(
        "search.html",
        articles=articles,
        query=query,
        category_meta=CATEGORY_META,
        categories=list(CATEGORIES.keys()),
    )


# ════════════════════════════════════════════════════════════════
#  API ENDPOINT  –  /api/search?q=...
#  JSON endpoint for live search suggestions (optional upgrade)
# ════════════════════════════════════════════════════════════════
@app.route("/api/search")
def api_search():
    """
    Returns search results as JSON.
    Useful for building live search / autocomplete later.
    """
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"articles": [], "query": ""})

    articles = search_news(query)
    summarize_articles(articles, is_search=True)

    # Return only the fields the frontend needs
    result = [
        {
            "title":    a["title"],
            "summary":  a["summary"],
            "url":      a["url"],
            "category": a["category"],
            "source":   a["source"],
        }
        for a in articles
    ]

    return jsonify({"articles": result, "query": query})


# ════════════════════════════════════════════════════════════════
#  RUN THE APP
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🟡 SnapNews starting...")
    print("📰 Open http://localhost:5001 in your browser")
    app.run(debug=True, host="0.0.0.0", port=5001)
