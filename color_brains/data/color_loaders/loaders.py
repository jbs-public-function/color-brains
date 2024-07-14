# python std library
from typing import *

# colors
import matplotlib as mpl

# analysis
import pandas as pd
import numpy as np

# https://forecastegy.com/posts/lightgbm-multi-output-regression-classification-python/


Sequential = [
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']


RGB_Type = Tuple[float | int, float | int, float | int]
RGBA_Type = Tuple[float | int, float | int, float | int, float | int]


class InvalidShapeError(AssertionError):
    ...


class CmapLoaderBase:
    rgb_columns: List[str] = ['red', 'green', 'blue']

    @classmethod
    def make_dataframe(cls, cmap: List[RGB_Type | RGBA_Type]) -> pd.DataFrame:
        df = pd.DataFrame(cmap)
        if df.shape[1] > 3:
            del df[3]
        
        try:
            assert df.shape[0] == 3 or df.shape[1] > 0
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



class MplCmapLoader(CmapLoaderBase):
    @classmethod
    def process_cmap(cls, cmap_name: str) -> pd.DataFrame:
        cmap = mpl.cm._colormaps[cmap_name]
        return cls.make_dataframe([cmap(i) for i in range(cmap.N)])
