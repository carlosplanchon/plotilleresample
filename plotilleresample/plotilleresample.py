#!/usr/bin/env python3

from collections.abc import Sequence
from math import ceil

# This value is used to avoid Nyquist related problems.
plot_multiplier = 4


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
