import boto3
import json
from methods import Do


"""
Main lambda handler that supports SQS queue triggers.
ETL process function: extract, transform to dataframe and save as a parquet file financial data from a given endpoint
It takes multiple parameters organized as follow:
    - ticker: ticker used in a single call
    - *methods: all functions that are used in the ETL process for one call
    - **data_provider: dictionary representing the endpoint used to exctract the data

"""


#code for lambda handler that does not support SQS triggers 
"""
# EVENT :
def lambda_handler(event, context):
    json = (eval(event["methods"]["get_json"])(**event["endpoint"]))
    if "json_to_pandas_quandl" in event["methods"].keys():
        data_df = (eval(event["methods"]["json_to_pandas_quandl"])(json))
    else:
        data_df = (eval(event["methods"]["json_to_pandas"])(json))
    #print(data_df)
    eval(event["methods"]["save_to_parquet"])(data_df, event["ticker"], event["endpoint"]['dataprovider_name'])
"""

def lambda_handler(event, context):
    for record in event["Records"]:
        json_param = record["body"]
        dict_param = json.loads(json_param)


        data_json  = (eval(dict_param["methods"]["get_json"])(**dict_param["endpoint"]))
        if "json_to_pandas_quandl" in dict_param["methods"].keys():
            data_df = (eval(dict_param["methods"]["json_to_pandas_quandl"])(data_json))
        else:
            data_df = (eval(dict_param["methods"]["json_to_pandas"])(data_json))

        eval(dict_param["methods"]["save_to_parquet"])(data_df, dict_param["ticker"], dict_param["endpoint"]['dataprovider_name'])
