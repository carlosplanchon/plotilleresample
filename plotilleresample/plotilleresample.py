#!/usr/bin/env python3

from collections.abc import Sequence
from math import ceil

# This value is used to avoid Nyquist related problems.
plot_multiplier = 4


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
        n = len(X)

        # One bucket per braille dot column (2 per char); min and max
        # per bucket keep the output at most width * plot_multiplier.
        buckets = width * plot_multiplier // 2

        new_X = []
        new_Y = []

        for b in range(buckets):
            start = b * n // buckets
            stop = (b + 1) * n // buckets

            i_min = i_max = start
            for i in range(start + 1, stop):
                if Y[i] < Y[i_min]:
                    i_min = i
                elif Y[i] > Y[i_max]:
                    i_max = i

            # Emit in index order so a sorted X stays sorted.
            for i in sorted({i_min, i_max}):
                new_X.append(X[i])
                new_Y.append(Y[i])

        X, Y = new_X, new_Y

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
