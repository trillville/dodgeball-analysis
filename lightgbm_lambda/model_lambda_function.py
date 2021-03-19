import lightgbm as lgb
import numpy as np
import boto3

# model = lgb.load("/opt/manual_fraud_model.pkl")

# bucket = boto3.resource("s3").Bucket("test-lgb-lambda")
# bucket.download_file("model/model.txt", "/tmp/model.txt")
model = lgb.Booster(model_file="manual_fraud_model.txt")

def lambda_handler(event, context):

    event = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    result = model.predict(event)[0]

    return {"StatusCode": 200, "body": f"Prediction: {result}"}
