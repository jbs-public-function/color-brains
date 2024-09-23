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
        self.dataset = self.rgb_start_of_sequence(self.dataset, self.target_cols, self.cmap_column_name)
        self.dataset = self.rgb_end_of_sequence(self.dataset, self.target_cols, self.cmap_column_name)
        self.dataset = self.calculate_cos_theta(self.dataset, "start")
        self.dataset = self.calculate_cos_theta(self.dataset, "previous")
        self.dataset = self.calculate_cos_theta(self.dataset, "end")
        self.dataset = self.next_rgb(self.dataset)
        self.next(self.end)
    
    @step
    def end(self):
        print("Features Created Dropping NaN Rows")
        self.dataset.dropna(how='any', inplace=True)
        print(f"Dataset has shape of {self.dataset.shape}")
        print(f"Dataset has {self.dataset[self.cmap_column_name].nunique()} Unique Colormaps")
        self.independent_variables = [c for c in self.dataset.columns if c.startswith('next')]
        self.dependent_variables = [c for c in self.dataset.columns if not c not in self.independent_variables]
    
    @classmethod
    def prev_rgb(cls, dataset: pd.DataFrame, target_cols: List[str], cmap_column_name: str) -> pd.DataFrame:
        print("Creating Previous RGB Independent Feature")
        prev_rgb = dataset[target_cols].groupby([cmap_column_name]).shift(1).reset_index(drop=True)
        prev_rgb.rename(columns=cls.rename_rgb_columns_map("previous"), inplace=True)
        return dataset.join(prev_rgb)

    @classmethod
    def calculate_cos_theta(cls, dataset: pd.DataFrame, label: str) -> pd.DataFrame:
        labeled_columns = cls.rename_rgb_columns_map(label)
        rgb, labeled_rgb = labeled_columns.keys(), labeled_columns.values()
        print(rgb, labeled_rgb)
        cos_theta_label = f"cos_theta_{label}"

        print(f"Calculating Cos Theta for {cos_theta_label} RGB Independent Feature")

        dot_product = np.einsum('ij,ij->i', dataset[rgb].values, dataset[labeled_rgb].values)
        magnitude_rgb = np.linalg.norm(dataset[rgb], axis=1)
        magnitude_label_rgb = np.linalg.norm(dataset[labeled_rgb], axis=1)

        cos_theta = pd.DataFrame(dot_product / (magnitude_rgb * magnitude_label_rgb), columns=[cos_theta_label])
        return dataset.join(cos_theta)

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
"""

# Define two vectors
v1 = np.array([3, 4])
v2 = np.array([6, 8])

# Calculate the dot product
dot_product = np.dot(v1, v2)

# Calculate the magnitudes of the vectors
magnitude_v1 = np.linalg.norm(v1)
magnitude_v2 = np.linalg.norm(v2)

# Calculate the cosine of the angle
cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

# Calculate the angle in radians and then convert to degrees
angle_radians = np.arccos(cos_theta)
angle_degrees = np.degrees(angle_radians)
"""

if __name__ == "__main__":
    RGBFeatureEnrichmentFlow()
