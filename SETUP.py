"""
🚀 Quick Start Guide - Setup Your API Keys & Run First Test
================================================================

Follow these steps to get your stock trading bot up and running:

STEP 1: Get Your API Keys
========================

A) Alpaca Markets (Paper Trading)
   - Go to: https://alpaca.markets
   - Sign Up (free, no credit card needed)
   - Navigate to: Dashboard → Settings → API Keys
   - Copy: API Key and Secret Key
   - Paste into: config.py → ALPACA_API_KEY, ALPACA_SECRET_KEY

B) Google Gemini API (AI Sentiment)
   - Go to: https://aistudio.google.com
   - Click "Get API key" → "Create new secret key"
   - Copy the key
   - Paste into: config.py → GEMINI_API_KEY

C) NewsAPI (News Headlines)
   - Go to: https://newsapi.org
   - Sign Up (free tier available)
   - Copy your API Key
   - Paste into: config.py → NEWS_API_KEY


STEP 2: Configure config.py
===========================

Edit config.py and fill in your API keys:

    ALPACA_API_KEY = "pk_xxxxxxx..."
    ALPACA_SECRET_KEY = "xxxxxxx..."
    GEMINI_API_KEY = "AIzaXxx..."
    NEWS_API_KEY = "xxxxxxx..."

Then customize (optional):
    
    STOCK_SYMBOL = "AAPL"        # Change to any ticker
    CAPITAL = 100000              # Your paper trading capital


STEP 3: Test Each Module
=========================

Run these in order to verify everything works:

# Test 1: Data Fetching
python data.py
# Expected output: Stock data printed with last 5 rows

# Test 2: Technical Signals
python signals.py
# Expected output: Signal report with RSI, MACD, Buy/Sell signals

# Test 3: AI Sentiment
python sentiment.py
# Expected output: News headlines and AI sentiment analysis

# Test 4: Dashboard
python dashboard.py
# Expected output: Plotly chart opens in your browser

# Test 5: Paper Trading
python trader.py
# Expected output: Connection check and signal analysis (dry-run)


STEP 4: Continuous Monitoring (Optional)
========================================

To run automated monitoring, edit trader.py and uncomment:

    # bot.run_continuous_monitoring("AAPL", interval_minutes=60, execute=False)

Then run:
    python trader.py

This will check signals every 60 minutes and print recommendations.


STEP 5: Next Steps
==================

✅ Week 1: Run all tests, understand the signals
✅ Week 2-4: Monitor paper portfolio, refine settings
✅ Month 2+: Consider live trading (with caution!)

BEFORE You Trade Real Money:
  ✓ Run paper trading for 30+ days
  ✓ Backtest strategy on historical data
  ✓ Understand the risks (you can lose money)
  ✓ Start with small amounts
  ✓ Always use stop losses


TROUBLESHOOTING
===============

Problem: "ModuleNotFoundError: No module named 'yfinance'"
Solution: Make sure your virtual environment is activated
   Windows: .\venv\Scripts\activate
   
Problem: "Invalid API key"
Solution: Double-check your keys in config.py (no extra spaces)

Problem: "Connection refused to Alpaca"
Solution: Verify you're using paper trading API, not live


USEFUL RESOURCES
================

- Alpaca Docs: https://alpaca.markets/docs/
- Technical Analysis: https://www.investopedia.com
- Stock Screeners: https://finviz.com, https://www.tradingview.com


===================================
Questions? Check README.md for more details!
"""

if __name__ == "__main__":
    print(__doc__)
