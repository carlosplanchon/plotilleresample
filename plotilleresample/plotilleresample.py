#!/usr/bin/env python3

from typing import List, Tuple

# This value is used to avoid Nyquist related problems.
plot_multiplier = 4


def resample_plot(
    X,
    Y,
    width: int = 80,
    height: int = 40
        ) -> Tuple[List[int], List[int]]:

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
    X,
    Y,
    width: int = 80,
    height: int = 40
        ) -> Tuple[List[int], List[int]]:

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
