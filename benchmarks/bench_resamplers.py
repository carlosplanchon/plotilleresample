#!/usr/bin/env python3

"""
Resampling pass alone: pure LTTB vs MinMaxLTTB.

Regenerates the "on the resampling pass alone at 1,000,000 points"
figure quoted in the README. Run from the repository root:
    uv run benchmarks/bench_resamplers.py

Deterministic on purpose: no random data, fixed size, best of 3.
Not part of the CI: timings on shared runners are noise.
"""

import math
import platform
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plotilleresample import resample_plot_lttb
from plotilleresample import resample_plot_minmax_lttb

WIDTH = 80
HEIGHT = 40
SIZE = 1_000_000
REPEATS = 3


def best_of(fn):
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times)


if __name__ == "__main__":
    X = list(range(SIZE))
    Y = [math.sin(i / 100) * 100 for i in range(SIZE)]

    t_lttb = best_of(lambda: resample_plot_lttb(X, Y, WIDTH, HEIGHT))
    t_mmlttb = best_of(lambda: resample_plot_minmax_lttb(X, Y, WIDTH, HEIGHT))

    print(f"Python {platform.python_version()} on {platform.platform()}")
    print(f"Canvas {WIDTH}x{HEIGHT}, {SIZE:,} points, best of {REPEATS} runs.")
    print()
    print(f"resample_plot_lttb:        {t_lttb * 1000:7.0f} ms")
    print(f"resample_plot_minmax_lttb: {t_mmlttb * 1000:7.0f} ms")
    print(f"ratio:                     {t_lttb / t_mmlttb:7.1f}x")
