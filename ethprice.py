import requests
from pycoingecko import CoinGeckoAPI

URL = "https://api.coingecko.com/api/v3"

PING = "/ping"

# try pinging the server
response = requests.get(URL + PING)
print(response.status_code, response.text)

cg = CoinGeckoAPI()
print(cg.ping())

