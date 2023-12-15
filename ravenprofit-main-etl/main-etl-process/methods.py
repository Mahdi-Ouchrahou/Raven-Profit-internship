import json
import csv
import os
import pandas as pd
from datetime import date
import time
import requests
from pandas import json_normalize
import boto3
import awswrangler as wr


class Do:
    """
    Class containing the methods used in the etl process to get financial data.
    It contains the methods: get_json(), save_to_parquet(), json_to_pandas(), json_to_pandas_quandl()

    The tow first methods are generic, used with all data providers.
    json_to_pandas() method can be used in a ganeric case if no transformations are needed.
    json_to_pandas_quandl() method can only be used with QUANDL API, it gets data in pandas df from a nested json dictionary

    """
    def get_json(**args):
        """
        Function that get the json response from a given endpoint, it takes one parameter, an endpoint dictionary.
        The endpoint dictionary should contain the following keys: "url", "param", "header"
        Return the json outpus of theendpoint get request
        """
        response = requests.get(args['url'] , params=args['param'], headers=args['header'])
        print(response.status_code)
        return response.json()

    def save_to_parquet(df, ticker, dataprovider):
        """
        function that takes a single dataframe and a single ticker name
        it creates, from the data frame, a parquet file named with the respective data provider and ticker
        """
        if df.empty:
            print("empty dataframe")
        else:
            df.columns = df.columns.map(str)
            wr.s3.to_parquet(
                df=df,
                compression="snappy",
                path=f"s3://ravenprofit-datafeed-tests/{dataprovider}/{ticker}-snappy.parquet"
            )

    #    df.columns = df.columns.map(str)
    #    table = pyarrow.Table.from_pandas(df)
    #    pq.write_table(table,f"{ticker}-snappy.parquet")
    #    s3_client = boto3.client('s3')
    #    bucket = "ravenprofit-datafeed-tests"
    #    with open(f"{ticker}-snappy.parquet") as f:
    #        object = f.read()
    #        s3_client.put_object(Body=object, Bucket=bucket, Key=f"{dataprovider}/")




    def json_to_pandas_quandl(json):
        """Function to convert a given dictionary to a pandas dataframe.
        One parameter: dictionary to be converted.
        return selected colums data in a pandas dataframe.
        """
        try:
            data_df = (pd.DataFrame.from_dict(json['dataset_data']['data']))
        except KeyError as ke:
            print("the key you are looking for is not in data dictionary:", ke)
        else:
            data_df[0] = pd.to_datetime(data_df[0], utc=False)

        #    print(data_df)
        #    print(data_df.dtypes)
            return data_df


    def json_to_pandas(response):
        """
        function that takes a json response and convert it, in its brute
        format, into a pandas data frame then returns it.
        """
        data_df = pd.DataFrame.from_dict(response)
        return data_df
