import numpy as np

# Custom loss functions
def logloss(preds, data):
    y_true = data.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    weight = data.get_weight() if data.get_weight() is not None else 1
    grad = (preds - y_true) * weight
    hess = preds * (1.0 - preds) * weight
    return grad, hess


def logloss_eval(preds, data):
    y_true = data.get_label()
    weight = data.get_weight() if data.get_weight() is not None else np.ones(len(y_true))
    preds = 1.0 / (1.0 + np.exp(-preds))
    sum_loss = -1 * (sum((-(y_true * np.log(preds)) - ((1 - y_true) * np.log(1 - preds))) * weight))

    return "binary_logloss", sum_loss / sum(weight), False
