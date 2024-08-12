# pandas
import pandas as pd

# internal packages
from color_brains.data import CmapLoader, MplSequentialColors, PalletableSequentialColors


class SequentialData:
    CmapNameColumn: str = "colormap_name"
    
    def __init__(self):
        self._dataset: None | pd.DataFrame = None
    
    @property
    def dataset(self) -> pd.DataFrame:
        if self._dataset is None:
            df: None | pd.DataFrame = None
            for color_schemes in [MplSequentialColors, PalletableSequentialColors]:
                for colormap_name, cmap in color_schemes.get_colormaps():
                    _df = CmapLoader.make_dataframe(cmap)
                    initial_columns = _df.columns
                    _df[self.CmapNameColumn] = colormap_name 
                    if df is None:
                        df = _df
                        continue
                    df = pd.concat([df, _df])
            df = df[[self.CmapNameColumn] + list(initial_columns)]
            self._dataset = df
                        
        return self._dataset
