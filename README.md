# SnapNews
<img width="1413" height="786" alt="SnapNews1" src="https://github.com/user-attachments/assets/772bc8c2-b3cf-43c7-807b-ef3fd3920294" />

SnapNews is an AI-powered news summarizer built for Gen-Z and busy people who don't have time to read long articles. It fetches real breaking news, runs it through Google Gemini AI, and delivers bite-sized summaries in plain English — displayed in a clean, dark-themed flash-card interface.

 Features

📰 Live News — Fetches real headlines via NewsAPI
🤖 AI Summaries — Google Gemini summarizes every article in 3–4 simple sentences
🗂️ 6 Categories — Tech, Business, World, Science, Sports, Entertainment
🔍 Search — Search any topic and get AI-summarized results instantly
🃏 Flash Cards — Clean grid of news cards, easy to scan
📱 Responsive — Works on mobile, tablet, and desktop
⌨️ Keyboard shortcut — Press / to instantly focus the search bar


🛠️ Tech Stack<img width="863" height="756" alt="SnapNews2" src="https://github.com/user-attachments/assets/7a96bd26-a790-4664-a840-531812971a7e" />

LayerToolBackendPython + FlaskFrontendHTML + CSS + JavaScriptAIGoogle Gemini 1.5 Flash APINews DataNewsAPI.orgStylingCustom CSS (Yellow + Green)

📁 Project Structure
snapnews/
│
├── app.py              # Flask routes (homepage, category, search)
├── news_fetcher.py     # Fetches articles from NewsAPI
├── summarizer.py       # Sends articles to Gemini, returns summaries
├── prompts.py          # Gemini prompt templates
├── config.py           # API keys, category config, settings
├── requirements.txt    # Python dependencies
├── .env                # Your secret API keys (never commit this!)
│
├── templates/
│   ├── layout.html     # Shared navbar + footer (base template)
│   ├── index.html      # Homepage — all categories in a grid
│   ├── category.html   # Single category page
│   ├── search.html     # Search results page
│   └── 404.html        # Not found page
│
└── static/
    ├── style.css       # Yellow + green dark theme
    └── script.js       # Loading states, card animations
