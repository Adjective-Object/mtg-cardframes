from diff_cards import create_all_photos_array_from_directory, get_mask
import itertools
import re


def split_by_colors(data_dirs):
    multicoloured = [
        d
        for d in data_dirs
        if re.search(r"(^|[^-]-)(c:(\w|[-:])*)([^-]-c):", d) is not None
    ]

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

    return colors_dict


def split_by_colors_with_duals(data_dirs):
    color_flags = ["c:r", "c:u", "c:g", "c:w", "c:c", "c:b"]
    colors_dict = {}
    for c in color_flags:
        colors_dict[c] = set(d for d in data_dirs if re.search(r"(^|[^-]-)" + c, d))

    for c1, c2 in itertools.combinations(color_flags, 2):
        colors_dict[c1 + "+" + c2] = colors_dict[c1].intersection(colors_dict[c2])

    for c1, c2 in itertools.combinations(color_flags, 2):
        overlap = (
            colors_dict[c1]
            .intersection(colors_dict[c2])
            .union(colors_dict[c2].intersection(colors_dict[c1]))
        )
        for to_remove in overlap:
            colors_dict[c1].remove(to_remove)
            colors_dict[c2].remove(to_remove)

    return dict(([k, list(v)] for k, v in colors_dict.items()))
