#!/usr/bin/env python3

"""
End to end benchmark: plotille alone vs resampling first.

Run from the repository root:
    uv run --group bench benchmarks/bench.py

Deterministic on purpose: no random data, fixed sizes, best of 3.
Not part of the CI: timings on shared runners are noise.
"""

import math
import platform
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotille

from plotilleresample import resample_plot
from plotilleresample import resample_plot_lttb
from plotilleresample import resample_plot_minmax
from plotilleresample import resample_plot_minmax_lttb

WIDTH = 80
HEIGHT = 40
SIZES = (10_000, 100_000)
REPEATS = 3


def best_of(fn):
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times)


def fmt(seconds):
    if seconds >= 1:
        return f"{seconds:.2f} s"
    return f"{seconds * 1000:.0f} ms"


def bench(r):
    X = list(range(r))
    Y = [math.sin(i / 500) * 100 for i in range(r)]

    def raw():
        plotille.plot(X, Y, WIDTH, HEIGHT)

    def stride():
        xs, ys = resample_plot(X, Y, WIDTH, HEIGHT)
        plotille.plot(xs, ys, WIDTH, HEIGHT)

    def minmax():
        xm, ym = resample_plot_minmax(X, Y, WIDTH, HEIGHT)
        plotille.plot(xm, ym, WIDTH, HEIGHT)

    def lttb():
        xl, yl = resample_plot_lttb(X, Y, WIDTH, HEIGHT)
        plotille.plot(xl, yl, WIDTH, HEIGHT)

    def mmlttb():
        xh, yh = resample_plot_minmax_lttb(X, Y, WIDTH, HEIGHT)
        plotille.plot(xh, yh, WIDTH, HEIGHT)

    return (
        best_of(raw), best_of(stride), best_of(minmax),
        best_of(lttb), best_of(mmlttb),
        )


if __name__ == "__main__":
    print(f"Python {platform.python_version()} on {platform.platform()}")
    print(f"Canvas {WIDTH}x{HEIGHT}, best of {REPEATS} runs.")
    print()
    header = (
        f"{'points':>10} | {'plotille alone':>15} | "
        f"{'stride + plotille':>18} | {'minmax + plotille':>18} | "
        f"{'lttb + plotille':>16} | {'mmlttb + plotille':>18}"
        )
    print(header)
    print("-" * len(header))
    for r in SIZES:
        t_raw, t_stride, t_minmax, t_lttb, t_mmlttb = bench(r)
        print(
            f"{r:>10,} | {fmt(t_raw):>15} | "
            f"{fmt(t_stride):>18} | {fmt(t_minmax):>18} | "
            f"{fmt(t_lttb):>16} | {fmt(t_mmlttb):>18}"
            )
