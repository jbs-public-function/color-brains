# python std library
from unittest import TestCase

# analysis
import pandas as pd

# internal modules
from color_brains.data.sequential_data import SequentialData


class TestSequentialData(TestCase):
    def test_sequential_data_obj(self):
        sd = SequentialData()
        
        assert sd._dataset is None
        df = sd.dataset
        assert isinstance(df, pd.DataFrame)
        test_id = id(sd.dataset)
        assert test_id == id(sd.dataset)

    def test_make_dataset(self):
        test_df = SequentialData().dataset
        
        self.assertListEqual(
            list(test_df.columns),
            [SequentialData.CmapNameColumn, 'red', 'green', 'blue']
        )
        
        self.assertTupleEqual(test_df.shape, (63488, 4))
