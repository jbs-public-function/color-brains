# Data
Handle generating rgb inputs for modeling

## Expected Output
pandas DataFrame defined as
```
cmap_name |  red | green | blue
some_cmap |  0.0 | 0.2   | 0.3
some_cmap |  0.12| 0.25  | 0.4
...
some_cmapN|  0.9 | 0.9   | 0.9
```

## Inputs
The inputs are colormap libraries with labeled classes. 

[matplotlib colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html#overview)

[plotly continous color scales](https://plotly.com/python/builtin-colorscales/)

[palettable color schemes](https://jiffyclub.github.io/palettable/)
