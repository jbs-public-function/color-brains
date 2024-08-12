# python std library
from enum import Enum
from typing import List, Iterator, Tuple

# colors
import matplotlib
from palettable import cmocean
from palettable import cartocolors
from palettable import colorbrewer 
from palettable import cubehelix
from palettable import mycarta
from palettable import scientific


class ColorsBaseEnum(Enum):
    @classmethod
    def get_colormap_names(cls) -> Iterator[Tuple[str, str]]:
        for e in cls:
            for color in e.value:
                yield (e.name, color)

    @classmethod
    def get_colormaps(cls) -> Iterator[Tuple[str, str]]:
        for colormap_name, color_name in cls.get_colormap_names():
            mangled_name: str = f"{colormap_name}.{color_name}"
            mpl_cmap = cls.load_colormap(colormap_name, color_name)
            cmap = [mpl_cmap(i) for i in range(256)]
            yield mangled_name, cmap
            
            reversed_name: str = f"{mangled_name}_r"
            cmap.reverse()
            yield reversed_name, cmap
            
        
    @classmethod
    def load_colormap(cls, cmap_name: str) -> matplotlib.colors.LinearSegmentedColormap:
        raise NotImplementedError("Implement In Subclass.")


class MplSequentialColors(ColorsBaseEnum):
    sequential: List[str] = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
    perceptually_uniform_sequential: List[str] = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    sequential_2: List[str] = ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']
    cyclic: List[str] = ['twilight', 'twilight_shifted', 'hsv']

    @classmethod
    def load_colormap(cls, colormap_name: str, cmap_name: str) -> matplotlib.colors.LinearSegmentedColormap:
        return matplotlib.cm._colormaps[cmap_name]


class PalletableSequentialColors(ColorsBaseEnum):
    cartomap: List[str] = ['Burg_7', 'BurgYl_7', 'RedOr_7', 'OrYel_7', 'Peach_7', 'PinkYl_7', 'Mint_7', 'BluGrn_7', 'DarkMint_7', 'Emrld_7', 'agGrnYl_7', 'BluYl_7', 'Teal_7', 'TealGrn_7', 'Purp_7', 'PurpOr_7', 'Sunset_7', 'Magenta_7', 'SunsetDark_7', 'agSunset_7', 'BrwnYl_7']
    colorbrewer: List[str] = ['Blues_9', 'BuGn_9', 'BuPu_9', 'GnBu_9', 'Greens_9', 'Greys_9', 'OrRd_9', 'Oranges_9', 'PuBu_9', 'PuBuGn_9', 'PuRd_9', 'Purples_9', 'RdPu_9', 'Reds_9', 'YlGn_9', 'YlGnBu_9', 'YlOrBr_9', 'YlOrRd_9']
    cmocean: List[str] = ['Algae_256', 'Amp_256', 'Deep_256', 'Dense_256', 'Gray_256', 'Haline_256', 'Ice_256', 'Matter_256', 'Oxy_256', 'Phase_256', 'Solar_256', 'Speed_256', 'Tempo_256', 'Thermal_256', 'Turbid_256']
    cubehelix: List[str] = ['classic_16', 'perceptual_rainbow_16', 'purple_16', 'jim_special_16', 'red_16', 'cubehelix1_16', 'cubehelix2_16', 'cubehelix3_16']
    mycarta: List[str] = ['Cube1_20', 'CubeYF_20', 'LinearL_20']
    scientific: List[str] = ['Devon_256', 'LaJolla_256', 'Bamako_256', 'Davos_256', 'Bilbao_256', 'Nuuk_256', 'Oslo_256', 'GrayC_256', 'Hawaii_256', 'LaPaz_256', 'Tokyo_256', 'Buda_256', 'Acton_256', 'Turku_256', 'Imola_256', 'Batlow_256', 'Oleron_256']

    @classmethod
    def load_colormap(cls, colormap_name: str, cmap_name: str) -> matplotlib.colors.LinearSegmentedColormap:
        color_scheme: None = None
        for e in cls:
            if e.name == colormap_name:        
                color_scheme: "PalletableSequentialColors" = e
                break

        if not color_scheme:
            raise ValueError(f"Invalid Colormap Type '{colormap_name}' Given. Choose One Of {[e.name for e in cls]}")

        if color_scheme == cls.cartomap:
            return cartocolors.sequential.get_map(cmap_name).mpl_colormap

        if color_scheme == cls.cmocean:
            return cmocean.sequential.get_map(cmap_name).mpl_colormap

        if color_scheme == cls.scientific:
            return scientific.sequential.get_map(cmap_name).mpl_colormap

        if color_scheme == cls.cubehelix:
            return cubehelix.get_map(cmap_name).mpl_colormap

        if color_scheme == cls.mycarta:
            return mycarta.get_map(cmap_name).mpl_colormap

        if color_scheme == cls.colorbrewer:
            mapname, number = cmap_name.split('_')
            return colorbrewer.get_map(mapname, 'sequential', number=number).mpl_colormap
