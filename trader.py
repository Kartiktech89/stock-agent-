"""
Phase 6: Local Paper Trading Automation
Runs fully offline using a local JSON portfolio file.
No broker account or external trading API required.
"""

import json
import time
from datetime import datetime
from pathlib import Path

from config import CAPITAL, PORTFOLIO_FILE
from data import fetch_stock_data
from sentiment import analyze_sentiment_with_gemini, combine_signals, fetch_news_headlines
from signals import calculate_indicators, generate_signals


class LocalPaperTradingBot:
    """Local paper trading simulator backed by a JSON portfolio file."""

    def __init__(self, portfolio_file: str = PORTFOLIO_FILE):
        self.portfolio_path = Path(portfolio_file)
        self._ensure_portfolio_exists()

    def _ensure_portfolio_exists(self) -> None:
        if self.portfolio_path.exists():
            return

        initial_state = {
            "cash": float(CAPITAL),
            "positions": {},
            "trade_history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self._save_portfolio(initial_state)
        print(f"✅ Created local paper portfolio at {self.portfolio_path}")

    def _load_portfolio(self) -> dict:
        with self.portfolio_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_portfolio(self, portfolio: dict) -> None:
        portfolio["updated_at"] = datetime.now().isoformat()
        with self.portfolio_path.open("w", encoding="utf-8") as file:
            json.dump(portfolio, file, indent=2)

    def _record_trade(self, portfolio: dict, action: str, symbol: str, qty: int, price: float) -> None:
        trade_value = round(qty * price, 2)
        portfolio["trade_history"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "symbol": symbol,
                "qty": qty,
                "price": round(price, 2),
                "value": trade_value,
            }
        )

    def submit_buy_order(self, symbol: str, quantity: int, market_price: float) -> dict:
        portfolio = self._load_portfolio()
        cost = round(quantity * market_price, 2)

        if cost > portfolio["cash"]:
            return {
                "status": "rejected",
                "reason": f"Insufficient cash. Needed ${cost:,.2f}, available ${portfolio['cash']:,.2f}",
            }

        current = portfolio["positions"].get(symbol, {"qty": 0, "avg_entry_price": 0.0})
        current_qty = int(current["qty"])
        current_avg = float(current["avg_entry_price"])

        new_qty = current_qty + quantity
        new_avg = ((current_qty * current_avg) + (quantity * market_price)) / new_qty

        portfolio["cash"] = round(portfolio["cash"] - cost, 2)
        portfolio["positions"][symbol] = {
            "qty": new_qty,
            "avg_entry_price": round(new_avg, 2),
        }
        self._record_trade(portfolio, "buy", symbol, quantity, market_price)
        self._save_portfolio(portfolio)

        print(f"🟢 PAPER BUY: {quantity} shares of {symbol} @ ${market_price:.2f}")
        return {
            "status": "filled",
            "action": "buy",
            "symbol": symbol,
            "qty": quantity,
            "fill_price": round(market_price, 2),
            "cash_remaining": portfolio["cash"],
        }

    def submit_sell_order(self, symbol: str, quantity: int, market_price: float) -> dict:
        portfolio = self._load_portfolio()
        position = portfolio["positions"].get(symbol)

        if not position or int(position["qty"]) <= 0:
            return {"status": "rejected", "reason": f"No open position for {symbol}"}

        held_qty = int(position["qty"])
        sell_qty = min(quantity, held_qty)
        proceeds = round(sell_qty * market_price, 2)

        remaining_qty = held_qty - sell_qty
        if remaining_qty == 0:
            portfolio["positions"].pop(symbol, None)
        else:
            position["qty"] = remaining_qty
            portfolio["positions"][symbol] = position

        portfolio["cash"] = round(portfolio["cash"] + proceeds, 2)
        self._record_trade(portfolio, "sell", symbol, sell_qty, market_price)
        self._save_portfolio(portfolio)

        print(f"🔴 PAPER SELL: {sell_qty} shares of {symbol} @ ${market_price:.2f}")
        return {
            "status": "filled",
            "action": "sell",
            "symbol": symbol,
            "qty": sell_qty,
            "fill_price": round(market_price, 2),
            "cash_remaining": portfolio["cash"],
        }

    def get_position(self, symbol: str):
        portfolio = self._load_portfolio()
        position = portfolio["positions"].get(symbol)
        if not position:
            return None
        return {
            "symbol": symbol,
            "qty": int(position["qty"]),
            "avg_entry_price": float(position["avg_entry_price"]),
        }

    def get_portfolio_snapshot(self) -> dict:
        portfolio = self._load_portfolio()
        return {
            "cash": portfolio["cash"],
            "positions": portfolio["positions"],
            "trades": len(portfolio["trade_history"]),
            "last_update": portfolio["updated_at"],
        }

    def check_signal_and_trade(self, symbol: str, execute: bool = False) -> dict:
        print(f"\n{'=' * 60}")
        print(f"Checking local paper signal for {symbol}...")
        print(f"{'=' * 60}\n")

        data = fetch_stock_data(symbol, days_back=100)
        if data is None:
            return {"status": "error", "message": "Failed to fetch data"}

        data = calculate_indicators(data)
        technical_signal = generate_signals(data, symbol)

        headlines = fetch_news_headlines(symbol)
        sentiment = analyze_sentiment_with_gemini(headlines, symbol)
        combined = combine_signals(technical_signal["signal"], sentiment["sentiment"])

        print(f"📊 ANALYSIS RESULT: {combined}")

        if not execute:
            print("🔍 [DRY RUN] Local simulator ready. Set execute=True to write trades to portfolio.json")
            return {
                "status": "dry_run",
                "signal": technical_signal["signal"],
                "sentiment": sentiment["sentiment"],
                "combined": combined,
                "price": technical_signal["close_price"],
                "quantity": technical_signal["quantity"],
            }

        current_price = float(technical_signal["close_price"])
        if "STRONG BUY" in combined:
            return self.submit_buy_order(symbol, technical_signal["quantity"], current_price)
        if "STRONG SELL" in combined:
            position = self.get_position(symbol)
            if position:
                return self.submit_sell_order(symbol, position["qty"], current_price)

        return {"status": "no_trade", "reason": "Signal not strong enough for execution"}

    def run_continuous_monitoring(self, symbol: str, interval_minutes: int = 60, execute: bool = False):
        print(f"🤖 Starting local paper monitoring for {symbol}")
        print(f"Check interval: {interval_minutes} minutes")
        print(f"Trade execution: {'ENABLED' if execute else 'DISABLED (dry-run)'}")

        try:
            while True:
                result = self.check_signal_and_trade(symbol, execute=execute)
                print(f"Result: {result}")
                print(f"Next check in {interval_minutes} minutes...\n")
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")


if __name__ == "__main__":
    from config import STOCK_SYMBOL

    bot = LocalPaperTradingBot()
    print("Portfolio snapshot:", bot.get_portfolio_snapshot())

    result = bot.check_signal_and_trade(STOCK_SYMBOL, execute=False)
    print(f"\nResult: {result}")

    # To write simulated trades to portfolio.json:
    # result = bot.check_signal_and_trade(STOCK_SYMBOL, execute=True)

    # To run continuous monitoring:
    # bot.run_continuous_monitoring(STOCK_SYMBOL, interval_minutes=60, execute=False)
