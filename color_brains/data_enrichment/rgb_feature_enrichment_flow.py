# python std library
from typing import *

# analysis
import pandas as pd
import numpy as np

# metaflow
from metaflow import FlowSpec, step

# internal modules
from color_brains.data.sequential_data import SequentialData


class RGBFeatureEnrichmentFlow(FlowSpec):
    rgb_columns: List[str] = ["red", "green", "blue"]

    @step
    def start(self):
        print(f"Building RGB Dataset For Modeling")
        sd = SequentialData()
        self.cmap_column_name = sd.CmapNameColumn
        self.target_cols = [self.cmap_column_name] + self.rgb_columns
        self.dataset = sd.dataset
        self.next(self.rgb_features)
    
    @step
    def rgb_features(self):
        self.prev_rgb()
        self.sqrt_rgb()
        self.cbrt_rgb()
        self.rgb_start_of_sequence()
        self.next_rgb()
        self.next(self.end)
    
    @step
    def end(self):
        print("Features Created Dropping NaN Rows")
        self.dataset.dropna(how='any', inplace=True)
        print(f"Dataset has shape of {self.dataset.shape}")
        print(f"Dataset has {self.dataset[self.cmap_column_name].nunique()} Unique Colormaps")
    
    def prev_rgb(self):
        print("Creating Previous RGB Independent Feature")
        prev_rgb = self.dataset[self.target_cols].groupby([self.cmap_column_name]).shift(1).reset_index(drop=True)
        prev_rgb.rename(columns=self.rename_rgb_columns_map("previous"), inplace=True)
        self.dataset = self.dataset.join(prev_rgb)

    def sqrt_rgb(self):
        print("Creating Square Root RGB Independent Feature")
        sqrt_df =  np.sqrt(self.dataset[self.rgb_columns])
        sqrt_df.rename(columns=self.rename_rgb_columns_map("sqrt"), inplace=True)
        self.dataset = self.dataset.join(sqrt_df)

    def cbrt_rgb(self):
        print("Creating Cube Root RGB Independent Feature")
        cbrt_df =  np.cbrt(self.dataset[self.rgb_columns])
        cbrt_df.rename(columns=self.rename_rgb_columns_map("cbrt"), inplace=True)
        self.dataset = self.dataset.join(cbrt_df)

    def rgb_start_of_sequence(self):
        print("Creating Start of Sequence RGB Independent Feature")
        start_rgb = self.dataset[self.target_cols].groupby(self.cmap_column_name).nth(0)
        start_rgb.rename(columns=self.rename_rgb_columns_map("start"), inplace=True)
        self.dataset = pd.merge(self.dataset, start_rgb, how='left', on=[self.cmap_column_name])

    def next_rgb(self):
        print("Creating Next RGB Dependent Feature")
        y_rgb = self.dataset[self.rgb_columns].shift(-1)
        y_rgb.rename(columns=self.rename_rgb_columns_map("next"), inplace=True)
        self.dataset = self.dataset.join(y_rgb)

    def rename_rgb_columns_map(self, tag: str) -> Dict[str, str]:
        return {col: f"{tag}_{col}" for col in self.rgb_columns}


if __name__ == "__main__":
    RGBFeatureEnrichmentFlow()
