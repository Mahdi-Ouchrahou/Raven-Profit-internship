import boto3



lambda_client = boto3.client("lambda")
#create event source mapping

response = lambda_client.create_event_source_mapping(
    EventSourceArn="arn:aws:sqs:us-east-1:746274870646:test_queue",
    FunctionName='sqs-test',
    Enabled=True,

#    DestinationConfig = {
#        'OnSuccess': {
#            'Destination': 'string'
#        },
#        'OnFailure': {
#            'Destination': 'string'
#        }
#    },

)
