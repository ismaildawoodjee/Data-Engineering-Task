import requests
import json
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3"

PING = "/ping"
COINS_LIST = "/coins/list"
SIMPLE_PRICE = "/simple/price"


def print_response(payload, params=None):
    """Prints response from server based on a HTTP GET request."""
    
    response = requests.get(API_URL + payload, params=params)
    data = response.json()
    
    print(response.status_code)
    print(json.dumps(data, indent=2))


def get_data(payload, params=None):
    """Returns data from API server in json format."""

    response = requests.get(API_URL + payload, params=params)
    return response.json()


def data_to_csv(payload, params=None, name="data"):
    """
    Function to convert data from JSON to CSV, writing it
    into the `/data` folder.

    Args:
        payload (str): A HTTP GET request.
        params (dict, optional): Parameters in the get request. Defaults to None.
        name (str, optional): Name of CSV output. Defaults to "data".
    """

    data = get_data(payload, params=params)
    df = pd.DataFrame(data)
    df.to_csv(f"./data/{name}.csv", index=False)
    

if __name__ == "__main__":
    data_to_csv(payload=COINS_LIST, name="list_of_coins")
    

# data = get_data(payload=COINS_LIST)
# coins_df = pd.DataFrame(data)
# coins_df.to_csv("./data/list_of_coins.csv", index=False)

# ethereum = coins_df[coins_df['name'] == 'Ethereum']
# print(ethereum)

# print(coins_df.shape) # 7673 coins
# print(coins_df.head())