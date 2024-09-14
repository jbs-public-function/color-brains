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
        self.target_cols = [self.cmap_column_name] + self.get_rgb_columns()
        self.dataset = sd.dataset
        self.next(self.rgb_features)
    
    @step
    def rgb_features(self):
        self.dataset = self.prev_rgb(self.dataset, self.target_cols, self.cmap_column_name)
        # self.dataset = self.sqrt_rgb(self.dataset)
        # self.dataset = self.cbrt_rgb(self.dataset)
        self.dataset = self.rgb_start_of_sequence(self.dataset, self.target_cols, self.cmap_column_name)
        self.dataset = self.rgb_end_of_sequence(self.dataset, self.target_cols, self.cmap_column_name)
        self.dataset = self.next_rgb(self.dataset)
        self.next(self.end)
    
    @step
    def end(self):
        print("Features Created Dropping NaN Rows")
        self.dataset.dropna(how='any', inplace=True)
        print(f"Dataset has shape of {self.dataset.shape}")
        print(f"Dataset has {self.dataset[self.cmap_column_name].nunique()} Unique Colormaps")
    
    @classmethod
    def prev_rgb(cls, dataset: pd.DataFrame, target_cols: List[str], cmap_column_name: str) -> pd.DataFrame:
        print("Creating Previous RGB Independent Feature")
        prev_rgb = dataset[target_cols].groupby([cmap_column_name]).shift(1).reset_index(drop=True)
        prev_rgb.rename(columns=cls.rename_rgb_columns_map("previous"), inplace=True)
        return dataset.join(prev_rgb)

    @classmethod
    def sqrt_rgb(cls, dataset: pd.DataFrame) -> pd.DataFrame:
        print("Creating Square Root RGB Independent Feature")
        sqrt_df = np.sqrt(dataset[cls.get_rgb_columns()])
        sqrt_df.rename(columns=cls.rename_rgb_columns_map("sqrt"), inplace=True)
        return dataset.join(sqrt_df)

    @classmethod
    def cbrt_rgb(cls, dataset: pd.DataFrame) -> pd.DataFrame:
        print("Creating Cube Root RGB Independent Feature")
        cbrt_df =  np.cbrt(dataset[cls.get_rgb_columns()])
        cbrt_df.rename(columns=cls.rename_rgb_columns_map("cbrt"), inplace=True)
        return dataset.join(cbrt_df)

    @classmethod
    def rgb_start_of_sequence(cls, dataset: pd.DataFrame, target_cols: List[str], cmap_column_name: str) -> pd.DataFrame:
        print("Creating Start of Sequence RGB Independent Feature")
        start_rgb = dataset[target_cols].groupby(cmap_column_name).nth(0)
        start_rgb.rename(columns=cls.rename_rgb_columns_map("start"), inplace=True)
        return pd.merge(dataset, start_rgb, how='left', on=[cmap_column_name])

    @classmethod
    def rgb_end_of_sequence(cls, dataset: pd.DataFrame, target_cols: List[str], cmap_column_name: str) -> pd.DataFrame:
        print("Creating End of Sequence RGB Independent Feature")
        start_rgb = dataset[target_cols].groupby(cmap_column_name).nth(-1)
        start_rgb.rename(columns=cls.rename_rgb_columns_map("end"), inplace=True)
        return pd.merge(dataset, start_rgb, how='left', on=[cmap_column_name])

    @classmethod
    def next_rgb(cls, dataset: pd.DataFrame) -> pd.DataFrame:
        print("Creating Next RGB Dependent Feature")
        y_rgb = dataset[cls.get_rgb_columns()].shift(-1)
        y_rgb.rename(columns=cls.rename_rgb_columns_map("next"), inplace=True)
        return dataset.join(y_rgb)
    
    @classmethod
    def get_rgb_columns(cls) -> List[str]:
        return ['red', 'green', 'blue']

    @classmethod
    def rename_rgb_columns_map(cls, tag: str) -> Dict[str, str]:
        return {col: f"{tag}_{col}" for col in cls.get_rgb_columns()}


if __name__ == "__main__":
    RGBFeatureEnrichmentFlow()
