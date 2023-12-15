FROM public.ecr.aws/lambda/python:3.8


WORKDIR /var/task

ENTRYPOINT ["/lambda-entrypoint.sh"]

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY handler.py ./
COPY methods.py ./

CMD ["/var/task/handler.lambda_handler"]
