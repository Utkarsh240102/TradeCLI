import urllib.request
import re

url = "https://binance-docs.github.io/apidocs/futures/en/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'.{0,50}Algo Order API.{0,50}', html, re.IGNORECASE)
    print("Found:", list(set(matches)))
except Exception as e:
    print(e)
