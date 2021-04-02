FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./
COPY bot_fraud_model.txt /opt/ml/model/

RUN yum -y install libgomp && python3.8 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
