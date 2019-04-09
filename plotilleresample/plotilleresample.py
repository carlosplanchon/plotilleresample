#!/usr/bin/env python3

from typing import List, Tuple

# This value is used to avoid Nyquist related problems.
plot_multiplier = 4

list_val = List[int]


def resample_plot(
    X: list_val,
    Y: list_val,
    width: int = 80,
    height: int = 40
        ) -> Tuple[List[int], List[int]]:
    """

    :param X: list_val: List of X values.
    :param Y: list_val: List of Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Height of the plot. (Default value = 40)

    """
    if len(X) > width * plot_multiplier:
        step = round(len(X) / width / plot_multiplier)
        print(step)

        if step != 0:
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
    X: list_val,
    Y: list_val,
    width: int = 80,
    height: int = 40
        ) -> Tuple[List[int], List[int]]:
    """

    :param X: list_val: List of X values.
    :param Y: list_val: List of Y values.
    :param width: int: Width of the plot. (Default value = 80)
    :param height: int: Height of the plot. (Default value = 40)

    """
    scatter_multiplier = width * 2 * height
    if len(X) > scatter_multiplier:
        step = round(len(X) / scatter_multiplier)
        print(step)

        if step != 0:
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
