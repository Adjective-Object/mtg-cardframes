from diff_cards import create_all_photos_array_from_directory, get_mask
import os, re, json, sys
import numpy as np
from imageio import imread, imsave
import matplotlib.pyplot as plt
import scipy.stats
import random
from skimage import color
from composite import composite
from regions import POWERBOX_X, POWERBOX_Y, POWERBOX_W, POWERBOX_H
from cleaning_cellular_automata import cleaning_cellular_automata


def get_power_boxes_array(images_dir_path):
    all_photos_typelines_file = os.path.join(images_dir_path, "all_photos_powers.npy")
    if not os.path.isfile(all_photos_typelines_file):
        print("loading from %s" % all_photos_typelines_file)
        all_photos = create_all_photos_array_from_directory(
            images_dir_path,
            transform=lambda arr: arr[
                POWERBOX_Y : POWERBOX_Y + POWERBOX_H,
                POWERBOX_X : POWERBOX_X + POWERBOX_W,
                :,
            ],
        )
        if all_photos is not None:
            print(all_photos.shape)
            print("saving to for future runs to %s" % all_photos_typelines_file)
            np.save(all_photos_typelines_file, all_photos)
        return all_photos
    else:
        print("loading from %s" % all_photos_typelines_file)
        return np.load(all_photos_typelines_file)


if __name__ == "__main__":

    data_dir = "./data"
    out_dir = "./powerboxes"
    data_dirs = os.listdir(data_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    data_dirs = [
        d
        for d in data_dirs
        if os.path.isdir(os.path.join(data_dir, d))
        and "-type:creature" in d
        and "--type:creature" not in d
    ]

    multicoloured = [
        d
        for d in data_dirs
        if re.search(r"(^|[^-]-)(c:(\w|[-:])*)([^-]-c):", d) is not None
    ]

    # print("multicolored", len(multicoloured), len(data_dirs), [d for d in data_dirs if d in multicoloured])
    # print([d for d in data_dirs if d not in multicoloured])

    color_flags = ["c:r", "c:u", "c:g", "c:w", "c:c", "c:b", "c:c"]

    colors_dict = {
        "multi": multicoloured,
    }
    for c in color_flags:
        colors_dict[c] = [
            d
            for d in data_dirs
            if d not in multicoloured and re.search(r"(^|[^-]-)" + c, d)
        ]

    print("colors_dict", json.dumps(colors_dict, indent=2))

    for name, photos_dirs in colors_dict.items():
        print("collecting %s power boxes from" % name, photos_dirs)
        all_power_boxes = []
        for photo_dir in photos_dirs:
            these_power_boxes = get_power_boxes_array(os.path.join(data_dir, photo_dir))
            if these_power_boxes is not None:
                print("these", these_power_boxes.shape)
                all_power_boxes.append(these_power_boxes)

        # print("calculating mask for", name, all_power_boxes)

        all_power_boxes = np.concatenate(all_power_boxes, axis=0)

        out_tmp_subdir = os.path.join(out_dir, name)
        if not os.path.isdir(out_tmp_subdir):
            os.mkdir(out_tmp_subdir)
        for i in range(0, len(all_power_boxes)):
            print("cleaing input %s / %s" % (i + 1, len(all_power_boxes) + 1))
            cleaned = cleaning_cellular_automata(
                all_power_boxes[i].reshape((all_power_boxes.shape[1:]))
            )
            imsave(os.path.join(out_tmp_subdir, "cleaned_%s.png" % i), cleaned)
            all_power_boxes[i] = cleaned

        # for i in range(10):
        #     index = random.randint(0, all_power_boxes.shape[0])
        #     print(index)
        #     plt.imshow(all_power_boxes[index].reshape((75, 678, 4)))
        #     plt.show()

        print("calculating mask for", name, all_power_boxes.shape)

        # original_shape = all_power_boxes.shape
        # colors_arr = all_power_boxes.reshape(
        #     original_shape[0],
        #     original_shape[1] * original_shape[2],
        #     4
        # )

        # mode = np.apply_along_axis(lambda x: color.rgb2lab(color.rgba2rgb(x))[0].argmax(), axis=0, arr=colors_arr)
        # mode, counts = scipy.stats.mode(
        #     axis = 0
        # )

        # print('mode', mode.shape)

        # merged = mode.reshape(
        #     original_shape[1:]
        # )

        merged = composite(all_power_boxes)

        print(merged.shape, merged.min(), merged.max())
        # plt.imshow(mask)
        # plt.show()
        imsave(os.path.join(out_dir, name + "_cleaned_merged.png"), merged)
        # cleaned = cleaning_cellular_automata(merged)
        # imsave(os.path.join(out_dir, name + "_cleaned.png"), cleaned)
