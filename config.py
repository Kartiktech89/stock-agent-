"""
Configuration file for API keys and settings.
Store all sensitive credentials here.
Never commit this file to public repositories.
"""

# Local paper trading config
PORTFOLIO_FILE = "portfolio.json"

# Gemini API (Google AI)
GEMINI_API_KEY = "AIzaSyB1xxxx

# NewsAPI
NEWS_API_KEY = "73f7cf7d17exxxx

# Sentiment Mode: auto | gemini | local
SENTIMENT_MODE = "local"

# Trading Configuration
CAPITAL = 100000  # Starting capital in dollars (paper trading)
RISK_PER_TRADE = 0.02  # 2% risk per trade
STOCK_SYMBOL = "AAPL"  # Default stock to track (can be changed)

# Dashboard Config
DASHBOARD_PORT = 8050
DASHBOARD_DEBUG = True

# Data Fetching Config
DAYS_BACK = 100  # Historical data to fetch
NEWS_HEADLINES = 5  # Number of news items to fetch for sentiment
USE_SAMPLE_DATA_ON_FAILURE = True  # If Yahoo fetch fails, generate local sample OHLCV data

# Logging
LOG_LEVEL = "INFO"
