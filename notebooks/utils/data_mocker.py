import pandas as pd
import numpy as np
import json


class DataMocker:
    def __init__(
        self,
        num_samples=1000,
        params_loc="/Users/tillman/dodgeball/dodgeball-analysis/notebooks/sample_parameters.json",
    ):
        self.num_samples = num_samples
        with open(params_loc, "r") as fp:
            self.sample_params = json.load(fp)
        self.attributes = list(self.sample_params["normal_visitor"]["attributes"])
        self.labels = ["manual_fraud", "bot_fraud", "visitor_profile"]
        self.profile_distribution = {
            key: self.sample_params[key]["traffic_pct"] for key in self.sample_params
        }

    def generate_label(self, label: str, key: str):
        """Generate a label vector for a particular visitor profile"""
        if label == "visitor_profile":
            key_data = [key] * int(self.sample_params[key]["traffic_pct"] * self.num_samples)
        else:
            key_data = np.random.binomial(
                1,
                self.sample_params[key][label],
                int(self.sample_params[key]["traffic_pct"] * self.num_samples),
            )
        return key_data

    def generate_attribute(self, attribute, key):
        """Generate an attribute vector for a particular visitor profile"""
        if self.sample_params[key]["attributes"][attribute] is not None:
            key_data = np.random.binomial(
                1,
                self.sample_params[key]["attributes"][attribute],
                int(self.sample_params[key]["traffic_pct"] * self.num_samples),
            )
        else:
            key_data = int(self.sample_params[key]["traffic_pct"] * self.num_samples) * [None]
        return key_data

    def generate_data(self):
        """Generate a sample dataset based on the rules/probabilities encoded into the self.sample_params json file"""
        sample_df = pd.DataFrame()
        # Generate labels
        for label in self.labels:
            col_data = []
            for key in self.sample_params.keys():
                col_data.extend(self.generate_label(label, key))
            sample_df[label] = col_data

        # Generate attributes
        for attribute in self.attributes:
            col_data = []
            for key in self.sample_params.keys():
                col_data.extend(self.generate_attribute(attribute, key))
            sample_df[attribute] = col_data

        return sample_df

    def add_nulls(self, df: pd.DataFrame, frac: float):
        """Add noise to a DataFrame by replacing random cells with missing values"""

        inds = np.random.randint(
            low=0, high=len(df), size=int(len(df) * len(self.attributes) * frac)
        )
        cols = np.random.randint(low=0, high=len(self.attributes), size=len(inds))
        x = df[self.attributes].astype(object).to_numpy()
        x[inds, cols] = None
        df[self.attributes] = x
        return df

    def flip_booleans(self, df: pd.DataFrame, frac: float):
        """Add noise to a DataFrame by flipping random the True/False values of random cells"""
        inds = np.random.randint(range(len(df)), int(len(df) * frac), replace=True)
        cols = np.random.randint(range(len(self.attributes)), len(inds), replace=True)
        x = df[self.attributes].astype(object).to_numpy()
        x[inds, cols] = (x[inds, cols] + 1) % 2
        df[self.attributes] = x
        return df
