   --> General description:
- Implementation of an AWS Lambda function. It requests, modify and saves (in a parquet
format) financial data, from API endpoints to specific AWS S3 bucket.
- The Lambda function is created and deployed using a docker image, contained in AWS ECR repository. (see documentation below)
- The Lambda function is triggered using an AWS SQS queue event source mapping.
- Lambda polls the queue and invokes your Lambda function synchronously with an event that contains queue messages.
- The SQS queue trigger is integrated with a dead-letter queue such that if a message fails to be processed multiple times
by Lambda, SQS send it to the dead-letter queue.


  --> General organization:
- Lambda handler code : "handler.py"
- Lambda creation bash file (CLI command) : "lambda-create.sh"
- Methods used to request, modify and save data : "methods.py"
- Methods to extract tickers for data providers : "get_tickers.py"
- Each data provider has it's own file, and their main purpose is to store (in a list) all parameters needed
by the lambda function to process once single ticker at a time. (done locally, independent from Lambda)
- SQS queue creation, dead-letter queue creation, event-source-mapping creation : "SQS-integration" folder
- Sending and receiving messages to SQS code : "send-message.py"
NB/all tokens are saved as environment variables and only used once, in each personalized data provider file.

   --> Deployment of Lambda function using container image step-by-step :
After installing the Docker Engine in a local machine and assuming the lambda handler
is written and bug-free:
  -STEP 1 : Create a docker file, it should contain the following:
            "FROM public.ecr.aws/lambda/python:version"
            "WORKDIR /work/dir"  --> specify absolute path of the working directory (generally "/var/task")
            "ENTRYPOINT[]"--> specifies the absolute path of the entry point to the application
            "COPY requirements.txt" --> copy all dependencies needed by the handler (previously encapsulated using pip freeze > )
            "RUN pip3 install -r requirements.txt" --> Install all mentioned dependencies in requirements.txt
            "COPY handler_file_name ./" --> copy handler code
            "COPY dependencies_file_names ./" --> copy all file dependencies to the handler code
            "CMD ["/workdir/handler_file_name.handler_function_name"]" --> specifies parameters that you want to pass in with ENTRYPOINT
      NB/"workdir" stands for the previously specified WORKDIR
      NB/respect syntax "handler_file_name.handler_function_name"

  -STEP 2 : Build local Docker image :
            "docker build -t name_of_image . "

  -STEP 3 : Authenticate the Docker CLI to your Amazon ECR registry :
            "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com"

  -STEP 4 : (if not already done) Create a repository in Amazon ECR using the create-repository comman :
            "aws ecr create-repository --repository-name name_of_repository --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE"

  -STEP 5 : Tag your image to match your repository name, and deploy the image to Amazon ECR using the docker push command:
            "docker tag  docker_image_name:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/ecr_repository_name:latest"
            "docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/ecr_repository_name:latest"
