import boto3


#create sqs queue
sqs_client = boto3.client("sqs")

response = sqs_client.create_queue(
    QueueName='test_queue',
     Attributes={
        'VisibilityTimeout': '900'
    },
)
