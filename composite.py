#!/usr/bin/env python3
import numpy as np
import sys, os
from skimage import color
from imageio import imread, imwrite
import pathlib


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


BLOCKSIZE = 300

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <input_file_names> <output_file_name>")
        exit(1)

    impaths = sys.argv[1:-1]
    first_img = imread(impaths[0])
    imshape = first_img.shape

    out = np.zeros(imshape, dtype=np.uint8)
    for y in range(0, imshape[0], BLOCKSIZE):
        y_next = min(imshape[0], y + BLOCKSIZE)
        for x in range(0, imshape[1], BLOCKSIZE):
            x_next = min(imshape[1], x + BLOCKSIZE)
            dest_shape = (1, y_next - y, x_next - x, 4)
            image_blocks = [first_img[y:y_next, x:x_next, :].reshape(dest_shape)]
            print("reading blocks at x[%s:%s],y[%s:%s]" % (x, x_next, y, y_next))
            for f in impaths[1:]:
                image_blocks.append(
                    imread(f)[y:y_next, x:x_next, :].reshape(dest_shape)
                )

            image_blocks_np_arr = np.concatenate(image_blocks, axis=0)
            out[y:y_next, x:x_next] = composite(image_blocks_np_arr)

    out_path = sys.argv[-1]
    pathlib.Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
    imwrite(out_path, out)
