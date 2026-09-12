#!/usr/bin/env python3

"""
Tests for plotilleresample.

Run with pytest, or directly:
    python tests/test_plotilleresample.py
"""

import math
import sys

from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plotilleresample import resample_plot
from plotilleresample import resample_plot_lttb
from plotilleresample import resample_plot_minmax
from plotilleresample import resample_plot_minmax_lttb
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


def test_lttb_size_exact():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    xl, yl = resample_plot_lttb(X, Y, 80, 40)
    assert len(xl) == len(yl) == 80 * 4


def test_lttb_passthrough_short_input():
    X = [1.0, 2.0]
    Y = [3.0, 4.0]
    assert resample_plot_lttb(X, Y, 80, 40) == (X, Y)
    assert resample_plot_lttb([], [], 80, 40) == ([], [])


def test_lttb_keeps_endpoints_and_sorted_x():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 7) * 100 for i in range(r)]
    xl, yl = resample_plot_lttb(X, Y, 80, 40)
    assert xl[0] == X[0] and yl[0] == Y[0]
    assert xl[-1] == X[-1] and yl[-1] == Y[-1]
    assert all(a <= b for a, b in zip(xl, xl[1:]))


def test_lttb_keeps_a_solitary_spike():
    r = 10000
    X = list(range(r))
    Y = [0.0] * r
    Y[33] = 1000.0
    _, yl = resample_plot_lttb(X, Y, 80, 40)
    assert 1000.0 in yl


def test_lttb_drops_one_of_two_opposing_extremes():
    # The documented trade-off: with a peak and a valley falling in
    # the same bucket, LTTB keeps exactly one shape point while
    # minmax keeps both extremes.
    r = 10000
    X = list(range(r))
    Y = [0.0] * r
    Y[33] = 1000.0
    Y[40] = -1000.0

    _, yl = resample_plot_lttb(X, Y, 80, 40)
    _, ym = resample_plot_minmax(X, Y, 80, 40)

    assert (1000.0 in yl) != (-1000.0 in yl)
    assert 1000.0 in ym and -1000.0 in ym


def test_minmax_lttb_size_endpoints_and_sorted_x():
    r = 10000
    X = list(range(r))
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    xh, yh = resample_plot_minmax_lttb(X, Y, 80, 40)
    assert len(xh) == len(yh) == 80 * 4
    assert xh[0] == X[0] and yh[0] == Y[0]
    assert xh[-1] == X[-1] and yh[-1] == Y[-1]
    assert all(a <= b for a, b in zip(xh, xh[1:]))


def test_minmax_lttb_passthrough_short_input():
    X = [1.0, 2.0]
    Y = [3.0, 4.0]
    assert resample_plot_minmax_lttb(X, Y, 80, 40) == (X, Y)
    assert resample_plot_minmax_lttb([], [], 80, 40) == ([], [])


def test_minmax_lttb_keeps_a_solitary_spike():
    r = 10000
    X = list(range(r))
    Y = [0.0] * r
    Y[33] = 1000.0
    _, yh = resample_plot_minmax_lttb(X, Y, 80, 40)
    assert 1000.0 in yh


def test_minmax_lttb_matches_pure_lttb_below_ratio_threshold():
    # With n_out < len(X) <= n_out * minmax_ratio there is no
    # preselection, so hybrid and pure LTTB must return the same points.
    r = 1000
    X = list(range(r))
    Y = [math.sin(i / 7) * 100 for i in range(r)]
    assert (
        resample_plot_minmax_lttb(X, Y, 80, 40)
        == resample_plot_lttb(X, Y, 80, 40)
        )


