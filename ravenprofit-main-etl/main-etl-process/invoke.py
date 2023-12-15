from tiingo import tiingo
from quandlapi import quandl
from iexcloudapi import iexcloud
import json
import boto3
from datetime import date
import os

"""
File to manually invoke lambda function.
"""


CURRENT_DATE=date.today().strftime("%Y-%m-%d")


tiingo_KEY = os.getenv("TIINGO_KEY")

def invoke_lambda(function_name, payload):
    payload_json = json.dumps(payload)
    payload_bytes = bytes(payload_json, encoding="utf8")
    s3_client = boto3.client("lambda")
    response = s3_client.invoke(
            FunctionName = function_name,
            InvocationType = "RequestResponse",
            Payload = payload_bytes
    )
    return response

def main():
    payload_tiingo = {"methods" : {
                          "get_json" : "Do.get_json",
                          "json_to_pandas" : "Do.json_to_pandas",
                          "save_to_parquet" : "Do.save_to_parquet"
                               },
                       "ticker" : "CGCRX",
                       "endpoint" : {'dataprovider_name' : 'TIINGOAPI',
                                     'url' : f"https://api.tiingo.com/tiingo/daily/CGCRX/prices",
                                     'param' : {'startDate' : '2020-1-1',
                                                'endDate' : CURRENT_DATE,
                                                'fromat' : 'json',
                                                'resampleFreq' : 'daily',
                                                'token' : tiingo_KEY,
                                                           },
                                      'header' : {'Content-Type': 'application/json' },
                                                }
                            }


    response  = invoke_lambda("etlprocess", payload_tiingo)
    print(response)

if __name__ == '__main__':
    main()
