import sys
from bot.client import BinanceClient

client = BinanceClient()

print("Trying /fapi/v1/algo/order")
try:
    print(client.post("/fapi/v1/algo/order", {"symbol": "BTCUSDT", "side": "SELL", "type": "STOP_MARKET", "quantity": 0.01, "stopPrice": 60000}))
except Exception as e:
    print(e)
