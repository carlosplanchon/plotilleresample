#!/usr/bin/env python3

# Interactive demo running every resampler on the same dataset.
# From the repository root:
#   uv run --group bench --with numpy --with vtclear examples/demo.py

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
print(" · Plot lttb...")
xl, yl = plotilleresample.resample_plot_lttb(X, Y, w, h)
print(" · Plot minmax lttb...")
xmml, ymml = plotilleresample.resample_plot_minmax_lttb(X, Y, w, h)
print(" --- READY ---")

print(f"Len plot.x {len(xp)}")

print(f"Len plot_minmax.x {len(xm)}")

print(f"Len plot_lttb.x {len(xl)}")

print(f"Len plot_minmax_lttb.x {len(xmml)}")

print(f"Len scatter.x {len(xs)}")

input("Plot:")
clear_screen()
print(plotille.plot(xp, yp, w, h))

input("Plot minmax:")
clear_screen()
print(plotille.plot(xm, ym, w, h))

input("Plot lttb:")
clear_screen()
print(plotille.plot(xl, yl, w, h))

input("Plot minmax lttb:")
clear_screen()
print(plotille.plot(xmml, ymml, w, h))

input("Scatter:")
clear_screen()
print(plotille.scatter(xs, ys, w, h))
