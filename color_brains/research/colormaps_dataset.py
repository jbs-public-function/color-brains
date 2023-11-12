import os
import pandas  as pd
import matplotlib as mpl


filepath = os.path.join(os.path.dirname(__file__), "data", "cmap_dataset.csv")
os.makedirs(os.path.dirname(filepath), exist_ok=True)
UNCATEGORIZED_KEY = "Uncategorized"

categorized_cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar'])]


def generate_cmap_data():
    categorized_cmap_names = []
    for cmap_name, cmap in categorized_cmaps:
        categorized_cmap_names.extend(cmap)

    missing_cmap_names = [k for k in mpl.cm._colormaps.keys() if k not in categorized_cmap_names]

    cmap_data = []
    for cmap_category, cmap_names in categorized_cmaps + [(UNCATEGORIZED_KEY, missing_cmap_names)]:
        for cmap_name in cmap_names:
            cmap = mpl.cm._colormaps[cmap_name]
            print(f"{cmap_category} - {cmap_name} - N {cmap.N}")
            data = [(cmap_category, cmap_name, i, *cmap(i)) for i in range(cmap.N)]
            cmap_data.extend(data)
    return cmap_data

def cmap_dataframe(refresh: bool = False):
    if refresh or not os.path.isfile(filepath):
        cmap_df = pd.DataFrame(generate_cmap_data(), columns=["category", "cmap_name", "n", "red", "green", "blue", "alpha"])
        cmap_df.to_csv(filepath)
        return cmap_df
    return pd.read_csv(filepath, index_col=0)
    