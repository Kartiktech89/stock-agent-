"""
System Health Check - Verify all dependencies and API keys
"""

import sys
from pathlib import Path

print("\n" + "="*70)
print("🔍 STOCK TRADING BOT - SYSTEM HEALTH CHECK")
print("="*70 + "\n")

# Check Python version
print(f"✓ Python Version: {sys.version.split()[0]}")

# Check virtual environment
try:
    venv_path = Path(sys.executable).parent.parent
    if 'venv' in str(venv_path) or 'virtualenv' in str(venv_path):
        print(f"✓ Virtual Environment: ACTIVE ({sys.executable})")
    else:
        print(f"⚠️  Virtual Environment: May not be activated properly")
except:
    pass

# Check dependencies
print("\n📦 Checking Dependencies:")
print("-" * 70)

dependencies = {
    "yfinance": "Stock data fetching",
    "pandas": "Data manipulation",
    "plotly": "Dashboard visualization",
    "requests": "API calls",
    "rich": "Pretty console output",
    "google.generativeai": "AI sentiment analysis",
    "ta": "Technical indicators",
}

missing = []
for module, description in dependencies.items():
    try:
        __import__(module)
        print(f"  ✓ {module:<25} - {description}")
    except ImportError:
        print(f"  ✗ {module:<25} - {description}")
        missing.append(module)

if missing:
    print(f"\n❌ Missing packages: {', '.join(missing)}")
    print(f"Install with: pip install {' '.join(missing)}\n")
else:
    print(f"\n✅ All dependencies installed!\n")

# Check config file
print("📝 Checking Configuration:")
print("-" * 70)

try:
    from config import (
        GEMINI_API_KEY, 
        NEWS_API_KEY,
        STOCK_SYMBOL,
        CAPITAL
    )
    
    keys_configured = {
        "Gemini API Key": GEMINI_API_KEY != "YOUR_GEMINI_API_KEY",
        "NewsAPI Key": NEWS_API_KEY != "YOUR_NEWS_API_KEY",
    }
    
    for key_name, is_configured in keys_configured.items():
        status = "✓ CONFIGURED" if is_configured else "⚠️  NOT SET"
        print(f"  {key_name:<25} - {status}")
    
    print(f"\n  Default Stock: {STOCK_SYMBOL}")
    print(f"  Paper Trading Capital: ${CAPITAL:,}")
    
except Exception as e:
    print(f"  ✗ Error reading config: {e}")

# Quick API connectivity test
print("\n🌐 Testing API Connectivity:")
print("-" * 70)

# Test yfinance
try:
    import yfinance as yf
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    print(f"  ✓ Yahoo Finance - Connected")
except Exception as e:
    print(f"  ✗ Yahoo Finance - Error: {str(e)[:50]}")

# Test local paper portfolio storage
try:
    from pathlib import Path as _Path

    portfolio_path = _Path("portfolio.json")
    if portfolio_path.exists():
        print("  ✓ Local Portfolio - portfolio.json available")
    else:
        print("  ⚠️  Local Portfolio - portfolio.json not created yet (run trader.py once)")
except Exception as e:
    print(f"  ⚠️  Local Portfolio - Error: {str(e)[:50]}")

# Test Gemini API
try:
    from config import GEMINI_API_KEY
    import google.generativeai as genai
    
    if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
        genai.configure(api_key=GEMINI_API_KEY)
        print(f"  ✓ Gemini API - Configured")
    else:
        print(f"  ⚠️  Gemini API - API key not configured")
except Exception as e:
    print(f"  ⚠️  Gemini API - Error: {str(e)[:50]}")

# Test NewsAPI
try:
    from config import NEWS_API_KEY
    import requests
    
    if NEWS_API_KEY != "YOUR_NEWS_API_KEY":
        headers = {"X-Api-Key": NEWS_API_KEY}
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=us&pageSize=1",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print(f"  ✓ NewsAPI - Connected")
        else:
            print(f"  ⚠️  NewsAPI - Invalid key or rate limit")
    else:
        print(f"  ⚠️  NewsAPI - API key not configured")
except Exception as e:
    print(f"  ⚠️  NewsAPI - Error: {str(e)[:50]}")

print("\n" + "="*70)
print("✅ Health check complete! Ready to trade 📈")
print("="*70 + "\n")

print("Next steps:")
print("  1. Edit config.py with your API keys")
print("  2. Run: python data.py")
print("  3. Run: python signals.py")
print("  4. Run: python dashboard.py")
print("  5. Run: python trader.py")
print("\nSee README.md for complete guide.\n")
