from diff_cards import create_all_photos_array_from_directory, get_mask
import os, re, json, sys
import numpy as np
from imageio import imread, imsave
import matplotlib.pyplot as plt
import random
from composite import composite
from regions import TEXTBODY_X, TEXTBODY_Y, TEXTBODY_W, TEXTBODY_H
from split_by_colors import split_by_colors_with_duals
from cleaning_cellular_automata import cleaning_cellular_automata


def get_all_text_bodies_array(images_dir_path):
    all_photos_text_bodies_file = os.path.join(
        images_dir_path, "all_photos_text_bodies.npy"
    )
    if not os.path.isfile(all_photos_text_bodies_file):
        print("loading from %s" % all_photos_text_bodies_file)
        all_photos = create_all_photos_array_from_directory(
            images_dir_path,
            transform=lambda arr: arr[
                TEXTBODY_Y : TEXTBODY_Y + TEXTBODY_H,
                TEXTBODY_X : TEXTBODY_X + TEXTBODY_W,
                :,
            ],
        )
        if all_photos is not None:
            print("saving to for future runs to %s" % all_photos_text_bodies_file)
            np.save(all_photos_text_bodies_file, all_photos)
        return all_photos
    else:
        print("loading from %s" % all_photos_text_bodies_file)
        return np.load(all_photos_text_bodies_file)


if __name__ == "__main__":

    data_dir = "./data"
    out_dir = "./text_bodies"
    data_dirs = os.listdir(data_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    data_dirs = [d for d in data_dirs if os.path.isdir(os.path.join(data_dir, d))]

    colors_dict = split_by_colors_with_duals(data_dirs)

    for name, photos_dirs_sets in colors_dict.items():
        for is_creature in [True, False]:
            photos_dirs = [
                p
                for p in photos_dirs_sets
                if is_creature == ("type:creature" in p and "--type:creature" not in p)
            ]

            print("collecting %s bodies from" % name, photos_dirs)
            all_text_bodies = []
            for photo_dir in photos_dirs:
                these_text_bodies = get_all_text_bodies_array(
                    os.path.join(data_dir, photo_dir)
                )
                if these_text_bodies is not None:
                    all_text_bodies.append(these_text_bodies)

            # print("calculating mask for", name, all_text_bodies)

            if len(all_text_bodies) == 0:
                print(
                    "!!!WARNING!! no bodies for is_creature=%s, name=%s"
                    % (is_creature, name)
                )
                print(photos_dirs)
                continue

            all_text_bodies = np.concatenate(all_text_bodies, axis=0)

            out_tmp_subdir = os.path.join(out_dir, name)
            if not os.path.isdir(out_tmp_subdir):
                os.mkdir(out_tmp_subdir)
            for i in range(0, len(all_text_bodies)):
                print("cleaing input %s / %s" % (i + 1, len(all_text_bodies) + 1))
                cleaned = cleaning_cellular_automata(
                    all_text_bodies[i].reshape((all_text_bodies.shape[1:]))
                )
                imsave(os.path.join(out_tmp_subdir, "cleaned_%s.png" % i), cleaned)
                all_text_bodies[i] = cleaned

            # for i in range(10):
            #     index = random.randint(0, all_text_bodies.shape[0])
            #     print(index)
            #     plt.imshow(all_text_bodies[index].reshape((75, 678, 4)))
            #     plt.show()

            print("calculating mask for", name, all_text_bodies.shape)
            merged = composite(all_text_bodies)
            print(merged.shape, merged.min(), merged.max())
            # plt.imshow(mask)
            # plt.show()
            imsave(
                os.path.join(
                    out_dir,
                    name
                    + ("_creature" if is_creature else "_noncreature")
                    + "_cleaned_merged.png",
                ),
                merged,
            )
