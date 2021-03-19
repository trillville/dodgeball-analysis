import pandas as pd
import lightgbm as lgb

from loss_funcs import logloss, logloss_eval
from data_mocker import DataMocker


class FraudModel:
    def __init__(
        self, hyperparam_dict=None, optimization_dict=None, data_path=None, run_hyperopt=False
    ):
        self.run_hyperopt = run_hyperopt
        self.hyperparamaters = hyperparam_dict or {
            "bagging_fraction": 0.8805141557918836,
            "feature_fraction": 0.5233501744144564,
            "learning_rate": 0.091609606997225,
            "max_depth": 29,
            "min_data_in_leaf": 27,
            "min_sum_hessian_in_leaf": 1.300293570679456,
            "num_leaves": 54,
            "subsample": 0.9609092003111154,
            "objective": "binary",
            "metric": "auc",
            "is_unbalance": True,
            "boost_from_average": False,
        }
        self.opt_boundaries = optimization_dict or {
            "learning_rate": (0.01, 1.0),
            "num_leaves": (24, 80),
            "feature_fraction": (0.1, 0.9),
            "bagging_fraction": (0.8, 1),
            "max_depth": (5, 30),
            "min_data_in_leaf": (20, 80),
            "min_sum_hessian_in_leaf": (0, 100),
            "subsample": (0.01, 1.0),
        }
        self.data_path = data_path

    def train(self):
        if self.data_path is not None:
            data = pd.read_csv(self.data_path)
        else:
            data = self.initialize_data()
        model_features = list(set(data.columns) - set(("manual_fraud", "bot_fraud")))
        X = data[model_features]
        y = data["manual_fraud"]
        if self.run_hyperopt:
            model_params = bayes_parameter_opt_lgb(
                X_train.drop(columns=["visitor_profile"]),
                y_train,
                init_round=5,
                opt_round=10,
                n_folds=3,
                random_seed=6,
            )
        else:
            model_params = self.hyperparamaters
        d_train = lgb.Dataset(X.drop(columns=["visitor_profile"]), label=y)
        model = lgb.train(model_params, d_train, 250)
        model.save_model("model.txt")

    def run_hyperopt(self, X, y, init_round=15, opt_round=25, n_folds=3, random_seed=6):
        train_data = lgb.Dataset(data=X, label=y, free_raw_data=False)

        def lgb_eval(
            learning_rate,
            num_leaves,
            feature_fraction,
            bagging_fraction,
            max_depth,
            min_data_in_leaf,
            min_sum_hessian_in_leaf,
            subsample,
        ):
            params = {"application": "binary"}
            params["learning_rate"] = max(min(learning_rate, 1), 0)
            params["num_leaves"] = int(round(num_leaves))
            params["feature_fraction"] = max(min(feature_fraction, 1), 0)
            params["bagging_fraction"] = max(min(bagging_fraction, 1), 0)
            params["max_depth"] = int(round(max_depth))
            params["min_data_in_leaf"] = int(round(min_data_in_leaf))
            params["min_sum_hessian_in_leaf"] = min_sum_hessian_in_leaf
            params["subsample"] = max(min(subsample, 1), 0)

            cv_result = lgb.cv(
                params,
                train_data,
                nfold=n_folds,
                seed=random_seed,
                stratified=True,
                verbose_eval=200,
                fobj=logloss,
                feval=logloss_eval,
            )
            return max(cv_result["auc-mean"])

        lgbBO = BayesianOptimization(lgb_eval, self.opt_boundaries, random_state=200,)

        lgbBO.maximize(init_points=init_round, n_iter=opt_round)

        model_auc = []
        for model in range(len(lgbBO.res)):
            model_auc.append(lgbBO.res[model]["target"])

        opt_params = lgbBO.res[pd.Series(model_auc).idxmax()]["params"]
        opt_params["num_leaves"] = int(round(opt_params[1]["num_leaves"]))
        opt_params["max_depth"] = int(round(opt_params[1]["max_depth"]))
        opt_params["min_data_in_leaf"] = int(round(opt_params[1]["min_data_in_leaf"]))
        opt_params["objective"] = "binary"
        opt_params["metric"] = "auc"
        opt_params["is_unbalance"] = True
        opt_params["boost_from_average"] = False

        return opt_params


if __name__ == "__main__":
    model = FraudModel(data_path="~/dodgeball/dodgeball-analysis/notebooks/sample_data.csv")
    model.train()
