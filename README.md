# plotilleresample
*Python module to resample datasets before plotting with Plotille.*

[![CI](https://github.com/carlosplanchon/plotilleresample/actions/workflows/ci.yml/badge.svg)](https://github.com/carlosplanchon/plotilleresample/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/plotilleresample.svg)](https://pypi.org/project/plotilleresample/)
[![Python versions](https://img.shields.io/pypi/pyversions/plotilleresample.svg)](https://pypi.org/project/plotilleresample/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why resample?

Plotille rasterizes to a terminal canvas of braille dots: `width * 2` columns by `height * 4` rows. Feeding it far more points than that costs interpolation time on detail the canvas cannot show. Plotille rasterizes; plotilleresample decides what information deserves to reach the rasterizer:

| Function               | Strategy           | Best for                          |
| ---------------------- | ------------------ | --------------------------------- |
| `resample_plot`        | uniform stride     | smooth lines, cheapest reduction  |
| `resample_plot_minmax` | min/max per bucket | peaks, oscillations, time series  |
| `resample_scatter`     | uniform stride     | large scatter inputs              |

The uniform stride keeps one point every N: fast and predictable, but a narrow peak that falls between two kept points disappears from the plot. `resample_plot_minmax` instead makes one bucket per braille dot column and keeps the minimum and the maximum Y of each bucket, so the envelope of the signal — spikes included — always survives:

```python
X = list(range(10000))
Y = [0.0] * 10000
Y[33] = 1000.0  # a narrow spike

_, y_stride = plotilleresample.resample_plot(X, Y)
_, y_minmax = plotilleresample.resample_plot_minmax(X, Y)

1000.0 in y_stride  # False: the spike vanished
1000.0 in y_minmax  # True: the envelope survives
```

Both plot resamplers keep at most `width * 4` points and `resample_scatter` keeps at most `width * 2 * height`, so plotille only receives what the canvas can actually display.

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
print(" · Plot minmax...")
xm, ym = plotilleresample.resample_plot_minmax(X, Y, w, h)
print(" --- READY ---")

print(f"Len plot.x {len(xp)}")

print(f"Len plot_minmax.x {len(xm)}")

print(f"Len scatter.x {len(xs)}")

input("Plot:")
clear_screen()
print(plotille.plot(xp, yp, w, h))

input("Plot minmax:")
clear_screen()
print(plotille.plot(xm, ym, w, h))

input("Scatter:")
clear_screen()
print(plotille.scatter(xs, ys, w, h))
```
