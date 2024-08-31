# Feature Engineering

Engineering additional features of the rgb colormaps dataset

## Independent Variables
```python
# current rgb
current_red, current_green, current_blue,

# starting rgb
previous_red, previous_green, previous_blue

# squareroots of current rgb 
current_red**2, current_green**2, current_blue**2,

# cuberoots of current rgb
current_red**3, current_green**3, current_blue**3,

# cos of current rgb
cos(current_red), cos(current_green), cos(current_blue),

# rgb of start of sequence
red_start, green_start, blue_start,

# rgb of end of sequence
red_end, green_end, blue_end,

# function of all three colors
f(current_red, current_green, current_blue),

# functions of two colors distance to third 
f(-current_red, current_green, current_blue), 
f(current_red, -current_green, current_blue). 
f(current_red, current_green, -current_blue),

# functions of two colors
f(current_red, current_green), 
f(current_red, current_blue), 
f(current_green, current_blue)
```

## Dependent Variables
```python
# next rgb from current rgb
next_red, next_green, next_blue
```