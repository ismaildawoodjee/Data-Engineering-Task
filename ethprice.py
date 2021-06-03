import requests
import json
import pandas as pd
from datetime import datetime

API_URL = "https://api.coingecko.com/api/v3"

COIN = "ethereum"
PING = "/ping"
COINS_LIST = "/coins/list"
SIMPLE_PRICE = "/simple/price"
COIN_OHLC = f"/coins/{COIN}/ohlc"

COIN_IDS = [
    "ethereum",
    "cardano",
    "dogecoin",
    "litecoin",
    "polkadot",
    "uniswap",
    "stellar",
    "tron",
    "monero",
    "dash"
]

# parameters for `SIMPLE_PRICE` payload
# provide a comma separated string, WITHOUT spaces, for `ids` parameter
SP_PARAMS = {
    "ids": ",".join(COIN_IDS),
    "vs_currencies": "usd,btc",
    "include_market_cap": "true",
    "include_24hr_vol": "false",
    "include_24hr_change": "true",
    "include_last_updated_at": "true"
}

# parameters for `COIN_OHLC` payload
OHLC_PARAMS = {
    "id": COIN,
    "vs_currency": "usd",
    "days": 14
}


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
    
    # get all coin IDs
    coins_data = get_data(payload=COINS_LIST)
    
    # unfortunately, this gave a JSONDecodeError that I couldn't fix
    # coin_ids = [coin["id"] for coin in coins_data]
    
    # get cryptocurrency current prices ordered by market cap
    sp_data = get_data(payload=SIMPLE_PRICE, params=SP_PARAMS)
    crypto_df = pd.DataFrame(sp_data).transpose()
    crypto_df['last_updated_at'] = [datetime.fromtimestamp(time) for time in crypto_df['last_updated_at']]
    crypto_df = crypto_df.sort_values(by="usd_market_cap", ascending=False).reset_index()
    
    # get the OHLC (open-high-low-close) prices for Ethereum in the last 14 days
    eth_data = get_data(payload=COIN_OHLC, params=OHLC_PARAMS)
    eth_df = pd.DataFrame(eth_data, columns=["time", "open", "high", "low", "close"])
    eth_df["time"] = [datetime.fromtimestamp(time/1000) for time in eth_df["time"]]
    
    # output CSV files
    data_to_csv(payload=COINS_LIST, name="list_of_coins")
    crypto_df.to_csv("./data/ten_cryptos_data.csv", index=False)
    eth_df.to_csv("./data/ethereum_pasttwo_weeks.csv", index=False)
    