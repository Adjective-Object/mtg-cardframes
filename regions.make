
REGION_frame_IN = $(wildcard queries/frame/*.txt)
REGION_frame_OUT = $(patsubst queries/frame/%.txt,composed_regions/frame/%.png,$(REGION_frame_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/frame/%.txt,queries/frame/%/make_rule.make,$(REGION_frame_IN))

composed_regions/frame/%.png: queries/frame/%/make_rule.make

queries/frame/%/make_rule.make: queries/frame/%/ids.txt ./meta/compose_image_makefile_from_ids.py ./gen_makefile.py
	mkdir -p queries/frame/$*
	./meta/compose_image_makefile_from_ids.py --input_path_relative=raw/frame.png --output_prefix_path=composed_regions/frame $* $< > $@

card_cache/%/cleaned/frame.png: card_cache/%/raw/frame.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@ 


# get query result from scryfall and cache 
queries/frame/%/ids.txt: queries/frame/%.txt
	mkdir -p queries/frame/$*
	./query_scryfall.py "$$(cat $<)" > $@

    
card_cache/%/raw/frame.png: card_cache/%/card_image.png card_cache/%/raw
	./crop-card-border.py $* $@

        



REGION_title_line_IN = $(wildcard queries/title_line/*.txt)
REGION_title_line_OUT = $(patsubst queries/title_line/%.txt,composed_regions/title_line/%.png,$(REGION_title_line_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/title_line/%.txt,queries/title_line/%/make_rule.make,$(REGION_title_line_IN))

composed_regions/title_line/%.png: queries/title_line/%/make_rule.make

queries/title_line/%/make_rule.make: queries/title_line/%/ids.txt ./meta/compose_image_makefile_from_ids.py ./gen_makefile.py
	mkdir -p queries/title_line/$*
	./meta/compose_image_makefile_from_ids.py --input_path_relative=cleaned/title_line.png --output_prefix_path=composed_regions/title_line $* $< > $@

card_cache/%/cleaned/title_line.png: card_cache/%/raw/title_line.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@ --l_scale=3 --a_scale=4 --b_scale=4 --diff_threshold=0.8


# get query result from scryfall and cache 
queries/title_line/%/ids.txt: queries/title_line/%.txt
	mkdir -p queries/title_line/$*
	./query_scryfall.py "$$(cat $<)" > $@

    
card_cache/%/raw/title_line.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 637x48+54+56 +repage $@

        



REGION_type_line_IN = $(wildcard queries/type_line/*.txt)
REGION_type_line_OUT = $(patsubst queries/type_line/%.txt,composed_regions/type_line/%.png,$(REGION_type_line_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/type_line/%.txt,queries/type_line/%/make_rule.make,$(REGION_type_line_IN))

composed_regions/type_line/%.png: queries/type_line/%/make_rule.make

queries/type_line/%/make_rule.make: queries/type_line/%/ids.txt ./meta/compose_image_makefile_from_ids.py ./gen_makefile.py
	mkdir -p queries/type_line/$*
	./meta/compose_image_makefile_from_ids.py --input_path_relative=cleaned/type_line.png --output_prefix_path=composed_regions/type_line $* $< > $@

card_cache/%/cleaned/type_line.png: card_cache/%/raw/type_line.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@ --l_scale=3 --a_scale=4 --b_scale=4 --diff_threshold=0.8


# get query result from scryfall and cache 
queries/type_line/%/ids.txt: queries/type_line/%.txt
	mkdir -p queries/type_line/$*
	./query_scryfall.py "$$(cat $<)" > $@

    
card_cache/%/raw/type_line.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 632x45+56+594 +repage $@

        



REGION_text_body_IN = $(wildcard queries/text_body/*.txt)
REGION_text_body_OUT = $(patsubst queries/text_body/%.txt,composed_regions/text_body/%.png,$(REGION_text_body_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/text_body/%.txt,queries/text_body/%/make_rule.make,$(REGION_text_body_IN))

composed_regions/text_body/%.png: queries/text_body/%/make_rule.make

queries/text_body/%/make_rule.make: queries/text_body/%/ids.txt ./meta/compose_image_makefile_from_ids.py ./gen_makefile.py
	mkdir -p queries/text_body/$*
	./meta/compose_image_makefile_from_ids.py --input_path_relative=cleaned/text_body.png --output_prefix_path=composed_regions/text_body $* $< > $@

card_cache/%/cleaned/text_body.png: card_cache/%/raw/text_body.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@ --l_scale=4.5 --a_scale=0.1 --b_scale=0.1 --diff_threshold=0.8


# get query result from scryfall and cache 
queries/text_body/%/ids.txt: queries/text_body/%.txt
	mkdir -p queries/text_body/$*
	./query_scryfall.py "$$(cat $<)" > $@

    
card_cache/%/raw/text_body.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 628x285+58+655 +repage $@

        



REGION_power_box_IN = $(wildcard queries/power_box/*.txt)
REGION_power_box_OUT = $(patsubst queries/power_box/%.txt,composed_regions/power_box/%.png,$(REGION_power_box_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/power_box/%.txt,queries/power_box/%/make_rule.make,$(REGION_power_box_IN))

composed_regions/power_box/%.png: queries/power_box/%/make_rule.make

queries/power_box/%/make_rule.make: queries/power_box/%/ids.txt ./meta/compose_image_makefile_from_ids.py ./gen_makefile.py
	mkdir -p queries/power_box/$*
	./meta/compose_image_makefile_from_ids.py --input_path_relative=cleaned/power_box.png --output_prefix_path=composed_regions/power_box $* $< > $@

card_cache/%/cleaned/power_box.png: card_cache/%/raw/power_box.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@ --l_scale=3 --a_scale=4 --b_scale=4 --diff_threshold=0.8


# get query result from scryfall and cache 
queries/power_box/%/ids.txt: queries/power_box/%.txt
	mkdir -p queries/power_box/$*
	./query_scryfall.py "$$(cat $<)" > $@

    
card_cache/%/raw/power_box.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 104x46+590+930 +repage $@

        
