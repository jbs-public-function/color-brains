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
        self.next(self.model_results)

    @card(id='results')
    @step
    def model_results(self):
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

        self.next(self.visualize_outputs)

    @card(id='visualize_outputs')
    @step
    def visualize_outputs(self):
        output_vis_card = current.card['visualize_outputs']
        output_vis_card.append(Markdown("# Visualizations"))

        rgb_names = ['red', 'green', 'blue']
        dataset = self.latest_run.data.dataset.reset_index(drop=True)
        dataset['category'] = dataset[self.latest_run.data.cmap_column_name].astype('str').str.split('.', expand=True)[0]
        
        dataset_predicted = self.xgb_reg.predict(dataset[self.x_cols])
        dataset_predicted[dataset_predicted > 1] = 1.0
        dataset_predicted[dataset_predicted < 0] = 0.0
        dataset_predicted = dataset[["category", self.latest_run.data.cmap_column_name]].join(pd.DataFrame(dataset_predicted, columns=rgb_names)).reset_index(drop=True)
        for _category in dataset.category.unique():
            output_vis_card.append(Markdown(f"### {_category.title()}"))

            category_set = dataset[dataset.category == _category]
            predicted_category_set = dataset_predicted[dataset_predicted.category == _category]
            for cmap_name in category_set[self.latest_run.data.cmap_column_name].unique():
                cmap_set = category_set[category_set[self.latest_run.data.cmap_column_name] == cmap_name]
                predicted_cmap_set = predicted_category_set[predicted_category_set[self.latest_run.data.cmap_column_name] == cmap_name]
                
                fig = self.plot_colorramps(predicted_cmap_set, cmap_set)
                output_vis_card.append(Image.from_matplotlib(fig))
                plt.close()

        self.next(self.end)

    @step
    def end(self):
        ...

    def plot_colorramps(self, colorramp: pd.DataFrame, comparison_ramp: pd.DataFrame=None) ->plt.figure:
        ramp_name = f"{colorramp.colormap_name.unique()[0].split('.')[-1]}"
        figsize = (8, 1)
        comparison_coloramp_ax = None
        if comparison_ramp is not None:
            fig, axes = plt.subplots(figsize=figsize, nrows=2)
            colorramp_ax, comparison_coloramp_ax = axes
        else:
            fig, colorramp_ax = plt.subplots(figsize=figsize)
        plt.subplots_adjust(hspace=0.0, top=.6, bottom=0.01)

        colorramp_ax.axis(xmin=0, xmax=len(colorramp))
        colorramp_ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        for index, color in enumerate(np.array(colorramp[['red', 'green', 'blue']])):
            colorramp_ax.axvspan(index, index + 1, color=color)
        
        colorramp_ax.set_xlabel(f"Model Output Vs Actual Output {ramp_name.title()}", labelpad=5)
        colorramp_ax.xaxis.set_label_position('top')
        colorramp_ax.spines['bottom'].set_visible(False)
        if not comparison_coloramp_ax:
            return fig

        comparison_coloramp_ax.axis(xmin=0, xmax=len(colorramp))
        comparison_coloramp_ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        comparison_coloramp_ax.spines['top'].set_visible(False)

        for index, color in enumerate(np.array(comparison_ramp[['red', 'green', 'blue']])):
            comparison_coloramp_ax.axvspan(index, index + 1, color=color)
        return fig


if __name__ == "__main__":
    RGBModelFlow()
