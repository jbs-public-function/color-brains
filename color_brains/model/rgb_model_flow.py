# python std library
from typing import *

# gradient boost library with multivariate regressions
from xgboost import XGBRegressor

# data prep & analysis
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# metaflow
from metaflow import FlowSpec, Flow, step, Parameter

# internal modules
from color_brains.model.utils import run_rgb_feature_metaflow, DATA_ENRICHMENT_METAFLOW_FILEPATH, DATA_ENRICHMENT_METAFLOW_NAME


class RGBModelFlow(FlowSpec):
    dependendent_variables: List[str] = ['next_red', 'next_green', 'next_blue']
    rgb_feature_file = Parameter("rgb_feature_file", default=DATA_ENRICHMENT_METAFLOW_FILEPATH)
    rgb_feature_flowname = Parameter("rgb_feature_flowname", default=DATA_ENRICHMENT_METAFLOW_NAME)
    random_state = Parameter("random_state", type=int, default=42)

    @step
    def start(self):
        print(f"Loading dataset from latest successful run of {self.rgb_feature_flowname}")
        try:
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run
        except Exception:
            print(f'No Previously Successful Run of {self.rgb_feature_flowname} Found...\nRunning')
            run_rgb_feature_metaflow(DATA_ENRICHMENT_METAFLOW_FILEPATH)
            latest_run = Flow(self.rgb_feature_flowname).latest_successful_run

        self.latest_run = latest_run
        self.next(self.run_model)

    @step
    def run_model(self):
        dataset = self.latest_run.data.dataset

        self.y_cols = [f"next_{rgb_val}" for rgb_val in self.latest_run.data.rgb_columns]
        self.x_cols = [c for c in dataset if c != self.latest_run.data.cmap_column_name and c not in self.y_cols]

        X_train, X_test, y_train, y_test = train_test_split(
            dataset[self.x_cols],
            dataset[self.y_cols],
            test_size=0.2,
            random_state=self.random_state
        )
        self.xgb_reg = XGBRegressor(multi_strategy='multi_output_tree')
        self.xgb_reg.fit(X_train, y_train)
        self.xgb_pred = pd.DataFrame(self.xgb_reg.predict(X_test), columns=self.y_cols)

        self.next(self.post_process_model)

    @step
    def post_process_model(self):
        # causes segmentation fault
        # https://github.com/dmlc/xgboost/issues/10686
        # raise Exception(f"{self.xgb_reg.get_booster().get_score(importance_type='weight')}")
        self.next(self.end)

    @step
    def end(self):
        ...


if __name__ == "__main__":
    RGBModelFlow()
