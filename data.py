"""
Phase 2: Fetch Stock Data
Uses yfinance to retrieve historical OHLCV data for any stock.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep
from config import DAYS_BACK, STOCK_SYMBOL, USE_SAMPLE_DATA_ON_FAILURE


def generate_sample_data(days_back: int = DAYS_BACK, base_price: float = 100.0) -> pd.DataFrame:
    """Generate local sample OHLCV data for offline testing."""
    periods = max(days_back, 30)
    dates = pd.date_range(end=datetime.now(), periods=periods, freq="B")

    rng = np.random.default_rng(42)
    returns = rng.normal(0.0005, 0.02, size=len(dates))
    close = base_price * np.cumprod(1 + returns)

    open_prices = close * (1 + rng.normal(0.0, 0.005, size=len(dates)))
    high = np.maximum(open_prices, close) * (1 + rng.uniform(0.0, 0.01, size=len(dates)))
    low = np.minimum(open_prices, close) * (1 - rng.uniform(0.0, 0.01, size=len(dates)))
    volume = rng.integers(200_000, 2_000_000, size=len(dates))

    df = pd.DataFrame(
        {
            "Open": open_prices,
            "High": high,
            "Low": low,
            "Close": close,
            "Adj Close": close,
            "Volume": volume,
        },
        index=dates,
    )
    return df.round(2)


def fetch_stock_data(symbol: str, days_back: int = DAYS_BACK) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a stock.
    
    Args:
        symbol: Stock ticker (e.g., 'RELIANCE.NS', 'AAPL', 'MSFT')
        days_back: Number of days to fetch (default 100)
    
    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, (and Adj Close)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    print(f"Fetching {days_back} days of data for {symbol}...")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    
    try:
        # Download data from Yahoo Finance with retries and period fallback.
        data = None
        errors = []

        for attempt in range(3):
            try:
                data = yf.download(
                    symbol,
                    start=start_date,
                    end=end_date,
                    progress=False,
                    auto_adjust=False,
                    threads=False,
                )
                if data is not None and not data.empty:
                    break
            except Exception as inner_e:
                errors.append(str(inner_e))

            sleep(1 + attempt)

        if data is None or data.empty:
            # Fallback: Yahoo period-based query sometimes succeeds when date ranges fail.
            data = yf.download(
                symbol,
                period=f"{max(days_back, 30)}d",
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False,
            )
        
        if data.empty:
            print(f"❌ No data found for symbol: {symbol}")
            if errors:
                print(f"Last error: {errors[-1]}")
            if USE_SAMPLE_DATA_ON_FAILURE:
                print("⚠️ Using local sample OHLCV data fallback for offline simulation")
                return generate_sample_data(days_back=days_back)
            return None
        
        print(f"✅ Successfully fetched {len(data)} rows of data")
        print(f"\nLast 5 rows:")
        print(data.tail())
        
        return data
    
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None


def get_latest_price(symbol: str) -> float:
    """
    Get the latest closing price for a stock.
    
    Args:
        symbol: Stock ticker
    
    Returns:
        Latest closing price
    """
    try:
        ticker = yf.Ticker(symbol)
        latest_price = ticker.info.get('currentPrice') or ticker.info.get('regularMarketPrice')
        return latest_price
    except Exception as e:
        print(f"❌ Error getting latest price for {symbol}: {e}")
        return None


if __name__ == "__main__":
    # Test: Fetch RELIANCE (Indian stock) or AAPL (US stock)
    symbol = STOCK_SYMBOL
    data = fetch_stock_data(symbol, days_back=30)
    
    if data is not None:
        print(f"\n📊 Data shape: {data.shape}")
        print(f"Columns: {list(data.columns)}")