def _raises_value_error(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return True
    return False


def test_length_mismatch_raises():
    X = list(range(1000))
    Y = list(range(500))
    for fn in (
        resample_plot, resample_plot_lttb, resample_plot_minmax,
        resample_plot_minmax_lttb, resample_scatter,
            ):
        assert _raises_value_error(fn, X, Y, 80, 40), fn.__name__
    # Fail fast even when the input is below the resampling threshold.
    assert _raises_value_error(resample_plot, [1.0], [1.0, 2.0], 80, 40)


def test_non_positive_width_raises():
    X = list(range(1000))
    for fn in (
        resample_plot, resample_plot_lttb, resample_plot_minmax,
        resample_plot_minmax_lttb, resample_scatter,
            ):
        for w in (0, -5):
            assert _raises_value_error(fn, X, X, w, 40), fn.__name__


def test_non_positive_height_raises_only_in_scatter():
    X = list(range(1000))
    for h in (0, -5):
        assert _raises_value_error(resample_scatter, X, X, 80, h)
        # height is unused in the plot resamplers, so it stays permissive.
        assert not _raises_value_error(resample_plot, X, X, 80, h)
        assert not _raises_value_error(resample_plot_lttb, X, X, 80, h)
        assert not _raises_value_error(resample_plot_minmax, X, X, 80, h)
        assert not _raises_value_error(resample_plot_minmax_lttb, X, X, 80, h)


def test_lttb_measures_triangles_on_x_not_on_the_index():
    # X spaced irregularly on purpose: these points are the ones LTTB picks
    # when the geometry reads X. Using the index instead would move them.
    X = [0.0, 1.0, 2.0, 10.0, 11.0, 12.0, 50.0, 51.0, 52.0, 53.0, 54.0, 100.0]
    Y = [0.0, 5.0, -3.0, 8.0, 1.0, -9.0, 4.0, 7.0, -2.0, 6.0, 0.0, 3.0]
    assert resample_plot_lttb(X, Y, 1, 40) == (
        [0.0, 12.0, 51.0, 100.0], [0.0, -9.0, 7.0, 3.0]
        )
    assert resample_plot_lttb(X, Y, 2, 40) == (
        [0.0, 1.0, 10.0, 12.0, 50.0, 52.0, 53.0, 100.0],
        [0.0, 5.0, 8.0, -9.0, 4.0, -2.0, 6.0, 3.0],
        )
    assert resample_plot_minmax_lttb(X, Y, 1, 40) == (
        [0.0, 12.0, 51.0, 100.0], [0.0, -9.0, 7.0, 3.0]
        )


def test_lttb_accepts_dates_on_the_x_axis():
    r = 5000
    base = datetime(2026, 1, 1)
    X = [base + timedelta(minutes=i) for i in range(r)]
    Y = [math.sin(i / 100) * 100 for i in range(r)]
    Y[1234] = 999.0
    for fn in (resample_plot_lttb, resample_plot_minmax_lttb):
        xl, yl = fn(X, Y, 80, 40)
        assert len(xl) == len(yl) == 80 * 4, fn.__name__
        assert all(isinstance(value, datetime) for value in xl), fn.__name__
        assert xl[0] == X[0] and xl[-1] == X[-1], fn.__name__
        assert 999.0 in yl, fn.__name__
        assert all(a <= b for a, b in zip(xl, xl[1:])), fn.__name__


def test_lttb_accepts_plain_dates_too():
    r = 1000
    X = [date(2026, 1, 1) + timedelta(days=i) for i in range(r)]
    Y = [float(i % 13) for i in range(r)]
    xl, _ = resample_plot_lttb(X, Y, 80, 40)
    assert all(isinstance(value, date) for value in xl)
    assert xl[0] == X[0] and xl[-1] == X[-1]


def test_lttb_rejects_an_x_that_is_neither_number_nor_date():
    Y = [float(i) for i in range(1000)]
    assert _raises_value_error(resample_plot_lttb, ["a"] * 1000, Y, 80, 40)
    assert _raises_value_error(resample_plot_minmax_lttb, ["a"] * 1000, Y, 80, 40)
    # Mixing aware and naive datetimes cannot be subtracted either.
    base = datetime(2026, 1, 1)
    mixed = [base] * 500 + [base.replace(tzinfo=timezone.utc)] * 500
    assert _raises_value_error(resample_plot_lttb, mixed, Y, 80, 40)


if __name__ == "__main__":
    tests = [
        fn for name, fn in sorted(globals().items())
        if name.startswith("test_")
        ]
    for fn in tests:
        fn()
        print(f"{fn.__name__} OK")
    print(f"--- {len(tests)} tests OK ---")
