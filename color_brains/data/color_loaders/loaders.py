# python std library
from typing import *

# analysis
import pandas as pd
import numpy as np

# https://forecastegy.com/posts/lightgbm-multi-output-regression-classification-python/
RGB_Type = Tuple[float | int, float | int, float | int]
RGBA_Type = Tuple[float | int, float | int, float | int, float | int]


class InvalidShapeError(AssertionError):
    ...


class CmapLoader:
    rgb_columns: List[str] = ['red', 'green', 'blue']

    @classmethod
    def make_dataframe(cls, cmap: List[RGB_Type | RGBA_Type]) -> pd.DataFrame:
        df = pd.DataFrame(cmap)
        if df.shape[1] > 3:
            del df[3]
        
        try:
            # there are rows in the dataframe
            # there are only 3 columns
            assert df.shape[0] > 0 and df.shape[1] == 3
        except AssertionError:
            raise InvalidShapeError(f"Invalid Dataframe of shape {df.shape}")
        
        df.columns = cls.rgb_columns
        return cls.scale_integers(df)

    @classmethod
    def convert_integers(cls, df: pd.DataFrame) -> pd.DataFrame:
        for rgb_column in cls.rgb_columns:
            df[rgb_column] /= 255.0
        return df

    @classmethod
    def scale_integers(cls, df: pd.DataFrame) -> pd.DataFrame:
        if np.any([(np.any(df[rgb_column] > 1)) for rgb_column in cls.rgb_columns]):
            return cls.convert_integers(df)
        return df
