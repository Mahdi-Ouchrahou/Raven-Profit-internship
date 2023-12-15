#!/bin/bash

aws lambda create-function --region us-east-1 \
    --function-name etlprocess \
    --package-type Image \
    --timeout 90 \
    --code ImageUri=746274870646.dkr.ecr.us-east-1.amazonaws.com/etl-process:latest \
    --dead-letter-config TargetArn=arn:aws:sqs:us-east-1:746274870646:dead_letter_queue \
    --role arn:aws:iam::746274870646:role/datafeed_test_lambda_role
