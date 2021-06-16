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
        params (dict, optional): Parameters in the GET request.
            Defaults to None.
        name (str, optional): Name of CSV output. Defaults to "data".
    """

    data = get_data(payload, params=params)
    df = pd.DataFrame(data)
    df.to_csv(f"./data/{name}.csv", index=False)


def get_current_prices(payload, params):
    """
    Gets the most recent, current prices of 10 cryptos specified in`COIN_IDS`.
    Simple transformations are done to put the data into the correct shape,
    renaming some columns, and converting Unix timestamp to datetime.

    Args:
        payload (str): A HTTP GET request.
        params (dict): Parameters in the GET request

    Returns:
        dataframe: Cryptocurrency details, ordered by market cap.
    """

    sp_data = get_data(payload=payload, params=params)
    crypto_df = pd.DataFrame(sp_data) \
        .transpose() \
        .sort_values(by="usd_market_cap", ascending=False) \
        .reset_index() \
        .rename({
            "index": "name",
            "usd": "price_in_usd",
            "btc": "price_in_btc"
        })

    crypto_df['last_updated_at'] = [
        datetime.fromtimestamp(time) for time in crypto_df['last_updated_at']
    ]

    return crypto_df


def get_ethereum_data(payload, params):
    """Gets the OHLC (open-high-low-close) prices, or candlestick data, for
    Ethereum in the last 14 days. The provided Unix timestamp was incorrectly
    multiplied by 1000, so a transformation was done to rectify this.

    Args:
        payload (str): A HTTP GET request.
        params (dict): Parameters for the GET request.

    Returns:
        dataframe: Ethereum OHLC dataframe for the past 14 days.
    """

    # get OHLC (open-high-low-close) prices for Ethereum in the last 14 days
    eth_data = get_data(payload=payload, params=params)
    eth_df = pd.DataFrame(eth_data, columns=[
        "time", "open", "high", "low", "close"
    ])
    eth_df["time"] = [
        datetime.fromtimestamp(time/1000) for time in eth_df["time"]
    ]

    return eth_df


if __name__ == "__main__":

    # get all coin IDs
    coins_data = get_data(payload=COINS_LIST)
    # coin_ids = [coin["id"] for coin in coins_data]

    # Unfortunately, using the above list for the `/simple/price` API gave
    # a JSONDecodeError that I couldn't fix

    # get the required dataframes for crypto prices and Ethereum data
    crypto_df = get_current_prices(payload=SIMPLE_PRICE, params=SP_PARAMS)
    eth_df = get_ethereum_data(payload=COIN_OHLC, params=OHLC_PARAMS)

    # output three dataframes as CSV files
    data_to_csv(payload=COINS_LIST, name="list_of_coins")
    crypto_df.to_csv("./data/ten_cryptos_data.csv", index=False)
    eth_df.to_csv("./data/ethereum_pasttwo_weeks.csv", index=False)
