import os
import tifffile
import regions
from imageio import imread, imsave
from split_by_colors import split_by_colors_with_duals
from prep_inout_dirs import prep_inout_dirs
import json
import numpy as np
import matplotlib.pyplot as plt


class ImLoader:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.name_map = dict([name, None] for name in os.listdir(folder_name))

    def get_image(self, name):
        if name not in self.name_map:
            raise Exception(
                "%s not in self.name_map for imloader %s : %s"
                % (name, self.folder_name, self.name_map)
            )

        if self.name_map[name] is None:
            self.name_map[name] = imread(os.path.join(self.folder_name, name))

        return self.name_map[name]


class Region(ImLoader):
    def __init__(self, folder_name, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        super().__init__(folder_name)

    def get_expanded_image(self, name):
        expanded_image = np.zeros((regions.CARD_H, regions.CARD_W, 4), dtype=np.uint8)
        expanded_image[
            self.y : self.y + self.h, self.x : self.x + self.w, :
        ] = self.get_image(name)
        return expanded_image


def flatten_with_alpha(*images):
    flattened_image = np.zeros(images[0].shape)
    single_channel_shape = (images[0].shape[0], images[0].shape[1], 1)
    for image in images:
        mask = image[:, :, 3].reshape(single_channel_shape)
        flattened_image = flattened_image * ((255 - mask) / 255.0) + image * (
            mask / 255.0
        )

    flattened_image = flattened_image.astype("uint8")

    return flattened_image


if __name__ == "__main__":
    in_dir = "./borders"
    out_dir = "./composed_tiff"
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    data_dirs = [d for d in os.listdir(in_dir) if d.endswith(".png")]

    borders = ImLoader("borders")

    title_lines = Region(
        "title_lines",
        regions.TITLEBOX_X,
        regions.TITLEBOX_Y,
        regions.TITLEBOX_W,
        regions.TITLEBOX_H,
    )

    powerboxes = Region(
        "powerboxes",
        regions.POWERBOX_X,
        regions.POWERBOX_Y,
        regions.POWERBOX_W,
        regions.POWERBOX_H,
    )

    type_lines = Region(
        "type_lines",
        regions.TYPELINE_X,
        regions.TYPELINE_Y,
        regions.TYPELINE_W,
        regions.TYPELINE_H,
    )

    text_bodies = Region(
        "text_bodies",
        regions.TEXTBODY_X,
        regions.TEXTBODY_Y,
        regions.TEXTBODY_W,
        regions.TEXTBODY_H,
    )

    colors = split_by_colors_with_duals(data_dirs)
    merged_or_composed = "composed"
    print("colors", json.dumps(colors, indent=2))
    for color, border_paths in colors.items():
        simple_color = "multi" if "+" in color else color

        print("#################")
        print("##### color!", color)

        simple_color_name = "%s_%s.png" % (simple_color, merged_or_composed)
        title_line = title_lines.get_expanded_image(simple_color_name)
        type_line = type_lines.get_expanded_image(simple_color_name)
        powerbox = powerboxes.get_expanded_image(simple_color_name)

        for border_path in border_paths:
            is_creature = (
                "type:creature" in border_path and not "--type:creature" in border_path
            )

            creaturetype = "creature" if is_creature else "noncreature"
            text_body_name = "%s_%s_%s.png" % (color, creaturetype, merged_or_composed)
            text_body = text_bodies.get_expanded_image(text_body_name)

            print("processing", border_path)
            border = borders.get_image(border_path)
            out_path = os.path.join(out_dir, border_path + ".tiff")
            out_path_flat = os.path.join(out_dir, border_path + "_flat.png")

            # if it is a creature, add
            layers = [
                border,
                title_line,
                type_line,
                text_body,
            ]

            if is_creature:
                layers.append(powerbox)

            with tifffile.TiffWriter(out_path) as tif:
                for layer in layers:
                    tif.save(layer, photometric="rgb")

            flattened_image = flatten_with_alpha(*layers)
            imsave(out_path_flat, flattened_image)
