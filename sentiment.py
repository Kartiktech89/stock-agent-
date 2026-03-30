"""
Phase 4: AI Sentiment Analysis
Fetches news headlines using NewsAPI and analyzes sentiment with Gemini LLM.
"""

import requests
import google.generativeai as genai
from config import NEWS_API_KEY, GEMINI_API_KEY, NEWS_HEADLINES, SENTIMENT_MODE


def _select_gemini_model() -> str | None:
    """Select an available Gemini model that supports generateContent."""
    preferred = [
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro-latest",
        "models/gemini-1.5-pro",
        "models/gemini-pro",
    ]

    try:
        available = list(genai.list_models())
    except Exception:
        return None

    available_names = {
        model.name
        for model in available
        if hasattr(model, "supported_generation_methods")
        and "generateContent" in model.supported_generation_methods
    }

    for name in preferred:
        if name in available_names:
            return name.replace("models/", "")

    for name in available_names:
        if "gemini" in name:
            return name.replace("models/", "")

    return None


def fetch_news_headlines(symbol: str, num_headlines: int = NEWS_HEADLINES) -> list:
    """
    Fetch recent news headlines for a stock using NewsAPI.
    
    Args:
        symbol: Stock ticker (e.g., 'RELIANCE', 'AAPL')
        num_headlines: Number of news items to fetch
    
    Returns:
        List of headlines (strings)
    """
    if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_NEWS_API_KEY":
        print("⚠️  NewsAPI key not configured. Using mock data for demo.")
        return get_mock_headlines(symbol)
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    
    try:
        print(f"Fetching news for {symbol}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        articles = response.json().get("articles", [])[:num_headlines]
        headlines = [article["title"] for article in articles]
        
        print(f"✅ Fetched {len(headlines)} headlines")
        return headlines
    
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return get_mock_headlines(symbol)


def get_mock_headlines(symbol: str) -> list:
    """
    Get mock news headlines for testing (when API key not available).
    """
    mock_data = {
        "AAPL": [
            f"{symbol} stock hits new all-time high amid strong iPhone sales",
            f"{symbol} announces record quarterly earnings, beats analyst expectations",
            f"Tech sector surge drives {symbol} 5% higher this week",
            f"{symbol} launches new AI features in flagship products",
            f"{symbol} CEO optimistic about market growth in 2026"
        ],
        "RELIANCE": [
            f"{symbol} reports strong Q4 results, dividend boost expected",
            f"Indian energy stocks rally with {symbol} leading gains",
            f"{symbol} expands renewable energy portfolio",
            f"Analysts maintain 'buy' rating on {symbol}",
            f"{symbol} trading near 52-week high"
        ]
    }
    
    return mock_data.get(symbol, mock_data["AAPL"])


def analyze_sentiment_with_gemini(headlines: list, symbol: str) -> dict:
    """
    Analyze sentiment of news headlines using Google's Gemini API.
    
    Args:
        headlines: List of news headlines
        symbol: Stock symbol (for context)
    
    Returns:
        Dictionary with sentiment analysis results
    """
    if SENTIMENT_MODE == "local":
        print("Using local sentiment mode (no Gemini call)")
        return analyze_sentiment_locally(headlines, symbol)

    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("⚠️  Gemini API key not configured. Using local sentiment.")
        return analyze_sentiment_locally(headlines, symbol)
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model_name = _select_gemini_model()
        if not model_name:
            raise RuntimeError("No Gemini generateContent model available for this key/API version")

        model = genai.GenerativeModel(model_name)
        
        headlines_text = "\n".join([f"- {h}" for h in headlines])
        
        prompt = f"""Given these news headlines about {symbol}, analyze the overall sentiment:

{headlines_text}

Is the sentiment Bullish, Bearish, or Neutral? 
Respond with ONLY one word: BULLISH, BEARISH, or NEUTRAL.
Then on a new line, give a confidence score from 0 to 100."""
        
        print(f"Analyzing sentiment with Gemini ({model_name})...")
        response = model.generate_content(prompt)
        sentiment_text = response.text.strip().split('\n')[0].strip().upper()
        if sentiment_text not in {"BULLISH", "BEARISH", "NEUTRAL"}:
            if "BULLISH" in sentiment_text:
                sentiment_text = "BULLISH"
            elif "BEARISH" in sentiment_text:
                sentiment_text = "BEARISH"
            else:
                sentiment_text = "NEUTRAL"
        
        # Parse confidence if provided
        try:
            confidence = int(response.text.strip().split('\n')[1])
        except:
            confidence = 60
        
        return {
            "sentiment": sentiment_text,
            "confidence": confidence,
            "headlines_count": len(headlines),
            "method": "gemini"
        }
    
    except Exception as e:
        print(f"❌ Error analyzing sentiment: {e}")
        if SENTIMENT_MODE in {"auto", "gemini"}:
            print("Falling back to local sentiment mode")
            return analyze_sentiment_locally(headlines, symbol)
        return get_mock_sentiment(symbol)


def get_mock_sentiment(symbol: str) -> dict:
    """
    Get mock sentiment data for testing.
    """
    sentiments = {
        "AAPL": {"sentiment": "BULLISH", "confidence": 75},
        "RELIANCE": {"sentiment": "BULLISH", "confidence": 70}
    }
    result = sentiments.get(symbol, {"sentiment": "NEUTRAL", "confidence": 50})
    result["headlines_count"] = 5
    return result


def analyze_sentiment_locally(headlines: list, symbol: str) -> dict:
    """Analyze sentiment using a local keyword-scoring method (no LLM/API calls)."""
    bullish_words = {
        "beat", "beats", "upgrade", "upgrades", "strong", "record", "growth",
        "profit", "profits", "bullish", "surge", "rally", "gain", "gains",
        "expands", "optimistic", "high", "outperform", "buy",
    }
    bearish_words = {
        "miss", "misses", "downgrade", "downgrades", "weak", "loss", "losses",
        "bearish", "drop", "falls", "fall", "decline", "declines", "lawsuit",
        "investigation", "risk", "cuts", "sell", "warning", "slump",
    }

    score = 0
    for headline in headlines:
        text = headline.lower()
        score += sum(1 for word in bullish_words if word in text)
        score -= sum(1 for word in bearish_words if word in text)

    if score > 1:
        sentiment = "BULLISH"
    elif score < -1:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"

    confidence = min(90, max(55, 55 + abs(score) * 8))
    return {
        "sentiment": sentiment,
        "confidence": int(confidence),
        "headlines_count": len(headlines),
        "method": "local-keyword",
        "symbol": symbol,
    }


def combine_signals(technical_signal: str, ai_sentiment: str) -> str:
    """
    Combine technical signal with AI sentiment for final recommendation.
    
    Args:
        technical_signal: BUY, SELL, or NEUTRAL from technical analysis
        ai_sentiment: BULLISH, BEARISH, or NEUTRAL from AI analysis
    
    Returns:
        Combined signal strength
    """
    if technical_signal == "BUY":
        if ai_sentiment == "BULLISH":
            return "STRONG BUY 🚀"
        elif ai_sentiment == "BEARISH":
            return "WEAK BUY ⚠️"
        else:
            return "BUY 📈"
    
    elif technical_signal == "SELL":
        if ai_sentiment == "BEARISH":
            return "STRONG SELL 📉"
        elif ai_sentiment == "BULLISH":
            return "WEAK SELL ⚠️"
        else:
            return "SELL 📉"
    
    else:  # NEUTRAL
        if ai_sentiment == "BULLISH":
            return "HOLD - Positive Sentiment 👍"
        elif ai_sentiment == "BEARISH":
            return "HOLD - Negative Sentiment 👎"
        else:
            return "HOLD - No Clear Signal"


def print_sentiment_report(symbol: str, headlines: list, sentiment: dict, combined: str):
    """
    Pretty-print sentiment analysis report.
    """
    print("\n" + "="*60)
    print(f"🤖 SENTIMENT ANALYSIS - {symbol}")
    print("="*60)
    print(f"Headlines fetched: {sentiment['headlines_count']}")
    print(f"\nTop headlines:")
    for i, h in enumerate(headlines[:3], 1):
        print(f"  {i}. {h}")
    
    print(f"\nAI Analysis:")
    print(f"  Sentiment: {sentiment['sentiment']} (Confidence: {sentiment['confidence']}%)")
    print(f"\nCombined Signal: {combined}")
    print("="*60 + "\n")


if __name__ == "__main__":
    from config import STOCK_SYMBOL
    
    # Test: Fetch news and analyze sentiment
    symbol = STOCK_SYMBOL
    headlines = fetch_news_headlines(symbol)
    sentiment = analyze_sentiment_with_gemini(headlines, symbol)
    combined = combine_signals("BUY", sentiment["sentiment"])
    
    print_sentiment_report(symbol, headlines, sentiment, combined)
