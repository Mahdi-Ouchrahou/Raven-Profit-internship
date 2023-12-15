from datetime import date
import time
import os
import csv
import requests
import pandas as pd




iexcloud_KEY = os.getenv("IEXCLOUD_KEY")
eodapi_KEY = os.getenv("EODAPI_KEY")


class Get:
    """
    The Get class contains all methods needed to extract tickers from data providers.
    It contains two generic functions to extract tickers from a given csv file in the directory: get_tickers(), get_filtered_tickers()
    The rest of the methods are specific to each data provider.
    """
    def get_eodapi_exchange(range=None):
        """
        Method to get list of exchanges from EOD API.
        It uses the exchange endpoints, make a call and return the exchanges as a list.
        It optionally take a range parameter to specify the needed number of exchanges
        """
        try:
            r = requests.get(f"https://eodhistoricaldata.com/api/exchanges-list/?api_token={eodapi_KEY}&fmt=json")
            print(r.status_code)
        except requests.exceptions.HTTPError as errh: #HTTP not found
            print("not found")
        except requests.exceptions.ConnectionError as errc: #handle connection errors
            print("connection error")
        except requests.exceptions.Timeout as errt: #request takes many time to complete
            print("request took too long")
        except requests.exceptions.RequestException as err:
            print(Err)
        else:
            df = pd.DataFrame.from_dict(r.json())
            #print(df)
            all_exchanges = df['Code'].to_list()
            #print(all_exchanges[:10])
            return all_exchanges[:range]

    def get_eod_tickers(exchange, range=None):
        """
        Method to get tickers from a choosen exchange from EOD API.
        It uses the symbols endpoint and return a list of all tickers of the given exchange.
        It takes two parameters: the wanted exchange and an optional range to specify number of tickers wanted
        """
        try:
            r = requests.get(f"https://eodhistoricaldata.com/api/exchange-symbol-list/{exchange}?api_token={eodapi_KEY}&fmt=json")
        except requests.exceptions.HTTPError as errh: #HTTP not found
            print(errh)
        except requests.exceptions.ConnectionError as errc: #handle connection errors
            print(errc)
        except requests.exceptions.Timeout as errt: #request takes many time to complete
            print(errt)
        except requests.exceptions.RequestException as err:
            print(Err)
        else:
            df = pd.DataFrame(r.json())
            tickers = df['Code'].to_list()
            #print(symbols_ofexchange)
            return tickers[:range]

    def get_iexcloud_ticker(exchange, range=None):
        """
        Method to get tickers from a choosen exchange from IEXCLOUD API.
        It uses the symbols endpoint and return a list of all tickers of the given exchange.
        It takes two parameters: the wanted exchange and an optional range to specify number of tickers wanted
        """
        url = f"https://cloud.iexapis.com/stable/ref-data/exchange/{exchange}/symbols?token={iexcloud_KEY}"
        r = requests.get(url)
        df = pd.DataFrame.from_dict(r.json())
        iexcloud_tickers=df['symbol'].to_list()
        return iexcloud_tickers[:range]


    def get_tickers(metadata, range=None):
        """
        Function to return selected tickers from the Metadata list of all tickers (in a range).
        Takes two parameters, starting and ending indeces of wanted tickers.
        Returns a list of selected tickers.
        EG: get_tickers(2, 20) --> tickers form index 2 to index 20 in the order of the metadata
        """
        with open(metadata) as f:
            reader=csv.reader(f)
            header=next(reader)
            #print(header)
            all_tickers=[]
            for row in reader:
                data = row[0]
                all_tickers.append(data)
        return all_tickers[:range]


    def get_filtered_tickers(metadata, selected_exchanges, range=None):
        """
        function that takes a list of exchanges and return all tickers associated with the given exchanges
        It may optionally take a second parameter, which is the range of the selected tickers
        EG: get_filtered_tickers(selected_exchanges, 2) --> 2 first tickers found in the exchanges mentioned in 'selected_exchanges'
        """
        with open(metadata) as f:
            reader=csv.reader(f)
            header=next(reader)
            #print(header)
            filtered_tickers=[row[0] for row in reader if row[1] in selected_exchanges]
            return filtered_tickers[:range]
