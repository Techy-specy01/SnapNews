

import google.generativeai as genai
from config import GEMINI_API_KEY
from prompts import SUMMARIZE_PROMPT, SEARCH_SUMMARY_PROMPT


# ── Configure Gemini once when this module loads ────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini Flash — it's fast and free-tier friendly
_model = genai.GenerativeModel("gemini-1.5-flash")


# ── Summarize a single article ──────────────────────────────────────────────
def summarize_article(title: str, text: str, is_search: bool = False) -> str:
    """
    Sends article title + text to Gemini and returns a short summary.

    Args:
        title     : Article headline
        text      : Article body or description
        is_search : Use a slightly different prompt for search results

    Returns:
        A 3-4 sentence plain-English summary string.
    """

    # Pick the right prompt template
    template = SEARCH_SUMMARY_PROMPT if is_search else SUMMARIZE_PROMPT

    # Fill in the prompt with actual content
    prompt = template.format(
        title=title,
        article_text=text[:1500],  # limit input to avoid token overuse
    )

    try:
        response = _model.generate_content(prompt)
        summary = response.text.strip()

        # Safety: if Gemini returns nothing useful, fall back to description
        if not summary or len(summary) < 20:
            return text[:200] + "..."

        return summary

    except Exception as e:
        print(f"[Gemini Error] {e}")
        # Graceful fallback — show original description
        return text[:200] + "..." if text else "Summary not available."


# ── Summarize a list of articles in place ──────────────────────────────────
def summarize_articles(articles: list[dict], is_search: bool = False) -> list[dict]:
    """
    Takes a list of article dicts and adds a 'summary' field to each.
    Modifies articles in place AND returns the list.
    """
    for article in articles:
        raw_text = article.get("description", "") or article.get("title", "")
        article["summary"] = summarize_article(
            title=article.get("title", ""),
            text=raw_text,
            is_search=is_search,
        )
    return articles


# ── Demo ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_title = "Scientists discover water on Mars"
    test_text  = """
    NASA scientists have confirmed the presence of liquid water beneath
    the south polar ice cap of Mars, using radar data from the Mars
    Express spacecraft. This discovery raises new questions about the
    possibility of microbial life on the red planet.
    """
    print("Testing summarizer...")
    result = summarize_article(test_title, test_text)
    print("Summary:", result)
