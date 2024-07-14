# python std library
from unittest import TestCase

# analysis
import pandas as pd

# internal modules
from color_brains.data.color_loaders.loaders import CmapLoaderBase, MplCmapLoader, InvalidShapeError


test_colors_empty = []
test_colors_one = [(1, 2, 3)]

skip_level = 3
set_size = 5
test_colors_many = [(x, x + 1, x + 2) for x in range(0, set_size * skip_level, skip_level)]

test_has_alpha = [(0, 1, 2, 3), (0, 1, 2, 3)]

test_colors_0_1 = pd.DataFrame(
    [
        (0/255., 125/255., 255/255.),
        (25/255., 135/255, 225/255.)
    ],
    columns=['red', 'green', 'blue']
)

test_colors_0_255 = [(0, 125, 255), (25, 135, 225)]


class TestLoaders(TestCase):
    def test_empty_colors(self):
        with self.assertRaises(InvalidShapeError):
            CmapLoaderBase.make_dataframe(test_colors_empty)

    def test_one_colors(self):
        df = CmapLoaderBase.make_dataframe(test_colors_one)
        assert df.shape == (1, 3)

    def test_many_colors(self):
        df = CmapLoaderBase.make_dataframe(test_colors_many)
        assert df.shape == (5, 3)
    
    def test_has_alpha(self):
        df = CmapLoaderBase.make_dataframe(test_has_alpha)
        assert df.shape == (2, 3)
    
    def test_convert_integers(self):
        df = CmapLoaderBase.make_dataframe(test_colors_0_255)
        pd.testing.assert_frame_equal(df, test_colors_0_1)