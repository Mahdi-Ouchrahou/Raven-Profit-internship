from datetime import date
import os
import itertools

from tiingo import tiingo
from quandlapi import quandl
from iexcloudapi import iexcloud
#from eodapi import eod

from methods import Do


def etl_process(ticker, *methods, **data_provider):
    """
    Main ETL process function: extract, transform to dataframe and save as a parquet file financial data from a given endpoint
    It takes multiple parameters organized as follow:
        - ticker: ticker used in a single call
        - *methods: all functions that are used in the ETL process for one call
        - **data_provider: dictionary representing the endpoint used to exctract the data
    """
    json = Do.get_json(**data_provider)
    if Do.json_to_pandas_quandl in methods:
        data_df = Do.json_to_pandas_quandl(json)
    else:
        data_df = Do.json_to_pandas(json)
    print(data_df)
    Do.save_to_parquet(data_df, ticker, data_provider['dataprovider_name'])



def main():
    for (ticker, endpoint) in zip(tiingo['tickers'], tiingo['endpoints']):
        etl_process(ticker, Do.get_json, Do.json_to_pandas, Do.save_to_parquet, **endpoint)

    quandl_column = ['dataset_data', 'data']
    for (ticker, endpoint) in zip(quandl['tickers'], quandl['endpoints']):
        etl_process(ticker, Do.get_json, Do.json_to_pandas_quandl, Do.save_to_parquet, **endpoint)


    for (ticker, endpoint) in zip(iexcloud['tickers'], iexcloud['endpoints']):
        etl_process(ticker, Do.get_json, Do.json_to_pandas, Do.save_to_parquet, **endpoint)


    #for (ticker, endpoint) in zip(eodapi_tickers, eodapi_endpoints):
    #    etl_process(ticker, Do.get_json, Do.json_to_pandas, Do.save_to_parquet, **endpoint)



main()
