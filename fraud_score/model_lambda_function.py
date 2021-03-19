import lightgbm as lgb
import numpy as np

model = lgb.load("/opt/manual_fraud_model.pkl")


def lambda_handler(event, context):

    event = np.array([[1,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0]])
    result = model.predict(event)

    return result
