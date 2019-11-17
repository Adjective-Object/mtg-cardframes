import numpy as np


def composite(a):
    return np.maximum(
        np.percentile(a, 90, axis=0, interpolation="nearest"), np.average(a, axis=0)
    )
