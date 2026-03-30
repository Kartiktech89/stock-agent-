# AI Stock Analysis & Signal Dashboard 📈🤖

A complete automated stock analysis system that combines technical indicators, AI sentiment analysis, and paper trading automation.

## 📋 Project Overview

This project implements a professional-grade stock trading signal system across 6 phases:

1. **Setup & Dependencies** - Install Python libraries and get API keys
2. **Data Fetching** - Historical stock data using yfinance
3. **Technical Analysis** - RSI, MACD, Moving Averages with automated signals
4. **AI Sentiment** - News sentiment analysis using Google Gemini LLM
5. **Interactive Dashboard** - Plotly visualization with buy/sell markers
6. **Paper Trading** - Alpaca API integration for risk-free automated trading

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows/Mac/Linux
- ~30 minutes for full setup

### Step 1: Setup Your Python Environment

```powershell
# Navigate to project directory
cd stock-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install yfinance pandas talib plotly requests google-generativeai alpaca-trade-api rich
```

### Step 2: Get Free API Keys

1. **Alpaca Markets** (Paper Trading)
   - https://alpaca.markets
   - Sign up → Get API key for paper trading account
   - No credit card needed

2. **Google Gemini API** (AI Sentiment)
   - https://aistudio.google.com
   - Generate API key (free tier available)

3. **NewsAPI** (News Headlines)
   - https://newsapi.org
   - Sign up for API key (free tier: 100 requests/day)

### Step 3: Configure API Keys

Edit `config.py` and fill in your API keys:

```python
ALPACA_API_KEY = "YOUR_ALPACA_API_KEY"
ALPACA_SECRET_KEY = "YOUR_ALPACA_SECRET_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
```

## 📊 Phase Breakdown

### Phase 1: Install & Setup (2 hours)
✅ Already done! Libraries installed, folder structure created, API keys configured.

### Phase 2: Fetch Stock Data (2 hours)
**File:** `data.py`

Fetches historical OHLCV data from Yahoo Finance.

```python
from data import fetch_stock_data

# Fetch RELIANCE (Indian stock) or any ticker
data = fetch_stock_data("RELIANCE.NS", days_back=30)
print(data.head())  # Show first 5 rows
```

**Output:** DataFrame with Open, High, Low, Close, Volume, Adj Close

### Phase 3: Technical Indicators & Signals (3 hours)
**File:** `signals.py`

Implements RSI, MACD, Moving Averages with automated signal generation.

**Signal Rules:**
- **BUY**: RSI < 30 AND MACD > Signal line
- **SELL**: RSI > 70 AND MACD < Signal line
- **Neutral**: No clear signal

**Position Sizing** (Risk Management):
```
Risk per trade = 2% of capital
Quantity = (Capital × 0.02) / Stock Price
```

```python
from signals import calculate_indicators, generate_signals, print_signal_report
from data import fetch_stock_data

data = fetch_stock_data("AAPL", days_back=100)
data = calculate_indicators(data)
signal = generate_signals(data, "AAPL")
print_signal_report(signal)
```

### Phase 4: AI Sentiment Analysis (2 hours)
**File:** `sentiment.py`

Fetches news headlines and analyzes sentiment using Google Gemini LLM.

```python
from sentiment import fetch_news_headlines, analyze_sentiment_with_gemini, combine_signals

headlines = fetch_news_headlines("AAPL")
sentiment = analyze_sentiment_with_gemini(headlines, "AAPL")
print(sentiment)  # {'sentiment': 'BULLISH', 'confidence': 75}

# Combine technical + AI signal
combined = combine_signals("BUY", sentiment['sentiment'])
print(combined)  # "STRONG BUY 🚀"
```

### Phase 5: Interactive Dashboard (3 hours)
**File:** `dashboard.py`

Creates professional Plotly charts with:
- Candlestick price chart
- Moving Averages (50-day, 200-day)
- RSI indicator with overbought/oversold zones
- Buy/Sell signal markers
- Interactive tooltips

```python
from dashboard import create_trading_dashboard, save_dashboard
from data import fetch_stock_data
from signals import calculate_indicators, generate_signals

data = fetch_stock_data("AAPL", days_back=100)
data = calculate_indicators(data)
signal = generate_signals(data, "AAPL")

fig = create_trading_dashboard("AAPL", data, signal)
fig.show()  # Opens in browser
save_dashboard(fig, "AAPL")  # Saves as HTML
```

### Phase 6: Paper Trading Automation (3 hours)
**File:** `trader.py`

Automates trading using Alpaca's paper trading API (zero financial risk).

```python
from trader import PaperTradingBot

bot = PaperTradingBot()

# Check signal without trading (dry-run)
result = bot.check_signal_and_trade("AAPL", execute=False)

# Execute trade automatically
result = bot.check_signal_and_trade("AAPL", execute=True)

# Continuous monitoring (checks every 60 minutes)
bot.run_continuous_monitoring("AAPL", interval_minutes=60, execute=False)
```

## 📈 Key Concepts Explained

### Technical Indicators

