from diff_cards import create_all_photos_array_from_directory, get_mask
import os, re, json, sys
import numpy as np
from imageio import imread, imsave
import matplotlib.pyplot as plt
import random
from regions import TYPELINE_X, TYPELINE_Y, TYPELINE_W, TYPELINE_H
from cleaning_cellular_automata import cleaning_cellular_automata
from composite import composite


def get_all_typelines_array(images_dir_path):
    all_photos_typelines_file = os.path.join(
        images_dir_path, "all_photos_typelines.npy"
    )
    if not os.path.isfile(all_photos_typelines_file):
        print("loading from %s" % all_photos_typelines_file)
        all_photos = create_all_photos_array_from_directory(
            images_dir_path,
            transform=lambda arr: arr[
                TYPELINE_Y : TYPELINE_Y + TYPELINE_H,
                TYPELINE_X : TYPELINE_X + TYPELINE_W,
                :,
            ],
        )
        if all_photos is not None:
            print("saving to for future runs to %s" % all_photos_typelines_file)
            np.save(all_photos_typelines_file, all_photos)
        return all_photos
    else:
        print("loading from %s" % all_photos_typelines_file)
        return np.load(all_photos_typelines_file)


if __name__ == "__main__":

    data_dir = "./data"
    out_dir = "./type_lines"
    data_dirs = os.listdir(data_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    data_dirs = [d for d in data_dirs if os.path.isdir(os.path.join(data_dir, d))]

    multicoloured = [
        d
        for d in data_dirs
        if re.search(r"(^|[^-]-)(c:(\w|[-:])*)([^-]-c):", d) is not None
    ]

    print(
        "multicolored",
        len(multicoloured),
        len(data_dirs),
        [d for d in data_dirs if d in multicoloured],
    )
    print([d for d in data_dirs if d not in multicoloured])

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
        print("collecting %s type lines from" % name, photos_dirs)
        all_typelines = []
        for photo_dir in photos_dirs:
            these_typelines = get_all_typelines_array(os.path.join(data_dir, photo_dir))
            if these_typelines is not None:
                print("these", these_typelines)
                all_typelines.append(these_typelines)

        print("calculating mask for", name, all_typelines)

        all_typelines = np.concatenate(all_typelines, axis=0)

        # for i in range(10):
        #     index = random.randint(0, all_typelines.shape[0])
        #     print(index)
        #     plt.imshow(all_typelines[index].reshape((75, 678, 4)))
        #     plt.show()

        print("calculating mask for", name, all_typelines.shape)
        merged = composite(all_typelines)
        print(merged.shape, merged.min(), merged.max())
        # plt.imshow(mask)
        # plt.show()
        imsave(os.path.join(out_dir, name + "_merged.png"), merged)

        cleaned = cleaning_cellular_automata(merged)
        imsave(os.path.join(out_dir, name + "_cleaned.png"), cleaned)
