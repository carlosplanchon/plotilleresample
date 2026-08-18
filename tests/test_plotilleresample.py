#!/usr/bin/env python3

"""
Tests for plotilleresample.

Run with pytest, or directly:
    python tests/test_plotilleresample.py
"""

import math
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plotilleresample import resample_plot
from plotilleresample import resample_plot_minmax
from plotilleresample import resample_scatter


def test_resample_plot_size():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    xp, yp = resample_plot(X, Y, 80, 40)
    assert len(xp) == len(yp)
    assert len(xp) <= 80 * 4


def test_resample_scatter_size():
    for r in (9000, 10000):
        xs, ys = resample_scatter(list(range(r)), list(range(r)), 80, 40)
        assert len(xs) == len(ys)
        assert len(xs) <= 80 * 2 * 40


def test_minmax_passthrough_short_input():
    X = [1.0, 2.0]
    Y = [3.0, 4.0]
    assert resample_plot_minmax(X, Y, 80, 40) == (X, Y)
    assert resample_plot_minmax([], [], 80, 40) == ([], [])


def test_minmax_size_within_target():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    xm, ym = resample_plot_minmax(X, Y, 80, 40)
    assert len(xm) == len(ym)
    assert len(xm) <= 80 * 4


def test_minmax_x_stays_sorted():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 7) * 100 for i in range(r)]
    xm, _ = resample_plot_minmax(X, Y, 80, 40)
    assert all(a <= b for a, b in zip(xm, xm[1:]))


def test_minmax_preserves_envelope():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    _, ym = resample_plot_minmax(X, Y, 80, 40)
    assert max(ym) == max(Y)
    assert min(ym) == min(Y)


def test_spike_survives_minmax_but_not_stride():
    # A flat signal with one spike placed off the stride grid:
    # resample_plot with 10000 points and width 80 keeps indices
    # 0, 32, 64, ... (step = ceil(10000 / 320) = 32), so the spike
    # at index 33 is dropped. The minmax bucket containing index 33
    # keeps it as the bucket maximum.
    r = 10000
    X = list(range(r))
    Y = [0.0] * r
    Y[33] = 1000.0

    _, y_stride = resample_plot(X, Y, 80, 40)
    _, y_minmax = resample_plot_minmax(X, Y, 80, 40)

    assert 1000.0 not in y_stride
    assert 1000.0 in y_minmax


def test_minmax_constant_data_dedups():
    # min and max coincide in every bucket -> one point per bucket.
    r = 10000
    X = list(range(r))
    Y = [5.0] * r
    xm, ym = resample_plot_minmax(X, Y, 80, 40)
    assert len(xm) == 80 * 4 // 2
    assert set(ym) == {5.0}


def _raises_value_error(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


def test_length_mismatch_raises():
    X = list(range(1000))
    Y = list(range(500))
    for fn in (resample_plot, resample_plot_minmax, resample_scatter):
        assert _raises_value_error(fn, X, Y, 80, 40), fn.__name__
    # Fail fast even when the input is below the resampling threshold.
    assert _raises_value_error(resample_plot, [1.0], [1.0, 2.0], 80, 40)


def test_non_positive_width_raises():
    X = list(range(1000))
    for fn in (resample_plot, resample_plot_minmax, resample_scatter):
        for w in (0, -5):
            assert _raises_value_error(fn, X, X, w, 40), fn.__name__


def test_non_positive_height_raises_only_in_scatter():
    X = list(range(1000))
    for h in (0, -5):
        assert _raises_value_error(resample_scatter, X, X, 80, h)
        # height is unused in the plot resamplers, so it stays permissive.
        assert not _raises_value_error(resample_plot, X, X, 80, h)
        assert not _raises_value_error(resample_plot_minmax, X, X, 80, h)


if __name__ == "__main__":
    tests = [
        fn for name, fn in sorted(globals().items())
        if name.startswith("test_")
        ]
    for fn in tests:
        fn()
        print(f"{fn.__name__} OK")
    print(f"--- {len(tests)} tests OK ---")
