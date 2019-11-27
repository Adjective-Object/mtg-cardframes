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

all_color_flag_combos = [
    "id:%s%s (c:%s and c:%s) -m:{%s/%s}" % (a, b, a, b, a, b)
    for a, b in itertools.combinations(colors, 2)
]

for color_flag in all_color_flag_combos + color_flags:

    color_name = re.sub(r"[()]", "", color_flag)
    color_name = re.sub(r"and", "", color_name)
    color_name = re.sub(r"-m:[^ ]*", "", color_name)
    color_name = re.sub(r"-id:[^ ]*", "", color_name)
    color_name = re.sub("id:", "", color_name)
    color_name = re.sub("c:", "", color_name)
    color_name = re.sub(" ", "", color_name)

    # split on rarity flag for holofoil stamps
    for rarity_flag in ["rarity<rare", "rarity>=rare"]:

        not_flags = ["-" + f for f in color_flags if f not in color_flag]

        for type_name, type_flag in {
            # don't bother fetching new card border legendary enchantment creatures
            # they're too rare
            "nonlegendary_creature": "-t:legend type:creature -type:enchantment",
            "legendary_creature": "t:legend type:creature -type:enchantment",
            "enchantment_creature": "type:creature type:enchantment",
            "land": "type:land",
            "sorceries_instants_and_enchantments": "(type:sorcery or type:instant or type:enchantment) -type:creature",
            "nonvehicle_artifacts": "(type:artifact and -type:vehicle)",
            "vehicles": "type:vehicle",
        }.items():
            # download
            search_term = " ".join(
                not_flags
                + [
                    color_flag,
                    type_flag,
                    rarity_flag,
                    "frame:2015",
                    "-is:split -is:meld -is:transform -is:leveler",
                    "set:dom,grn,m19,m20,mh1,c18,gk",
                ]
            )

            query_name = (
                ("rareplus_" if rarity_flag == "rarity>=rare" else "common_")
                + color_name
                + "_"
                + type_name
            )

            # pre-query scryfall to avoid writing empty queries.
            scryfall_result = query_scryfall(search_term)

            if len(scryfall_result) != 0:
                out_path = os.path.join("queries", "frame", query_name + ".txt")
                print("writing", out_path)
                out = open(out_path, "w")
                out.write(search_term)
                out.close()

