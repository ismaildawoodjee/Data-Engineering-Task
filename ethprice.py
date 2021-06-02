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
    return response.json()

data = get_data(payload=COINS_LIST)
coins_df = pd.DataFrame(data)
coins_df.to_csv("./data/list_of_coins.csv", index=False)

# ethereum = coins_df[coins_df['name'] == 'Ethereum']
# print(ethereum)

# print(coins_df.shape) # 7673 coins
# print(coins_df.head())