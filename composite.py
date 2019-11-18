import numpy as np


def composite(a):
    x = np.maximum(
        np.percentile(a, 80, axis=0, interpolation="nearest"), np.average(a, axis=0)
    )

    return x.astype(np.uint8)
