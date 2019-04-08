# plotilleresample
*Python3 module to resample datasets before plotting with Plotille.*

# Rationale
I want to optimize plot and scatter function of plotille.

## Installation
### Install with pip
```
pip3 install -U servusresample
```

## Usage
```
#!/usr/bin/env python3

import plotille

import plotilledimreduction

import math

from shutil import get_terminal_size

from vtclear import clear_screen

import numpy as np


w = get_terminal_size().columns - 20
h = get_terminal_size().lines - 7

r = 10000
res = np.random.normal(size=r)

# Here I'm testing stuffs with histograms.
# input("Histogram:")
# print(plotille.histogram(res, bins=w*2, width=w, height=h))

X = [i for i in range(r)]
Y = [math.sin(i / 100) * 100 for i in range(r)]

print(" · Scatter...")
xs, ys = plotilledimreduction.dim_reduction_scatter(X, Y, w, h)
print(" · Plot...")
xp, yp = plotilledimreduction.dim_reduction_plot(X, Y, w, h)
print(" --- READY ---")

print(f"Len plot.x {len(xp)}")

print(f"Len scatter.x {len(xs)}")

input("Plot:")
clear_screen()
print(plotille.plot(xp, yp, w, h))

input("Scatter:")
clear_screen()
print(plotille.plot(xs, ys, w, h))
```
