# color-brains

Research into the transition schemes of colorbars for maxmimum perceptual differentiation

__author__

james barrett

__email__ 

jbs.public.function@gmail.com

__LinkedIn__

https://www.linkedin.com/in/james-barrett-36075bb3/

## Categorized colormaps

```python
    cmaps = [('Perceptually Uniform Sequential', [
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
```

[Matplotlib Colormap Documentation](https://matplotlib.org/stable/users/explain/colors/colormaps.html#colormaps)

[Matplotlib Colormap Reference](https://matplotlib.org/stable/gallery/color/colormap_reference.html)

These colormaps are curated from the maintainers of matplotlib and are labeled by type
- Perceptually Uniform Sequential
    - For many applications, a perceptually uniform colormap is the best choice; i.e. a colormap in which equal steps in data are perceived as equal steps in the color space. Researchers have found that the human brain perceives changes in the lightness parameter as changes in the data much better than, for example, changes in hue. Therefore, colormaps which have monotonically increasing lightness through the colormap will be better interpreted by the viewer. Wonderful examples of perceptually uniform colormaps can be found in the Third-party colormaps section as well. 
- Sequential & Sequential (2)
    -  change in lightness and often saturation of color incrementally, often using a single hue; should be used for representing information that has ordering. 
- Diverging
    - change in lightness and possibly saturation of two different colors that meet in the middle at an unsaturated color; should be used when the information being plotted has a critical middle value, such as topography or when the data deviates around zero.
- Cyclic
    - change in lightness of two different colors that meet in the middle and beginning/end at an unsaturated color; should be used for values that wrap around at the endpoints, such as phase angle, wind direction, or time of day. 
- Qualitative
    - often are miscellaneous colors; should be used to represent information which does not have ordering or relationships.
- Miscellaneous
    - Interesting colormaps of no obvious category

__Initial Analysis__

Of the 170 named colormaps provided by matplotlib as
```python
len(mpl.cm._colormaps.keys())
```

only 83 are categorized currently by matplotlib.

Adding all of the *_r colors, the colorbars in reverse to their appropriate categories leave us with all but 4 of the color gradients categorized.

This will us to use reverse data in the mix.

I want to try and categorize the color gradients since I have a labeled category that is somewhat meaningful.
