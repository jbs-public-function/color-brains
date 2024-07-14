# Data
Handle the data engineering of inputs

## Model
sequential model that takes as in an input a tensor of a sequence of colormaps, with a label
(N<sub>cmap_category</sub>, 256, 3)

#### labels
one of 
- sequential
- divergent
- tbd

#### preprocessing
Each row in this dataset would represent a colormap and have a corresponding y-label with its category
A colormap will be padded to 256 (r, g, b) tuples

#### dense neural networks
Try a perceptron for this. 
Smaller dataset, maybe a very simple model will do. 

#### output layer
sigmoid if only two labels else
softmax with shape Y<sub>labels</sub>


## Inputs
The inputs are colormap libraries with labeled classes. 

[matplotlib colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html#overview)

[plotly continous color scales](https://plotly.com/python/builtin-colorscales/)

