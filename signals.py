"""
Phase 3: Technical Indicators & Signals
Uses ta (Technical Analysis) library to calculate RSI, MACD, Moving Averages.
Generates BUY/SELL signals based on indicator combinations.
"""

import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from config import CAPITAL, RISK_PER_TRADE
from data import fetch_stock_data


def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators: RSI, MACD, Moving Averages.
    
    Args:
        data: DataFrame with OHLCV data
    
    Returns:
        DataFrame with added indicator columns
    """
    df = data.copy()
    
    # RSI (Relative Strength Index) - default period 14
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()

    # MACD (Moving Average Convergence Divergence)
    macd = MACD(close=df['Close'], window_fast=12, window_slow=26, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Hist'] = macd.macd_diff()

    # Moving Averages
    df['MA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['MA_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
    
    # Golden Cross / Death Cross signals
    df['Golden_Cross'] = (df['MA_50'] > df['MA_200']).astype(int)
    
    return df


def generate_signals(data: pd.DataFrame, symbol: str) -> dict:
    """
    Generate BUY/SELL signals based on technical indicators.
    
    Signal Rules:
    - BUY: RSI < 30 AND MACD > Signal line (bullish crossover)
    - SELL: RSI > 70 AND MACD < Signal line (bearish crossunder)
    
    Args:
        data: DataFrame with indicator columns
        symbol: Stock symbol (for display)
    
    Returns:
        Dictionary with signal info and position sizing
    """
    # Ensure indicators are calculated
    if 'RSI' not in data.columns:
        data = calculate_indicators(data)
    
    latest = data.iloc[-1]
    
    rsi = latest['RSI']
    macd = latest['MACD']
    macd_signal = latest['MACD_Signal']
    ma_50 = latest['MA_50']
    ma_200 = latest['MA_200']
    close_price = latest['Close']
    
    # Initialize signal
    signal = "NEUTRAL"
    signal_strength = 0
    
    # BUY Conditions
    if rsi < 30 and macd > macd_signal:
        signal = "BUY"
        signal_strength = abs(30 - rsi) / 30  # Strength based on RSI distance
    
    # SELL Conditions
    elif rsi > 70 and macd < macd_signal:
        signal = "SELL"
        signal_strength = (rsi - 70) / 30  # Strength based on RSI distance
    
    # Additional context from Moving Averages
    trend = "BULLISH" if ma_50 > ma_200 else "BEARISH"
    
    # Position Sizing (real trader risk management)
    quantity = calculate_position_size(close_price)
    
    result = {
        "signal": signal,
        "signal_strength": float(signal_strength),
        "trend": trend,
        "rsi": float(round(rsi, 2)) if pd.notna(rsi) else None,
        "macd": float(round(macd, 4)) if pd.notna(macd) else None,
        "macd_signal": float(round(macd_signal, 4)) if pd.notna(macd_signal) else None,
        "ma_50": float(round(ma_50, 2)) if pd.notna(ma_50) else None,
        "ma_200": float(round(ma_200, 2)) if pd.notna(ma_200) else None,
        "close_price": float(round(close_price, 2)),
        "quantity": quantity,
        "symbol": symbol,
    }
    
    return result


def calculate_position_size(stock_price: float) -> int:
    """
    Calculate position size based on 2% risk per trade.
    
    Formula: quantity = (capital × 0.02) / stock_price
    This is standard risk management used by professional traders.
    
    Args:
        stock_price: Current price of the stock
    
    Returns:
        Number of shares to buy/sell
    """
    risk_amount = CAPITAL * RISK_PER_TRADE
    quantity = int(risk_amount / stock_price)
    return max(quantity, 1)  # At least 1 share


def print_signal_report(signal_dict: dict):
    """
    Pretty-print the signal analysis.
    """
    print("\n" + "="*60)
    print(f"📊 SIGNAL REPORT - {signal_dict['symbol']}")
    print("="*60)
    print(f"Signal: {signal_dict['signal']} (Strength: {signal_dict['signal_strength']:.2%})")
    print(f"Trend: {signal_dict['trend']}")
    print(f"\n📈 Indicators:")
    print(f"  RSI (14): {signal_dict['rsi']} {'(Overbought ⚠️)' if signal_dict['rsi'] > 70 else '(Oversold ⚠️)' if signal_dict['rsi'] < 30 else ''}")
    print(f"  MACD: {signal_dict['macd']:.4f} (Signal: {signal_dict['macd_signal']:.4f})")
    print(f"  MA 50: {signal_dict['ma_50']}")
    print(f"  MA 200: {signal_dict['ma_200']}")
    print(f"\n💰 Trading Info:")
    print(f"  Current Price: ${signal_dict['close_price']}")
    print(f"  Position Size: {signal_dict['quantity']} shares")
    print(f"  Risk Amount: ${CAPITAL * RISK_PER_TRADE:,.2f}")
    print("="*60 + "\n")


if __name__ == "__main__":
    from config import STOCK_SYMBOL
    
    # Test: Fetch data and generate signals
    data = fetch_stock_data(STOCK_SYMBOL, days_back=100)
    
    if data is not None:
        data_with_indicators = calculate_indicators(data)
        signal = generate_signals(data_with_indicators, STOCK_SYMBOL)
        print_signal_report(signal)
