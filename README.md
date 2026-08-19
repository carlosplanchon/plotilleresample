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
| `resample_plot_lttb`   | largest triangle per bucket | shape-faithful single line |
| `resample_plot_minmax_lttb` | minmax preselection + LTTB | shape-faithful line, large inputs |
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

`resample_plot_lttb` implements Largest-Triangle-Three-Buckets (Steinarsson, 2013): it always keeps the first and the last point and picks the most shape-representative point of each bucket, giving a single clean line that looks like the original. It keeps one point per bucket, so — unlike min/max — one of two opposing extremes falling in the same bucket can be dropped: shape fidelity instead of envelope guarantee.

`resample_plot_minmax_lttb` is the hybrid (MinMaxLTTB, Van der Donckt et al., 2023; the plotly-resampler default): on large inputs a minmax pass preselects the per bucket extremes and LTTB runs over those candidates only. Visually close to pure LTTB and faster, with a gap that grows with input size — about 1.6x end to end at 100,000 points, and about 4x on the resampling pass alone at 1,000,000 — and the true extremes are always among the candidates.

All four plot resamplers keep at most `width * 4` points and `resample_scatter` keeps at most `width * 2 * height`, so plotille only receives what the canvas can actually display.

## Benchmark

End to end times: building the plot string with plotille alone versus resampling first. Measured with `benchmarks/bench.py` (canvas 80x40, best of 3) on Python 3.14, Linux, Intel Core i5-1135G7:

| Points  | plotille alone | stride + plotille | minmax + plotille | lttb + plotille | mmlttb + plotille |
| ------- | -------------- | ----------------- | ----------------- | --------------- | ----------------- |
| 10,000  | 202 ms         | 23 ms             | 22 ms             | 27 ms           | 24 ms             |
| 100,000 | 1.75 s         | 39 ms             | 52 ms             | 90 ms           | 56 ms             |

Reproduce it from the repository root with:

```
uv run --group bench benchmarks/bench.py
```

## Installation
### Install with UV:
```
uv add plotilleresample
```
### Install with pip:
```
pip install plotilleresample
```

## Usage
```python
import math

import plotille

from plotilleresample import resample_plot_minmax_lttb

r = 100_000
X = list(range(r))
Y = [math.sin(i / 500) * 100 for i in range(r)]

X, Y = resample_plot_minmax_lttb(X, Y, width=80, height=40)
print(plotille.plot(X, Y, width=80, height=40))
```

The full interactive demo, running every resampler on the same dataset, lives in [`examples/demo.py`](examples/demo.py).
