# plotilleresample
*Python module to resample datasets before plotting with Plotille.*

[![CI](https://github.com/carlosplanchon/plotilleresample/actions/workflows/ci.yml/badge.svg)](https://github.com/carlosplanchon/plotilleresample/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/plotilleresample.svg)](https://pypi.org/project/plotilleresample/)
[![Python versions](https://img.shields.io/pypi/pyversions/plotilleresample.svg)](https://pypi.org/project/plotilleresample/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation
### Install with UV:
```
uv add plotilleresample
```

## Usage
```
#!/usr/bin/env python3

import plotille

import plotilleresample

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
xs, ys = plotilleresample.resample_scatter(X, Y, w, h)
print(" · Plot...")
xp, yp = plotilleresample.resample_plot(X, Y, w, h)
print(" --- READY ---")

print(f"Len plot.x {len(xp)}")

print(f"Len scatter.x {len(xs)}")

input("Plot:")
clear_screen()
print(plotille.plot(xp, yp, w, h))

input("Scatter:")
clear_screen()
print(plotille.scatter(xs, ys, w, h))
```
