import urllib.request
import urllib.parse
import json

q = urllib.parse.urlencode({"q": "Binance API error [-4120]: Order type not supported for this endpoint"})
req = urllib.request.Request(f"https://api.duckduckgo.com/v1/?{q}&format=json", headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
except Exception as e:
    print(e)
