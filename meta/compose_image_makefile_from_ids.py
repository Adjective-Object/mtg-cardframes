#!/usr/bin/env python3
import sys
import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create a make rule for composing files"
    )
    parser.add_argument(
        "query_name", metavar="query_name", type=str, nargs=1, help="name of the query",
    )
    parser.add_argument(
        "ids_file_path",
        metavar="id_file_path",
        type=str,
        nargs=1,
        help="path to the ids file",
    )
    parser.add_argument(
        "--output_prefix_path",
        dest="composite_output_prefix_path",
        default="out/frames",
    )
    parser.add_argument(
        "--input_path_relative",
        dest="card_input_relative_path",
        default="raw/border_crop.png",
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    card_ids = open(args.ids_file_path[0], "r").read().strip().split(" ")

    composite_rule = "%s/%s.png: %s\n\t./composite.py $^ $@" % (
        args.composite_output_prefix_path,
        args.query_name[0],
        " ".join(
            [
                "card_cache/%s/%s" % (card_id, args.card_input_relative_path)
                for card_id in card_ids
            ]
        ),
    )

    debug_composite_rule = "%s/%s_debug: %s\n\t%s" % (
        args.composite_output_prefix_path,
        args.query_name[0],
        " ".join(
            [
                "card_cache/%s/%s.png" % (card_id, args.composite_output_prefix_path)
                for card_id in card_ids
            ]
        ),
        "\n\t".join(
            ["rm -f $@", "mkdir $@"]
            + [
                "cp card_cache/%s/%s.png $@/%s"
                % (card_id, args.composite_output_prefix_path, card_id)
                for card_id in card_ids
            ]
        ),
    )

    print("%s\n\n%s" % (composite_rule, debug_composite_rule))
