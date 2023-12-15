import boto3
import json

"""
This file creates an event source mapping between our Lambda function and our
SQS queue.
It specifies a dead-letter queue, where messages that are not processed by Lambda
get stored.
"""


#Declaring lambda clients to use with boto3
lambda_client = boto3.client("lambda")


#function to create an event source mapping between lambda and an SQS queue
response = lambda_client.create_event_source_mapping(
    EventSourceArn="arn:aws:sqs:us-east-1:746274870646:triggers_queue",
    FunctionName='etlprocess',
    Enabled=True,

)
