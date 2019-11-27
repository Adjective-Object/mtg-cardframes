import subprocess
import itertools
import json
import re
import os
from query_scryfall import query_scryfall

colors = [
    "r",
    "u",
    "g",
    "w",
    "b",
    "c",
]

color_flags = ["id:%s" % c for c in colors]
not_color_flags = ["c:%s" % c for c in colors]

all_color_flag_combos = [
    "(c:%s and c:%s) id:%s%s" % (a, b, a, b)
    for a, b in itertools.combinations(colors, 2)
]

for color_flag in all_color_flag_combos + color_flags:

    color_name = re.sub(r"[()]", "", color_flag)
    color_name = re.sub(r"-id:[^ ]*", "", color_name)
    color_name = re.sub(r"-m:[^ ]*", "", color_name)
    color_name = re.sub(r"and", "", color_name)
    color_name = re.sub("id:", "", color_name)
    color_name = re.sub("c:", "", color_name)
    color_name = re.sub(" ", "", color_name)

    # split on rarity flag for holofoil stamps
    for watermark_name, watermark_flag in {
        "no_watermark": "-has:watermark",
        # ravnica guilds
        "azorius": "wm:azorius",
        "dimir": "wm:dimir",
        "rakdos": "wm:rakdos",
        "gruul": "wm:gruul",
        "selesnya": "wm:selesnya",
        "orzhov": "wm:orzhov",
        "golgari": "wm:golgari",
        "simic": "wm:simic",
        "izzet": "wm:izzet",
        "boros": "wm:boros",
        # khans block
        "Abzan": "wm:Abzan",
        "Jeskai": "wm:Jeskai",
        "Sultai": "wm:Sultai",
        "Mardu": "wm:Mardu",
        "Temur": "wm:Temur",
        # mirrodin beseiged
        "phyrexian": "wm:phyrexian",
        "mirrian": "wm:mirrian",
        # misc
        "planeswalker": "wm:planeswalker",
    }.items():

        not_flags = ["-" + f for f in color_flags if f not in color_flag]

        # download
        search_term = " ".join(
            [color_flag]
            + not_flags
            + [
                watermark_flag,
                "frame:2015",
                "-is:split -is:meld -is:transform -is:leveler",
                "set:dom,grn,m19,m20,mh1,c18,gk",
            ]
        )

        query_name = color_name + "_" + watermark_name

        # pre-query scryfall to avoid writing empty queries.
        scryfall_result = query_scryfall(search_term)

        if len(scryfall_result) != 0:
            out_path = os.path.join("queries", "text_body", query_name + ".txt")
            print("writing", out_path)
            out = open(out_path, "w")
            out.write(search_term)
            out.close()

