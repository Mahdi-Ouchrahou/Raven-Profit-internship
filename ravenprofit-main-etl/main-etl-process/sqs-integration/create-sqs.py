import boto3
import json

"""
This file create a main queue trigger for lambda function and a dead-letter queue
to store failed lambda invocations.

It uses boto3 to interact with AWS SQS.

"""




#declaring sqs client and resource to use with boto3
sqs_client = boto3.client("sqs")
sqs_resource = boto3.resource('sqs')


#Creating the dead-letter-queue
response1 = sqs_client.create_queue(
    QueueName="dead_letter_queue"
)

#creating the redrive policy including the dead-letter queue ARN to use with the main queue
queue = sqs_resource.get_queue_by_name(QueueName='dead_letter_queue')
redrive_policy = {
    'deadLetterTargetArn': queue.attributes.get('QueueArn'),
    "maxReceiveCount" : "10",

}

#creating our main lambda queue trigger
response2 = sqs_client.create_queue(
    QueueName='triggers_queue',
    Attributes={
        'RedrivePolicy': json.dumps(redrive_policy)
    },
)


#Code to modify visibility time out of the main queue
"""
response = sqs_client.set_queue_attributes(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/746274870646/triggers_queue',
    Attributes={
        'VisibilityTimeout': '0'
    }
)
"""
