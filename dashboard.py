"""
Phase 5: Interactive Dashboard
Creates interactive charts with technical indicators and buy/sell signals.
Uses Plotly for visualization.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data import fetch_stock_data
from signals import calculate_indicators, generate_signals


def create_trading_dashboard(symbol: str, data: pd.DataFrame, signals_dict: dict) -> go.Figure:
    """
    Create an interactive Plotly dashboard with:
    - Candlestick chart with moving averages
    - RSI indicator
    - Buy/Sell signal markers
    - Sentiment box
    
    Args:
        symbol: Stock ticker
        data: DataFrame with OHLCV + indicators
        signals_dict: Signal analysis from generate_signals()
    
    Returns:
        Plotly Figure object
    """
    
    # Ensure indicators are calculated
    if 'RSI' not in data.columns:
        data = calculate_indicators(data)
    
    # Create subplots: candlestick + RSI
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3],
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # ========== Plot 1: Candlestick Chart ==========
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=f'{symbol} Price',
            yaxis='y1'
        ),
        row=1, col=1
    )
    
    # Moving Average 50
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MA_50'],
            mode='lines',
            name='MA 50',
            line=dict(color='orange', width=2),
            yaxis='y1'
        ),
        row=1, col=1
    )
    
    # Moving Average 200
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['MA_200'],
            mode='lines',
            name='MA 200',
            line=dict(color='blue', width=2),
            yaxis='y1'
        ),
        row=1, col=1
    )
    
    # ========== Plot 2: RSI Chart ==========
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI (14)',
            line=dict(color='purple', width=2),
            yaxis='y2'
        ),
        row=2, col=1
    )
    
    # RSI Oversold line (30)
    fig.add_hline(
        y=30, 
        line_dash="dash", 
        line_color="red",
        annotation_text="Oversold (30)",
        row=2, col=1
    )
    
    # RSI Overbought line (70)
    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="green",
        annotation_text="Overbought (70)",
        row=2, col=1
    )
    
    # ========== Add Buy/Sell Signal Markers ==========
    latest_idx = len(data) - 1
    if signals_dict['signal'] == 'BUY':
        fig.add_annotation(
            x=data.index[latest_idx],
            y=signals_dict['close_price'],
            text="🟢 BUY",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="green",
            font=dict(size=14, color="green"),
            row=1, col=1
        )
    elif signals_dict['signal'] == 'SELL':
        fig.add_annotation(
            x=data.index[latest_idx],
            y=signals_dict['close_price'],
            text="🔴 SELL",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="red",
            font=dict(size=14, color="red"),
            row=1, col=1
        )
    
    # ========== Update Layout ==========
    fig.update_layout(
        title={
            'text': f"<b>{symbol} - AI Stock Analysis Dashboard</b><br><sub>Technical Indicators + AI Sentiment</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        height=800,
        hovermode='x unified',
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
    )
    
    # Y-axis labels
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    
    return fig


def create_summary_text(signals_dict: dict, sentiment: dict) -> str:
    """
    Create a text summary with trading recommendation.
    """
    signal = signals_dict['signal']
    trend = signals_dict['trend']
    rsi = signals_dict['rsi']
    sentiment_val = sentiment.get('sentiment', 'NEUTRAL')
    
    text = f"""
    <b>Signal Analysis Summary:</b><br>
    Signal: <b>{signal}</b> ({signals_dict['signal_strength']:.0%} strength)<br>
    Trend: <b>{trend}</b><br><br>
    
    <b>Technical Indicators:</b><br>
    RSI: {rsi} {'(Overbought ⚠️)' if rsi > 70 else '(Oversold ⚠️)' if rsi < 30 else '(Neutral)'}<br>
    Trend: {trend}<br><br>
    
    <b>AI Sentiment:</b><br>
    {sentiment_val} (Confidence: {sentiment.get('confidence', 0)}%)<br><br>
    
    <b>Position Size:</b> {signals_dict['quantity']} shares<br>
    <b>Risk Amount:</b> ${signals_dict.get('risk_amount', 'N/A')}
    """
    
    return text


def save_dashboard(fig: go.Figure, symbol: str, filename: str = None):
    """
    Save dashboard as an HTML file.
    
    Args:
        fig: Plotly figure
        symbol: Stock symbol
        filename: Output filename (default: dashboard_{symbol}.html)
    """
    if filename is None:
        filename = f"dashboard_{symbol}.html"
    
    fig.write_html(filename)
    print(f"✅ Dashboard saved to {filename}")


if __name__ == "__main__":
    from config import STOCK_SYMBOL
    
    # Test: Create dashboard
    symbol = STOCK_SYMBOL
    data = fetch_stock_data(symbol, days_back=100)
    
    if data is not None:
        data_with_indicators = calculate_indicators(data)
        signals_dict = generate_signals(data_with_indicators, symbol)
        
        fig = create_trading_dashboard(symbol, data_with_indicators, signals_dict)
        fig.show()  # Opens in browser
        
        # Or save as HTML
        # save_dashboard(fig, symbol)
