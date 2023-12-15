#!/bin/bash

aws lambda create-function --region us-east-1 \
    --function-name sqs-test \
    --runtime python3.8 \
    --role arn:aws:iam::746274870646:role/datafeed_test_lambda_role \
    --handler code.sqs_lambda \
    --package-type Zip \
    --zip-file fileb:////home/bloodycig/internship/sqs-test/deployment-package.zip \
    --timeout 900
