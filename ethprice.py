import requests
import json
import pandas as pd

URL = "https://api.coingecko.com/api/v3"

PING = "/ping"
COINS_LIST = "/coins/list"
SIMPLE_PRICE = "/simple/price"

def print_response(payload, params=None):
    """Prints response from server based on HTTP request."""
    
    response = requests.get(URL + payload, params=params)
    data = response.json()
    
    print(response.status_code)
    print(json.dumps(data, indent=2))


def get_data(payload, params=None):
    """Returns data from API server in json format."""

    response = requests.get(URL + payload, params=params)
    data = response.json()
    
    return data 


# print_response(payload=PING)
# print_response(payload=COINS_LIST)

df = pd.DataFrame(get_data(payload=COINS_LIST))
print(df.head())