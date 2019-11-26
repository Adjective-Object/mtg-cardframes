#!/usr/bin/env python3
from cleaning_cellular_automata import cleaning_cellular_automata
from imageio import imread, imwrite
import sys
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create a make rule for composing files"
    )
    parser.add_argument(
        "in_path", metavar="in_path", type=str, nargs=1, help="input path",
    )
    parser.add_argument(
        "out_path", metavar="out_path", type=str, nargs=1, help="output path",
    )
    parser.add_argument("--l_scale", dest="l_scale", default=3, type=float)
    parser.add_argument("--a_scale", dest="a_scale", default=3, type=float)
    parser.add_argument("--b_scale", dest="b_scale", default=3, type=float)
    parser.add_argument(
        "--diff_threshold", dest="diff_threshold", default=0.8, type=float
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    in_img = imread(args.in_path[0])
    out_img = cleaning_cellular_automata(
        in_img,
        L_COLOR_DISTANCE_SCALE=args.l_scale,
        A_COLOR_DISTANCE_SCALE=args.a_scale,
        B_COLOR_DISTANCE_SCALE=args.b_scale,
        NORMALIZED_WEIGHTED_COLOR_DISTANCE_THRESHOLD=args.diff_threshold,
    )
    imwrite(args.out_path[0], out_img)