| Indicator | Formula | What it means |
|-----------|---------|---------------|
| **RSI** | Relative Strength Index over 14 days | Momentum (>70 = overbought, <30 = oversold) |
| **MACD** | 12-day EMA - 26-day EMA | Trend and momentum changes |
| **MA 50** | Average closing price over 50 days | Short-term trend |
| **MA 200** | Average closing price over 200 days | Long-term trend |
| **Golden Cross** | MA 50 crosses above MA 200 | Bullish signal |
| **Death Cross** | MA 50 crosses below MA 200 | Bearish signal |

### Position Sizing

```
Risk Amount = Capital × Risk %
Quantity = Risk Amount / Current Price

Example:
Capital = $100,000
Risk % = 2%
Risk Amount = $100,000 × 0.02 = $2,000
Stock Price = $150

Quantity = $2,000 / $150 = 13 shares
```

This ensures you risk the same amount on each trade, regardless of stock price.

### AI Sentiment Analysis

Uses Google's Gemini LLM to analyze news headlines:

```
Input: ["Stock hits all-time high", "Analyst upgrades rating"]
Output: BULLISH (75% confidence)
```

Combined with technical signals:
- BUY + BULLISH = **STRONG BUY** 🚀
- BUY + BEARISH = **WEAK BUY** ⚠️
- BUY + NEUTRAL = **BUY**

## 📁 File Structure

```
stock-agent/
├── config.py          # All API keys and settings
├── data.py            # Fetch stock data (Phase 2)
├── signals.py         # Technical indicators (Phase 3)
├── sentiment.py       # AI sentiment analysis (Phase 4)
├── dashboard.py       # Interactive charts (Phase 5)
├── trader.py          # Paper trading automation (Phase 6)
└── README.md          # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
CAPITAL = 100000              # Your trading capital
RISK_PER_TRADE = 0.02         # 2% per trade
STOCK_SYMBOL = "AAPL"         # Default stock to track
DAYS_BACK = 100               # Historical data (days)
NEWS_HEADLINES = 5            # Sentiment analysis headlines
```

## 📊 Example Workflow

### Day 1 - Setup & Testing

```python
# 1. Test data fetching
python data.py

# 2. Test technical signals
python signals.py

# 3. Test sentiment analysis
python sentiment.py
```

### Day 2+ - Analysis & Trading

```python
# 1. Generate dashboard
python dashboard.py

# 2. Check signal (dry-run)
python trader.py

# 3. Run continuous monitoring (optional)
# Modify trader.py main to enable continuous monitoring
# Uncomment: bot.run_continuous_monitoring("AAPL", interval_minutes=60, execute=True)
```

## ⚠️ Important Notes

### Paper Trading (SAFE)
✅ **Paper trading is 100% risk-free** - no real money is used
✅ Great for testing your strategy
✅ No losses, no gains (virtual portfolio)

### Before Live Trading
⚠️ **NEVER** use real money without:
1. Extensively testing the strategy on historical data (backtesting)
2. Running paper trading for at least 1-2 months
3. Understanding the risks: past performance ≠ future results
4. Consulting with a financial advisor

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'talib'"**
```powershell
# TALib can be tricky on Windows. Try:
pip install TA-Lib

# If that fails, use alternatives:
pip install ta  # Or use pandas_ta instead of talib
```

**Issue: "API rate limit exceeded"**
- NewsAPI free tier: 100 requests/day
- Gemini API: Generous free tier
- Reduce `NEWS_HEADLINES` in config.py or increase `interval_minutes`

**Issue: "Connection refused to Alpaca"**
- Check API keys in config.py
- Ensure using PAPER trading URL (not live)
- Test connection: `python trader.py`

## 🚀 Future Enhancements

After completing the base project, consider adding:

1. **Backtesting** - Test strategy on historical data
   ```python
   from backtest import backtest_strategy
   results = backtest_strategy("AAPL", start="2023-01-01", end="2024-01-01")
   ```

2. **Telegram Alerts** - Get notifications on your phone
   ```python
   send_telegram_alert(f"STRONG BUY signal on {symbol}")
   ```

3. **Multi-stock Portfolio** - Track multiple stocks
   ```python
   stocks = ["AAPL", "MSFT", "GOOGL", "RELIANCE.NS"]
   for stock in stocks:
       bot.check_signal_and_trade(stock)
   ```

4. **Web Dashboard** - Deploy using Streamlit
   ```bash
   streamlit run dashboard_web.py
   ```

5. **Discord Bot** - Share signals with your community
   ```python
   send_discord_message(f"Trading signal: {combined}")
   ```

## 📚 Learning Resources

- **Technical Analysis**: https://www.investopedia.com/terms/t/technicalanalysis.asp
- **RSI Indicator**: https://www.investopedia.com/terms/r/rsi.asp
- **MACD**: https://www.investopedia.com/terms/m/macd.asp
- **Position Sizing**: https://www.investopedia.com/terms/p/positionsizing.asp
- **Paper Trading**: https://alpaca.markets/docs/trading/paper-trading/

## 📞 Support

If you encounter issues:
1. Check the "Common Issues" section above
2. Verify all API keys are correct in `config.py`
3. Ensure internet connection for API calls
4. Test each module individually before combining

## 📄 License

This project is educational. Use at your own risk for trading decisions.

---

**Happy trading! 📈🚀**
