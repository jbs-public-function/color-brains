# color-brains

Research into the transition schemes of colorbars for maxmimum perceptual differentiation
___
__author__

James Barrett

__email__ 

jbs.public.function@gmail.com

__LinkedIn__


https://www.linkedin.com/in/james-barrett-36075bb3/

---

### Work related to the analysis to colormaps as provided by matplotlib and palettable
[matplotlib colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html#overview)

[palettable color schemes](https://jiffyclub.github.io/palettable/)


### setup

---
**Note**

Developed using Python version 3.11.9

---

create a virual environment
```shell
python -m venv .venv --prompt color-brains
```
___

activate and install requirements
```shell
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

### with venv active
```shell
source .venv/bin/activate
```

___
run model
```shell
make run-model
```
___
see results
```shell
make view-results
```
___
see visualizations
```shell
make view-outputs
```
___
run tests
```shell
make run-tests
```

___
set jupyter kernel for notebooks
```shell
source .venv/bin/activate
python -m ipykernel install --user --name color-brains --display-name color-brains
jupyter notebook
```
