import requests
import json
import pandas as pd
import os
from datetime import date
import time
import pyarrow.parquet as pq
import pyarrow


KEY = os.getenv("EODAPI_KEY")

CURRENT_DATE=date.today().strftime("%Y-%m-%d")



base_url = "https://eodhistoricaldata.com/api/"
endofday_endpoint = "eod/"
endofday_param = f"fmt=json&api_token={KEY}&period=d&from=2021-01-01&to={CURRENT_DATE}&filter=last_close"

exchange_endpoint= "exchanges-list/?"
exchange_param = f"api_token={KEY}&fmt=json"

symbol_endpoint = f"exchange-symbol-list/"
symbols_param = f"api_token={KEY}&fmt=json"


def get_exchange():
    try:
        r = requests.get(base_url+exchange_endpoint+exchange_param)
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
        return all_exchanges


def get_symbols(exchange):
    try:
        r = requests.get(base_url+symbol_endpoint+ f"{exchange}?"+symbols_param)
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
        symbols_ofexchange = df['Code'].to_list()
        print(symbols_ofexchange)
        return symbols_ofexchange


#function to get single ticker
def get_endofday_data(exchange, symbols_of_chosen_exchange):
    pairs = [f"{symbol}.{exchange}" for symbol in symbols_of_chosen_exchange]
    #print(pairs)
    df_list = []
    for pair in pairs:
        try:
            r = requests.get(base_url+endofday_endpoint+ f"{pairs}?"+endofday_param)
            #print(r.status_code)
        except requests.exceptions.HTTPError as errh: #HTTP not found
            print(errh)
        except requests.exceptions.ConnectionError as errc: #handle connection errors
            print(errc)
        except requests.exceptions.Timeout as errt: #request takes many time to complete
            print(errt)
        except requests.exceptions.RequestException as err:
            print(Err)
        else:
            data_df = pd.DataFrame(r.json())
            df_list.append(df)
    final_df = pd.concat(df_list)
    return final_df




def get_parquet_endofday(df, exchange):
    df['Date'] = pd.to_datetime(df['Date'], utc=False)
    df.columns = df.columns.map(str)
    table = pyarrow.Table.from_pandas(df)
    pyarrow.parquet.write_table(table, f'{exchange}_endofday.parquet', compression='SNAPPY')



exchanges_list = get_exchange()
for exchange in exchanges_list[0:1]:
    #print(all_exchanges[0])
    symbol_list = get_symbols(exchange)
    data_df = get_endofday_data(exchange, symbol_list[:20])
    get_parquet_endofday(data_df, exchange)
