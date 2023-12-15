import boto3


#source code of the function
def sqs_lambda(event, context):
    """
    function to put a text file into an s3 bucket
    event: parameter dictionary of sqs message
    """
    s3_resource = boto3.resource("s3")
    index = 10
    for record in event["Records"]:
        data = record["body"]
        object = s3_resource.Object("bucket-to-test-sqs",f"testfile-{index}.txt")
        result = object.put(Body=data)
