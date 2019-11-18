import numpy as np
from skimage import color


def composite(a):
    # print(a.shape)
    lab_a = color.rgb2lab(color.rgba2rgb(a))
    x = (
        color.lab2rgb(
            np.maximum(
                np.percentile(lab_a, 50, axis=0, interpolation="nearest"),
                np.average(lab_a, axis=0),
            )
        )
        * 255
    ).astype(np.uint8)

    # print (x.shape, x.min(), x.max(), x.dtype)
    m = np.mean(a[:, :, :, 3], axis=0).reshape(x.shape[0], x.shape[1], 1)
    # print(m.shape, m.min(), m.max())
    with_alpha = np.concatenate((x, m), axis=2)

    return with_alpha.astype(np.uint8)
