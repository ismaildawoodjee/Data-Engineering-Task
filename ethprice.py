import requests
import json

URL = "https://api.coingecko.com/api/v3"

PING = "/ping"
COINS_LIST = "/coins/list"
SIMPLE_PRICE = "/simple/price"

# try pinging the server
# response = requests.get(URL + PING)
# print(response.status_code, response.text)

def print_response(payload):
    """Prints response from server based on HTTP request."""
    
    response = requests.get(URL + payload)
    data = response.json()
    
    print(response.status_code)
    print(json.dumps(data, indent=2))

# print_response(payload=PING)
print_response(payload=COINS_LIST)