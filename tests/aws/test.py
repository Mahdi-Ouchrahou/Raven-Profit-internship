import pandas
import boto3
import csv


#session = boto3.Session


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


#test = s3_resource.Bucket(name="test")
"""
session = boto3.session.Session()
region ={'LocationConstraint':session.region_name}
s3_resource.create_bucket(
        Bucket='test-01',
        CreateBucketConfiguration=region
        )
"""




buckets = s3_client.list_buckets()

for bucket in buckets['Buckets']:
    print(f"{bucket['Name']}\n")



bucket = s3_resource.Bucket("ravenprofit-datafeed-tests")


print(bucket)

for obj in bucket.objects.all():
    print(obj)



#bucket.put_object(Key='test.csv', Body=data)
#s3_resource.Bucket("ravenprofit-datafeed-tests").upload_file("/home/bloodycig/internship/ravenprofit-etl/etlprocess/aws/requirements.txt", "requirements.txt")

s3_resource.Object("ravenprofit-datafeed-tests", "requirements.txt").delete()

for obj in bucket.objects.all():
    print(obj)


#for bucket in buckets['Buckets']:
#    print(f"{bucket['Name']}\n")
