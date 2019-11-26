#!/usr/bin/env python3
from diff_cards import remove_card_art, remove_collectors_type
import json, os, sys
import config
from imageio import imread, imwrite


def crop_card_border(card_id):
    json_path = os.path.join(config.CARD_DATA_DIR, card_id, config.CARD_JSON_NAME)
    png_path = os.path.join(config.CARD_DATA_DIR, card_id, config.CARD_PNG_NAME)

    card_json = json.load(open(json_path))

    is_legend = "legend" in card_json["type_line"].lower()
    is_powerless = "creature" not in card_json["type_line"].lower()

    card_img = imread(png_path)
    remove_card_art(card_img, is_legend)
    remove_collectors_type(card_img, is_powerless)

    return card_img


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: %s <card_id> <output_img_path>" % sys.argv[0])
        exit(1)

    card_id = sys.argv[1]
    out_path = sys.argv[2]

    card = crop_card_border(card_id)
    imwrite(out_path, card)
