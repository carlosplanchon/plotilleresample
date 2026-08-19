#!/usr/bin/env python3

from collections.abc import Sequence
from math import ceil

# This value is used to avoid Nyquist related problems.
plot_multiplier = 4

# Preselection ratio for resample_plot_minmax_lttb, as in plotly-resampler.
minmax_ratio = 4


def _check_input(
    X: Sequence[float],
    Y: Sequence[float],
    width: int
        ) -> None:
    if len(X) != len(Y):
        raise ValueError(
            "X and Y must have the same number of entries: "
            f"{len(X)} != {len(Y)}"
            )

    if width <= 0:
        raise ValueError(f"width must be positive: {width}")


def _minmax_indices(
    Y: Sequence[float],
    buckets: int
        ) -> list[int]:
    n = len(Y)

    idxs = []
    for b in range(buckets):
        start = b * n // buckets
        stop = (b + 1) * n // buckets

        i_min = i_max = start
        for i in range(start + 1, stop):
            if Y[i] < Y[i_min]:
                i_min = i
            elif Y[i] > Y[i_max]:
                i_max = i

        # In index order so a sorted X stays sorted.
        idxs.extend(sorted({i_min, i_max}))

    return idxs


def _lttb(
    X: Sequence[float],
    Y: Sequence[float],
    n_out: int
        ) -> tuple[list[float], list[float]]:
    n = len(X)

    # First and last point always survive; one point per bucket
    # in between, for exactly n_out points.
    m = n_out - 2

    new_X = [X[0]]
    new_Y = [Y[0]]

    a = 0
    for b in range(m):
        start = 1 + b * (n - 2) // m
        stop = 1 + (b + 1) * (n - 2) // m

        # A is the previously selected point; C is the average of
        # the next bucket (the last point for the final bucket).
        if b + 1 < m:
            next_stop = 1 + (b + 2) * (n - 2) // m
            span = next_stop - stop
            c_x = sum(X[stop:next_stop]) / span
            c_y = sum(Y[stop:next_stop]) / span
        else:
            c_x = X[n - 1]
            c_y = Y[n - 1]

        a_x = X[a]
        a_y = Y[a]

        best = start
        best_area = -1.0
        for i in range(start, stop):
            area = abs(
                (a_x - c_x) * (Y[i] - a_y)
                - (a_x - X[i]) * (c_y - a_y)
                )
            if area > best_area:
                best_area = area
                best = i

        new_X.append(X[best])
        new_Y.append(Y[best])
        a = best

    new_X.append(X[n - 1])
    new_Y.append(Y[n - 1])

    return new_X, new_Y


def resample_plot(
    X: Sequence[float],
    Y: Sequence[float],
    width: int = 80,
    height: int = 40
        ) -> tuple[Sequence[float], Sequence[float]]:
    """

    :param X: Sequence[float]: X values.
    :param Y: Sequence[float]: Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Unused; kept for signature symmetry
        with resample_scatter. (Default value = 40)

    """
    _check_input(X, Y, width)

    if len(X) > width * plot_multiplier:
        step = ceil(len(X) / (width * plot_multiplier))

        X = [
            X[i] for i in range(
                0, len(X), step
                )
            ]
        Y = [
            Y[i] for i in range(
                0, len(Y), step
                )
            ]

    return X, Y


def resample_plot_minmax(
    X: Sequence[float],
    Y: Sequence[float],
    width: int = 80,
    height: int = 40
        ) -> tuple[Sequence[float], Sequence[float]]:
    """
    Like resample_plot, but it keeps the minimum and the maximum
    Y of each bucket, so peaks in high frequency data survive
    the resampling.

    :param X: Sequence[float]: X values.
    :param Y: Sequence[float]: Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Unused; kept for signature symmetry
        with resample_scatter. (Default value = 40)

    """
    _check_input(X, Y, width)

    if len(X) > width * plot_multiplier:
        # One bucket per braille dot column (2 per char); min and max
        # per bucket keep the output at most width * plot_multiplier.
        idxs = _minmax_indices(Y, width * plot_multiplier // 2)

        X = [X[i] for i in idxs]
        Y = [Y[i] for i in idxs]

    return X, Y


def resample_plot_lttb(
    X: Sequence[float],
    Y: Sequence[float],
    width: int = 80,
    height: int = 40
        ) -> tuple[Sequence[float], Sequence[float]]:
    """
    Like resample_plot, but it applies Largest-Triangle-Three-Buckets
    (Steinarsson, 2013): it always keeps the first and the last point
    and picks the most shape-representative point of each bucket, so
    the reduced line looks like the original. Unlike
    resample_plot_minmax it keeps one point per bucket, so one of two
    opposing extremes falling in the same bucket can be dropped.

    :param X: Sequence[float]: X values.
    :param Y: Sequence[float]: Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Unused; kept for signature symmetry
        with resample_scatter. (Default value = 40)

    """
    _check_input(X, Y, width)

    if len(X) > width * plot_multiplier:
        X, Y = _lttb(X, Y, width * plot_multiplier)

    return X, Y


def resample_plot_minmax_lttb(
    X: Sequence[float],
    Y: Sequence[float],
    width: int = 80,
    height: int = 40
        ) -> tuple[Sequence[float], Sequence[float]]:
    """
    Like resample_plot_lttb, but on large inputs it first preselects
    the per bucket extremes with a minmax pass at minmax_ratio finer
    granularity and runs LTTB over those candidates (MinMaxLTTB,
    Van der Donckt et al., 2023; the plotly-resampler default).
    Faster than pure LTTB, with a gap that grows with input size;
    the true extremes are always among the candidates, and the
    output only differs marginally from pure LTTB.

    :param X: Sequence[float]: X values.
    :param Y: Sequence[float]: Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Unused; kept for signature symmetry
        with resample_scatter. (Default value = 40)

    """
    _check_input(X, Y, width)

    n_out = width * plot_multiplier
    if len(X) > n_out:
        if len(X) > n_out * minmax_ratio:
            idxs = _minmax_indices(Y, n_out * minmax_ratio // 2)

            # LTTB anchors on the endpoints, so force them in.
            if idxs[0] != 0:
                idxs.insert(0, 0)
            if idxs[-1] != len(X) - 1:
                idxs.append(len(X) - 1)

            X = [X[i] for i in idxs]
            Y = [Y[i] for i in idxs]

        X, Y = _lttb(X, Y, n_out)

    return X, Y


def resample_scatter(
    X: Sequence[float],
    Y: Sequence[float],
    width: int = 80,
    height: int = 40
        ) -> tuple[Sequence[float], Sequence[float]]:
    """

    :param X: Sequence[float]: X values.
    :param Y: Sequence[float]: Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Height of the plot. (Default value = 40)

    """
    _check_input(X, Y, width)

    if height <= 0:
        raise ValueError(f"height must be positive: {height}")

    scatter_multiplier = width * 2 * height
    if len(X) > scatter_multiplier:
        step = ceil(len(X) / scatter_multiplier)

        X = [
            X[i] for i in range(
                0, len(X), step
                )
            ]
        Y = [
            Y[i] for i in range(
                0, len(Y), step
                )
            ]

    return X, Y
