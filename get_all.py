import subprocess
import itertools
import json
import re

colors = [
    'r',
    'u',
    'g',
    'w',
    'b',
    'c',
]

color_flags = [
    'c:%s' % c for c in colors
]

all_color_flag_combos = ['c:%s c:%s -m:{%s/%s}' %(a, b, a, b) for a,b in itertools.combinations(colors, 2)]

print(all_color_flag_combos)

for color_flag in color_flags + all_color_flag_combos:

    # split on rarity flag for holofoil stamps
    for rarity_flag in [
        "rarity<rare",
        "rarity>=rare"
    ]:

        not_flags = ['-' + f for f in color_flags if f not in color_flag]

        for type_flag in [
            # don't bother fetching new card border legendary enchantment creatures
            # they're too rare
            '-t:legend type:creature -type:enchantment',
            't:legend type:creature -type:enchantment',
            'type:creature type:enchantment',
            "type:land",
            "type:sorcery type:instant type:enchantment -type:creature"
        ]:
            # download
            search_term = ' '.join(
                    not_flags + [color_flag, type_flag, rarity_flag, 'frame:2015', 'set:dom,grn,m19,m20,mh1,c18,gk']
            ) 
            print(search_term)
            proc = subprocess.Popen([
                'node', './list-cards.js', search_term
            ], stdout=subprocess.PIPE)
            output, _err = proc.communicate()
            print(output)
            output_file_path = re.search(r" ([^ ]+\.json)", str(output)).groups()[0]
            print("output_file_path", output_file_path)
            if output_file_path:
                print("downloading!")
                subprocess.call([
                    "./download-cards.sh", output_file_path
                ])
