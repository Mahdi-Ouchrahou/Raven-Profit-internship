import json
import csv
import os
import pandas as pd
from datetime import date
import time
import requests

API_KEY = os.getenv("iexcloud_api_key")


#available exchanges for international symbols
all_exchanges = ["TSE",
                "LON",
                "KRX",
                "MEX",
                "BOM",
                "TSX",
                "TAE",
                "PAR",
                "ETR",
                "AMS",
                "BRU",
                "DUB",
                "LIS",
                "ADS"]

#function to return a list of international symbols given one of the listed exchanges
def get_international_symbols(exchange):
    url = f"https://cloud.iexapis.com/stable/ref-data/exchange/{exchange}/symbols?token={API_KEY}"
    r = requests.get(url)
    df = pd.DataFrame.from_dict(r.json())
    international_symbols=df['symbol'].to_list()
    #for symbol in international_symbols:
    #    print(symbol)
    return international_symbols

#function to get historical prices
def get_historical_prices(symbols, number_of_symbols, range=None, date=None):
    for symbol in symbols[:number_of_symbols]:
        url = f"https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range}?chartCloseOnly=True&token={API_KEY}"
        r = requests.get(url)
        df = pd.DataFrame.from_dict(r.json())
        df['date'] = pd.to_datetime(df['date'], utc=False)
        #print(df.dtypes)
        print(df)




symbols_list = get_international_symbols(all_exchanges[4])
range = "1y"
get_historical_prices(symbols_list, 5, range)
