import sys
import os
import numpy as np
from imageio import imread, imsave
from skimage import color
import matplotlib.pyplot as plt
from composite import composite


def print_usage():
    print(
        """
    Usage: %s <directory_path>
    """
        % (sys.argv[0])
    )


def create_all_photos_array_from_directory(directory_path, limit=None, transform=None):
    file_names = sorted(os.listdir(directory_path))
    if limit is not None:
        print(limit)
        file_names = file_names[0:limit]

    images = []
    for f in file_names:
        if not f.endswith(".png"):
            continue
        im_path = os.path.join(directory_path, f)
        print("reading", im_path)
        image = imread(im_path)
        print("read as", image.dtype)
        if transform:
            image = transform(image)
        images.append(image)

    if len(images) == 0:
        print("no images, returning None")
        return None
    print("collecting into single numpy array")
    return np.array(images)


def get_all_photos_array(images_dir_path):
    all_photos_file = os.path.join(images_dir_path, "all_photos.npy")
    if not os.path.isfile(all_photos_file):
        print("loading from %s" % all_photos_file)
        all_photos = create_all_photos_array_from_directory(images_dir_path, limit=30)
        if all_photos is not None:
            print("saving to for future runs to %s" % all_photos_file)
            all_photos = all_photos
            np.save(all_photos_file, all_photos)
        return all_photos
    else:
        print("loading from %s" % all_photos_file)
        return np.load(all_photos_file)


def get_mask(all_photos):
    av_photos = np.average(all_photos, axis=0)

    all_photos_l = color.rgb2lab((all_photos)[:, :, :, 0:3])[:, :, :, 0]
    del all_photos

    all_photos_l_avg = np.average(all_photos_l, axis=0)

    diff_with_avg = all_photos_l - all_photos_l_avg

    mask = np.sum(np.power(diff_with_avg, 2), axis=0)
    mask = mask - mask.min()
    mask = mask / mask.max()
    mask = 1 - mask

    return mask


def percentile_mask(directory_path, percentile):
    file_names = sorted(os.listdir(directory_path))[0:20]
    int_perecentile = int(len(file_names) * percentile)
    print(int_perecentile)
    composite_image = np.zeros((1040, 745, 4))
    composite_image_lab = np.zeros((1040, 745))
    counts = np.zeros((1040, 745), dtype=np.int)

    FILE_LIMIT = 50
    if len(file_names) > FILE_LIMIT:
        print(
            "%s files is too many images. Only loading first %s at once"
            % (len(file_names), FILE_LIMIT)
        )
        file_names = file_names[0:50]

    for [i, f] in enumerate(file_names):
        if not f.endswith(".png"):
            continue

        im_path = os.path.join(directory_path, f)
        print("reading", "%002d/%002s" % (i + 1, len(file_names)), im_path)
        next_image = imread(im_path)
        next_image_lab = color.rgb2lab(color.rgba2rgb(next_image))[:, :, 0]

        bump_mask = np.logical_and(
            (composite_image_lab < next_image_lab), (counts < int_perecentile)
        )
        bump_mask_reshaped = bump_mask.reshape(
            (bump_mask.shape[0], bump_mask.shape[1], 1)
        )

        # print(bump_mask.shape, bump_mask.min(), bump_mask.max())
        # plt.imshow(bump_mask * 1.0)
        # plt.show()

        composite_image_lab = next_image_lab * bump_mask + composite_image_lab * (
            1 - bump_mask
        )
        composite_image = next_image * bump_mask_reshaped + composite_image * (
            1 - bump_mask_reshaped
        )

        plt.imshow(composite_image_lab, cmap="gray")
        plt.show()

        counts += bump_mask
        # print(counts.shape, counts.min(), counts.max(), np.average(counts))

    return composite_image


def remove_card_art(card, is_legend=False):

    print(card.shape)

    x = 58
    y = 117
    w = 629
    h = 461

    if is_legend:
        x -= 1
        y -= 2
        w += 2
        h += 3

    card[y : y + h, x : x + w, 3] = 0.1
    card[y + 1 : y + h - 2, x + 1 : x + w - 2, 3] = 0


def remove_collectors_type(card, is_powerless=False):

    # sampling black from here
    x = 37
    y = 1013
    w = 682
    h = 14

    t = card[y : y + h, x : x + w]
    # plt.imshow(t)
    # plt.show()
    mean_color = np.mean(t.reshape((w * h, 4)), axis=0)

    print("mean color", mean_color)

    # assignign black to here
    x = 37
    y = 990
    w = 682
    h = 24
    card[y : y + h, x : x + w, :] = mean_color
    x = 37
    y = 970
    w = 120
    h = 22
    card[y : y + h, x : x + w, :] = mean_color

    if is_powerless:
        x = 439
        y = 969
        w = 266
        h = 39
        card[y : y + h, x : x + w, :] = mean_color


def process_photos_dir(photos_dir, out_file):
    all_photos = get_all_photos_array(photos_dir)
    if all_photos is None:
        return
    print("all_photos", all_photos.dtype, all_photos.min(), all_photos.max())

    out_img = composite(all_photos)

    del all_photos
    remove_card_art(out_img, is_legend=("--t:legend:" not in photos_dir))
    remove_collectors_type(
        out_img,
        is_powerless=(
            "--type:creature" in photos_dir or "type:creature" not in photos_dir
        ),
    )

    print("out_img", out_img.dtype, out_img.min(), out_img.max())

    imsave(out_file, out_img)


def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    process_photos_dir(sys.argv[0], "single-run.png")


if __name__ == "__main__":
    main()
