import json
import csv
import os
import pandas as pd
from datetime import date
import time
import requests
from pandas import json_normalize
import pyarrow.parquet as pq
import pyarrow




KEY = os.getenv("KEY")
METADATA = "BATS_metadata.csv"
CURRENT_DATE=date.today().strftime("%Y-%m-%d")

#in comments:
#arguments + explanation + example
#erturn value + explanation + example

def get_tickers(start, end):
    """
    Function to return selected tickers from the Metadata list of all tickers (in a range).
    Takes two parameters, starting and ending indeces of wanted tickers.
    Returns a list of selected tickers
    """
    with open(METADATA) as f:
        reader=csv.reader(f)
        header=next(reader)
        #print(header)
        all_tickers=[]
        for row in reader:
            data = row[0]
            all_tickers.append(data)
    #print(all_tickers[start:end])
    return all_tickers[start:end]


def convert_to_df(dict):
    """Function to convert a given dictionary to a pandas dataframe.
    One parameter: dictionary to be converted.
    return selected colums data in a pandas dataframe.
    """
    try:
        data_df = (pd.DataFrame.from_dict(dict['dataset_data']['data']))
    except KeyError as ke:
        print("the key you are looking for is not in data dictionary:", ke)
    else:
        data_df[0] = pd.to_datetime(data_df[0], utc=False)

    #    print(data_df)
    #    print(data_df.dtypes)
        return data_df


def request_json(ticker):
    """Function to make an API request from a specific dataset.
    One parameter: string ticker
    Returns the json response as a dataset dictionary
    """
    url = f"https://www.quandl.com/api/v3/datasets/BATS/{ticker}/data.json?start_date=2016-07-01&end_date={CURRENT_DATE}&api_key={KEY}"
    try:
        r = requests.get(url)
    except requests.exceptions.HTTPError as errh: #HTTP not found
        print(errh)
    except requests.exceptions.ConnectionError as errc: #handle connection errors
        print(errc)
    except requests.exceptions.Timeout as errt: #request takes many time to complete
        print(errt)
    except requests.exceptions.RequestException as err:
        print(Err)
    else:
        try:
            dataset_dict = r.json()
        except json.decoder.JSONDecodeError as e:
            print(e)
    #print(dataset_dict)
    return dataset_dict


def save_to_parquet(df, ticker):
    """Function to write to a csv file.
    Takes 2 parameters: the data frame object and the ticker string.
    No return type
    """
    df.columns = df.columns.map(str)
    table = pyarrow.Table.from_pandas(df)
    pyarrow.parquet.write_table(table, f'{ticker}_data.parquet', compression='SNAPPY')
    #df.to_parquet(f"{ticker}_data.parquet", index=False, compression='snappy', engine="pyarrow")
    pd.read_parquet(f"{ticker}_data.parquet")
    #print(df)


def get_data():
    """Function to get the final csv file from all selected tickers
    """
    selected_tickers=get_tickers(0, 3)
    for ticker in selected_tickers:
        dataset_dict = request_json(ticker)
        try:
            data_df = convert_to_df(dataset_dict)
        except KeyError as ke:
            print("the key you are looking for is not in data dictionary:", ke)
        else:
            save_to_parquet(data_df, ticker)

get_data()

#


"""
WHATS LEFT TO DO;
1)mabe functors
2) log function
"""
