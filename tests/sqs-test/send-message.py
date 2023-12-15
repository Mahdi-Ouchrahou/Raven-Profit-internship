
#send message to a queue

import boto3
import json

sqs_client = boto3.client("sqs")

dic = {"methods" : {
                      "get_json" : "Do.get_json",
                      "json_to_pandas" : "Do.json_to_pandas",
                      "save_to_parquet" : "Do.save_to_parquet"
                           },
                   "ticker" : "CGCRX",
                   "endpoint" : {'dataprovider_name' : 'TIINGOAPI',
                                 'url' : f"https://api.tiingo.com/tiingo/daily/CGCRX/prices",
                                 'param' : {'startDate' : '2020-1-1',
                                            'endDate' : "XXXXXX",
                                            'fromat' : 'json',
                                            'resampleFreq' : 'daily',
                                            'token' : "XXXX",
                                                       },
                                  'header' : {'Content-Type': 'application/json' },
                                            }
                        }
json = json.dumps(dic)




response1 = sqs_client.send_message(
QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/test_queue',
MessageBody=json

)
esponse1 = sqs_client.receive_message(
QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/test_queue',
)


"""
response2 = sqs_client.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/test_queue',
    MessageBody="did it work?",

)

response2 = sqs_client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/test_queue',
)
"""
