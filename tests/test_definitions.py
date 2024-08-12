# python std library
from unittest import TestCase


# internal modules
from color_brains.data.color_loaders.color_definitions import MplSequentialColors, PalletableSequentialColors


class TestColorDefinitions(TestCase):
    def test_get_mpl_colormaps(self):
        cmap_iter = MplSequentialColors.get_colormaps()
        test_color_name, cmap = next(cmap_iter)
        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "sequential.Greys"

        test_color_name, cmap = next(cmap_iter)
        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "sequential.Greys_r"
        
        for test_color_name, cmap in cmap_iter:
            ...

        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "cyclic.hsv_r"
    
    def test_get_palettable_colormaps(self):
        cmap_iter = PalletableSequentialColors.get_colormaps()
        test_color_name, cmap = next(cmap_iter)
        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "cartomap.Burg_7"

        test_color_name, cmap = next(cmap_iter)
        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "cartomap.Burg_7_r"
        
        for test_color_name, cmap in cmap_iter:
            ...

        assert len(cmap) == 256
        assert all([len(c) == 4 for c in cmap])
        assert test_color_name == "scientific.Oleron_256_r"
