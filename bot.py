import os
import time
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import (
    SIDE_BUY,
    SIDE_SELL,
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC
)

# ================== CONFIGURATION ==================

load_dotenv()

logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================== BOT CLASS ==================

class BasicBot:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_SECRET_KEY")

        if not api_key or not api_secret:
            print("❌ Missing API credentials. Please check your .env file.")
            exit()

        # Initialize Binance Futures Testnet client
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        # Sync time offset
        self._sync_time()

        try:
            self.client.futures_account()
            print("✅ Connected successfully to Binance Futures Testnet!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            logging.error(f"Connection failed: {e}")

    def _sync_time(self):
        """Fix local time offset to prevent timestamp error"""
        server_time = self.client.futures_time()
        local_time = int(time.time() * 1000)
        diff = server_time["serverTime"] - local_time
        self.client.timestamp_offset = diff
        logging.info(f"Time synchronized. Offset: {diff} ms")

    def get_balance(self):
        """Fetch and display account USDT balance"""
        try:
            account = self.client.futures_account_balance()
            usdt_balance = next((x for x in account if x["asset"] == "USDT"), None)
            print(f"💰 Balance: {usdt_balance['balance']} USDT")
        except Exception as e:
            print(f"❌ Error fetching balance: {e}")
            logging.error(f"Balance fetch error: {e}")

    def place_market_order(self, symbol, side, quantity):
        """Place a market order"""
        try:
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=float(quantity)
            )
            print(f"✅ Market {side.upper()} order placed successfully!")
            print(f"📄 Order ID: {order['orderId']}")
            logging.info(f"Market order placed: {order}")
        except Exception as e:
            print(f"❌ Error placing market order: {e}")
            logging.error(f"Market order failed: {e}")

    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order"""
        try:
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                quantity=float(quantity),
                price=str(price),
                timeInForce=TIME_IN_FORCE_GTC
            )
            print(f"✅ Limit {side.upper()} order placed at {price}!")
            print(f"📄 Order ID: {order['orderId']}")
            logging.info(f"Limit order placed: {order}")
        except Exception as e:
            print(f"❌ Error placing limit order: {e}")
            logging.error(f"Limit order failed: {e}")

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place a Stop-Limit order (correct Futures version)"""
        try:
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=SIDE_BUY if side.lower() == "buy" else SIDE_SELL,
                type="STOP",
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=float(quantity),
                price=str(limit_price),     # actual execution price (limit)
                stopPrice=str(stop_price),  # trigger price
                workingType="CONTRACT_PRICE"  # or "MARK_PRICE"
            )
            print(f"✅ Stop-Limit {side.upper()} order placed successfully!")
            print(f"🟡 Trigger (Stop): {stop_price} | 💰 Limit: {limit_price}")
            logging.info(f"Stop-Limit order placed: {order}")
        except Exception as e:
            print(f"❌ Error placing Stop-Limit order: {e}")
            logging.error(f"Stop-Limit order failed: {e}")

# ================== MAIN CLI ==================

if __name__ == "__main__":
    print("=== Binance Futures Trading Bot ===\n")
    bot = BasicBot()

    while True:
        print("\nAvailable commands: balance | buy | sell | limit | stop-limit | exit")
        command = input("👉 Enter command: ").strip().lower()

        if command == "exit":
            print("👋 Exiting bot.")
            break

        elif command == "balance":
            bot.get_balance()

        elif command in ["buy", "sell"]:
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            quantity = input("Enter quantity: ").strip()
            bot.place_market_order(symbol, command, quantity)

        elif command == "limit":
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            side = input("Buy or Sell? ").strip().lower()
            quantity = input("Enter quantity: ").strip()
            price = input("Enter limit price: ").strip()
            bot.place_limit_order(symbol, side, quantity, price)

        elif command == "stop-limit":
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            side = input("Buy or Sell? ").strip().lower()
            qty = float(input("Enter quantity: "))
            stop_price = float(input("Enter stop (trigger) price: "))
            limit_price = float(input("Enter limit (execution) price: "))
            bot.place_stop_limit_order(symbol, side, qty, stop_price, limit_price)

        else:
            print("⚠️ Invalid command. Try again.")
