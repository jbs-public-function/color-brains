import os
from itertools import chain
from typing import Dict, List, Tuple

import pandas  as pd
import numpy as np

import matplotlib as mpl
from matplotlib.pyplot import imshow

from skimage.transform import resize


datapath = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(datapath, exist_ok=True)

colors_dir = os.path.join(
   datapath,
   "color_images",
)

color_cmaps_dir = os.path.join(
   colors_dir,
   "cmaps"
)

os.makedirs(color_cmaps_dir, exist_ok=True)


UNCATEGORIZED_KEY = "Uncategorized"


def get_categorized_cmaps() -> Dict[str, List[str]]:
   return {
      'Perceptually Uniform Sequential': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'], 
      'Sequential': ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'], 
      'Sequential (2)': ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'], 
      'Diverging': ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'], 
      'Cyclic': ['twilight', 'twilight_shifted', 'hsv'], 
      'Qualitative': ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'], 
      'Miscellaneous': ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']
   }


def assign_reverse_variables(categorized_cmaps: Dict[str, List[str]]) -> None:
   missing_cmap_names = [k for k in mpl.cm._colormaps.keys() if k not in chain(*categorized_cmaps.values())]

   for _, cmap_names in categorized_cmaps.items():
      for cmap_name in cmap_names:
         if f"{cmap_name}_r" in missing_cmap_names:
               missing_cmap_names.pop(missing_cmap_names.index(f"{cmap_name}_r"))
               cmap_names.append(f"{cmap_name}_r")

   categorized_cmaps[UNCATEGORIZED_KEY] = missing_cmap_names


def get_cmap_data() -> Dict[str, List[str]]:
   categorized_cmaps = get_categorized_cmaps()
   assign_reverse_variables(categorized_cmaps)
   return categorized_cmaps


def generate_cmap_data() -> List[Tuple[str, str, int, float, float, float, float]]:
   categorized_cmaps = get_cmap_data()
   cmap_data = []
   for cmap_category, cmap_names in categorized_cmaps.items():
      print(f"{cmap_category}")
      for cmap_name in cmap_names:
         cmap = mpl.cm._colormaps[cmap_name]
         print(f"{cmap_name} - N {cmap.N}")
         data = [(cmap_category, cmap_name, i, *cmap(i)) for i in range(cmap.N)]
         cmap_data.extend(data)
   return cmap_data


def cmap_dataframe(convert_data_to_int: bool = False, refresh: bool = False) -> pd.DataFrame:
    if convert_data_to_int:
       filepath = os.path.join(datapath, "integer_cmap_dataset.csv")
    else:
       filepath = os.path.join(datapath, "scaled_cmap_dataset.csv")

    if refresh or not os.path.isfile(filepath):
        cmap_df = pd.DataFrame(generate_cmap_data(), columns=["category", "cmap_name", "n", "red", "green", "blue", "alpha"])
        if convert_data_to_int:
         for column in ["red", "green", "blue", "alpha"]:
               cmap_df[column] = (cmap_df[column] * 255).astype(int)
        cmap_df.to_csv(filepath)
        return cmap_df
    return pd.read_csv(filepath, index_col=0)


def generate_cmap_tensors(refresh: bool = False) -> None:
   for cmap_category, cmap_names in get_cmap_data().items():
      print(f"Writing Images for - {cmap_category}")

      img_dir = os.path.join(color_cmaps_dir, cmap_category)
      os.makedirs(img_dir, exist_ok=True)
      for cmap_name in cmap_names:
         png_filename = os.path.join(img_dir, f"{cmap_name}.png")

         if  not os.path.isfile(png_filename) or refresh:
            colormap = mpl.cm._colormaps[cmap_name]
            cmap = [colormap(i) for i in range(colormap.N)]
            img_array = np.array([cmap])
            if colormap.N != 256:
               img_array = resize(img_array, (1, 256))
            
            ax = imshow(img_array, aspect='auto')
            ax.write_png(png_filename)


def generate_cmap_probabilities(
      exclude: List[str] = ["Qualitative", "Uncategorized"]
   ) -> Tuple[np.array, np.array, np.array]:
   red_proba, green_proba, blue_proba = np.zeros((256,256)), np.zeros((256,256)), np.zeros((256,256))
   df = cmap_dataframe(convert_data_to_int=True)

   for category in df[~df.category.isin(exclude)].category.unique():
      for cmap_name in df[df.category == category].cmap_name.unique():
         rgb = df[(df.category == category) &  (df.cmap_name == cmap_name)]
         first_value = True
         for _, _rgb in rgb.iterrows():
               if first_value:
                  current_red = _rgb['red']
                  current_green = _rgb['green']
                  current_blue = _rgb['blue']
                  first_value = False
                  continue

               next_red = _rgb['red']
               next_green = _rgb['green']
               next_blue = _rgb['blue']

               red_proba[current_red][next_red] += 1
               green_proba[current_green][next_green] += 1
               blue_proba[current_blue][next_blue] += 1

               current_red = next_red
               current_green = next_green
               current_blue = next_blue

   return (
      calculate_rowwise_probability(red_proba),
      calculate_rowwise_probability(green_proba),
      calculate_rowwise_probability(blue_proba)
   )


def calculate_rowwise_probability(arr: np.array) -> np.array:
   """
      [
         [1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]
      ]
      =>
      [
         [1/6, 1/3, 1/2],
         [4/15, 1/3, 2/5],
         [7/24, 1/3, 9/24]
      ]

      s.t. all rows sum to 1.0
   """
   return (arr.T / arr.sum(axis=1)).T
