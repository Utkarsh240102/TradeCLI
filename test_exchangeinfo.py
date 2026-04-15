import sys
import requests
resp = requests.get('https://testnet.binancefuture.com/fapi/v1/exchangeInfo')
info = resp.json()
print("Order Types for BTCUSDT:", [s['orderTypes'] for s in info['symbols'] if s['symbol'] == 'BTCUSDT'])
