# python std library
from typing import *

# gradient boost library with multivariate regressions
from xgboost import XGBRegressor

# data prep & analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# metaflow
from metaflow import FlowSpec, Flow, step, Parameter, card, current
from metaflow.cards import Markdown, Image, Table

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
        self.y_pred = pd.DataFrame(self.xgb_reg.predict(X_test), columns=self.y_cols)
        self.y_test = y_test
        self.next(self.post_process_model)

    @card(id='results')
    @step
    def post_process_model(self):
        # causes segmentation fault
        # https://github.com/dmlc/xgboost/issues/10686
        # raise Exception(f"{self.xgb_reg.get_booster().get_score(importance_type='weight')}")

        result_card = current.card['results']
        result_card.append(Markdown("## Results"))

        mse = mean_squared_error(self.y_test, self.y_pred, multioutput='uniform_average')
        self.rmse = np.sqrt(mse)
        result_card.append(Markdown(f"### RMSE: {self.rmse}"))

        fig, axes = plt.subplots(3, figsize=(8,11))
        fig.suptitle("Actual RGB Color ~ Predicted RGB Color By Color")
        for idx, col in enumerate(self.y_cols):
            ax = axes[idx]
            color = col.split('next_')[-1]
            ax.plot(self.y_test[col], self.y_pred[col], 'x', color=color, alpha=0.3)
            ax.set_xlabel(f"Actual {color}")
            ax.set_ylabel(f"Predicted {color}")
            ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
            ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        plt.tight_layout()

        result_card.append(Image.from_matplotlib(fig))
        plt.close()

        y_rgb_pred = self.y_pred['next_red'] * self.y_pred['next_green'] *  self.y_pred['next_blue']
        y_rgb_test = self.y_test['next_red'] * self.y_test['next_green'] *  self.y_test['next_blue']

        fig, ax = plt.subplots(figsize=(8,11))

        ax.plot(y_rgb_test, y_rgb_pred, 'x', color='k', alpha=0.3)
        ax.set_xlabel(f"Actual R*G*B")
        ax.set_ylabel(f"Predicted R*G*B")
        ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.set_title('Red * Green * Blue Sequence actual ~ predicted')
        plt.tight_layout()

        result_card.append(Image.from_matplotlib(fig))

        plt.close()

        self.next(self.end)

    @step
    def end(self):
        ...


if __name__ == "__main__":
    RGBModelFlow()
