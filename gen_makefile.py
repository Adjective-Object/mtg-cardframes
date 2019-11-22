import json, re


def tabify(space_str):
    return re.sub(r"^    ", "\t", space_str)


config = json.load(open("config.json"))
rule_blocks = []
for region_name, region in config["regions"].items():
    rule_block = """
REGION_{region_name}_IN = $(wildcard queries/{region_name}/*.txt)
REGION_{region_name}_OUT = $(patsubst queries/{region_name}/%.txt,out/{region_name}/%.png,$(REGION_{region_name}_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/{region_name}/%.txt,queries/{region_name}/%/make_rule.make,$(REGION_{region_name}_IN))

out/{region_name}/%.png: queries/{region_name}/%/make_rule.make

queries/{region_name}/%/make_rule.make: queries/{region_name}/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/{region_name}/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/{region_name} --input_prefix_path={input_prefix}/border_crop.png $* $< > $@

card_cache/%/cleaned/{region_name}.png: card_cache/%/raw/{region_name}.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@


# get query result from scryfall and cache 
queries/{region_name}/%/ids.txt: queries/{region_name}/%.txt
	mkdir -p queries/{region_name}/$*
	./query_scryfall.py "$$(cat $<)" > $@

    """.format(
        region_name=region_name, input_prefix="cleaned" if region["clean"] else "raw",
    )

    if "prep_script" in region:
        rule_block += """
card_cache/%/raw/{region_name}.png: card_cache/%/card_image.png card_cache/%/raw
	{prep_script}

        """.format(
            region_name=region_name, prep_script=region["prep_script"],
        )
    elif "prep_crop" in region:
        rule_block += """
card_cache/%/raw/{region_name}.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop {width}x{height}+{x}+{y} +repage $@

        """.format(
            region_name=region_name,
            x=region["prep_crop"]["x"],
            y=region["prep_crop"]["y"],
            width=region["prep_crop"]["w"],
            height=region["prep_crop"]["h"],
        )

    else:
        raise Exception(
            "neither prep_crop not prep_script defined in region " + region_name
        )

    rule_blocks.append(rule_block)

print(tabify("\n\n\n".join(rule_blocks)))

