import lightgbm as lgb
import pandas as pd

model = lgb.Booster(model_file="/opt/ml/model/bot_fraud_model.txt")


def lambda_handler(event, context):

    data_df = pd.DataFrame(event, index=[0])

    result = model.predict(data_df)[0]

    return {
        "statusCode": 200,
        "body": {"prediction_type": "bot_fraud", "fruad_probability": 100 * round(result, 4)},
    }
