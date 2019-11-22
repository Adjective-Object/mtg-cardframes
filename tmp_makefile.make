
REGION_power_box_IN = $(wildcard queries/power_box/*.txt)
REGION_power_box_OUT = $(patsubst queries/power_box/%.txt,out/power_box/%.png,$(REGION_power_box_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/power_box/%.txt,queries/power_box/%/make_rule.make,$(IN_power_box))

out/power_box/%.png: queries/power_box/%/make_rule.make

queries/power_box/%/make_rule.make: queries/power_box/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/power_box/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/power_box --input_prefix_path=cleaned/border_crop.png $* $< > $@

card_cache/%/cleaned/power_box.png: card_cache/%/raw/power_box.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

    
card_cache/%/raw/power_box.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 104x46+590+930 +repage $@

        



REGION_title_line_IN = $(wildcard queries/title_line/*.txt)
REGION_title_line_OUT = $(patsubst queries/title_line/%.txt,out/title_line/%.png,$(REGION_title_line_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/title_line/%.txt,queries/title_line/%/make_rule.make,$(IN_title_line))

out/title_line/%.png: queries/title_line/%/make_rule.make

queries/title_line/%/make_rule.make: queries/title_line/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/title_line/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/title_line --input_prefix_path=cleaned/border_crop.png $* $< > $@

card_cache/%/cleaned/title_line.png: card_cache/%/raw/title_line.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

    
card_cache/%/raw/title_line.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 637x48+54+56 +repage $@

        



REGION_frame_IN = $(wildcard queries/frame/*.txt)
REGION_frame_OUT = $(patsubst queries/frame/%.txt,out/frame/%.png,$(REGION_frame_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/frame/%.txt,queries/frame/%/make_rule.make,$(IN_frame))

out/frame/%.png: queries/frame/%/make_rule.make

queries/frame/%/make_rule.make: queries/frame/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/frame/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/frame --input_prefix_path=raw/border_crop.png $* $< > $@

card_cache/%/cleaned/frame.png: card_cache/%/raw/frame.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

    
card_cache/%/raw/frame.png: card_cache/%/card_image.png card_cache/%/raw
	./crop-card-border.py $* $@

        



REGION_type_line_IN = $(wildcard queries/type_line/*.txt)
REGION_type_line_OUT = $(patsubst queries/type_line/%.txt,out/type_line/%.png,$(REGION_type_line_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/type_line/%.txt,queries/type_line/%/make_rule.make,$(IN_type_line))

out/type_line/%.png: queries/type_line/%/make_rule.make

queries/type_line/%/make_rule.make: queries/type_line/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/type_line/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/type_line --input_prefix_path=cleaned/border_crop.png $* $< > $@

card_cache/%/cleaned/type_line.png: card_cache/%/raw/type_line.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

    
card_cache/%/raw/type_line.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 632x45+56+594 +repage $@

        



REGION_text_body_IN = $(wildcard queries/text_body/*.txt)
REGION_text_body_OUT = $(patsubst queries/text_body/%.txt,out/text_body/%.png,$(REGION_text_body_IN))


# include make rules for calculating frame dependencies
include $(patsubst queries/text_body/%.txt,queries/text_body/%/make_rule.make,$(IN_text_body))

out/text_body/%.png: queries/text_body/%/make_rule.make

queries/text_body/%/make_rule.make: queries/text_body/%/ids.txt ./meta/compose_image_makefile_from_ids.py
	mkdir -p queries/text_body/$*
	./meta/compose_image_makefile_from_ids.py --output_prefix_path=out/text_body --input_prefix_path=cleaned/border_crop.png $* $< > $@

card_cache/%/cleaned/text_body.png: card_cache/%/raw/text_body.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

    
card_cache/%/raw/text_body.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop 628x285+58+655 +repage $@

        
