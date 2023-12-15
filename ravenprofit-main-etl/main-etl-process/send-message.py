from tiingo import tiingo
from quandlapi import quandl
from iexcloudapi import iexcloud
#from eodapi import eodapi
import json
import boto3
from datetime import date
import os
from methods import Do



sqs_client = boto3.client("sqs")
sqs_resource = boto3.resource('sqs')

queue = sqs_resource.get_queue_by_name(QueueName='dead_letter_queue')
redrive_policy = {
    'deadLetterTargetArn': queue.attributes.get('QueueArn'),
    "maxReceiveCount" : "5",
}
response2 = sqs_client.set_queue_attributes(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
    Attributes={
        'RedrivePolicy': json.dumps(redrive_policy),
        "VisibilityTimeout" : "15"
    },
)


lambda_client = boto3.client("lambda")
response = lambda_client.update_event_source_mapping(
    UUID='ec893d0e-52b4-4e8b-a374-70902e0d2634',
    FunctionName='etlprocess',
    Enabled=True,
    BatchSize=10,
    MaximumBatchingWindowInSeconds=8,
    #MaximumRecordAgeInSeconds=10,

    )
"""
File to send messages to SQS that will automatically invoke the lambda function
with the send message.
Messages leading to failing invokations are moved to the dead-letter queue.


The code consist of multiple for loops, each one for a specific dataprovider.
The loop loops along a list containing all required lambda arguments for a specific tickers

Each dataprovider has a seperate .py file.
You can specify the number of tickers needed in the dataprovider file in question.

"""



for params in tiingo:
    param = json.dumps(params)

    sqs_client = boto3.client("sqs")

    #function to send message to sqs
    response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        MessageBody=param

    )

    #function to recieve a message from sqs
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        VisibilityTimeout=0
    )


for params in iexcloud:
    param = json.dumps(params)

    sqs_client = boto3.client("sqs")

    #function to send message to sqs
    response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        MessageBody=param

    )

    #function to recieve a message from sqs
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        VisibilityTimeout=0
    )


for params in quandl:
    param = json.dumps(params)

    sqs_client = boto3.client("sqs")

    #function to send message to sqs
    response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        MessageBody=param

    )

    #function to recieve a message from sqs
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        VisibilityTimeout=0
    )

"""
queue = sqs_resource.get_queue_by_name(QueueName='dead_letter_queue')
redrive_policy = {
    'deadLetterTargetArn': queue.attributes.get('QueueArn'),
    "maxReceiveCount" : "10",

}
for params in eodapi:
    param = json.dumps(params)
    sqs_client = boto3.client("sqs")
    #function to send message to sqs
    response = sqs_client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        MessageBody=param

    )

    #function to recieve a message from sqs
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
        VisibilityTimeout=0
    )
"""
