
TEXTBOX_X = 54
TEXTBOX_Y = 56
TEXTBOX_W = 637
TEXTBOX_H = 48

TYPELINE_X = 56
TYPELINE_Y = 594
TYPELINE_W = 632
TYPELINE_H = 45

TEXTBODY_X = 58
TEXTBODY_Y = 655
TEXTBODY_W = 628
TEXTBODY_H = 285

POWERBOX_X = 590
POWERBOX_Y = 930
POWERBOX_W = 104
POWERBOX_H = 46

IN_FRAMES = $(wildcard queries/frames/*.txt)
OUT_FRAMES = $(patsubst queries/frames/%.txt,out/frames/%.png,$(IN_FRAMES))

IN_TEXT_BOXES = $(wildcard queries/text_boxes/*.txt)
OUT_TEXT_BOXES = $(patsubst queries/text_boxes/%.txt,out/text_boxes/%.png,$(IN_TEXT_BOXES))

.DEFAULT: OUT_FRAMES OUT_TEXT_BOXES

# don't ever delete intermediates -- we want to have on-disk caching.
.SECONDARY:

# include make rules for calculating frame dependencies
include $(patsubst queries/frames/%.txt,queries/frames/%/make_rule.make,$(IN_FRAMES))

out/frames/%.png: queries/frames/%/make_rule.make

queries/frames/%/make_rule.make: queries/frames/%/ids.txt ./meta/makefile_from_ids.py
	mkdir -p queries/frames/$*
	./meta/makefile_from_ids.py --output_prefix_path=out/frames --input_prefix_path=raw/border_crop.png $* $< > $@

# include make rules for calculating textbox dependencies
include $(patsubst queries/text_boxes/%.txt,queries/text_boxes/%/make_rule.make,$(IN_TEXT_BOXES))

out/text_boxes/%.png: queries/text_boxes/%/make_rule.make

queries/text_boxes/%/make_rule.make: queries/text_boxes/%/ids.txt ./meta/makefile_from_ids.py
	mkdir -p queries/text_boxes/$*
	./meta/makefile_from_ids.py --output_prefix_path=out/text_boxes --input_prefix_path=cleaned/textbox_crop.png $* $< > $@

# get query result from scryfall and cache resulting ids on disk
queries/text_boxes/%/ids.txt: queries/text_boxes/%.txt
	mkdir -p queries/text_boxes/$*
	./query-scryfall.py "$$(cat $<)" > $@

# clean card images
card_cache/%/cleaned/titleline_crop.png: card_cache/%/raw/titleline_crop.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@
card_cache/%/cleaned/typeline_crop.png: card_cache/%/raw/typeline_crop.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@
card_cache/%/cleaned/textbox_crop.png: card_cache/%/raw/textbox_crop.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@
card_cache/%/cleaned/powerbox_crop.png: card_cache/%/raw/powerbox_crop.png ./cleaning_cellular_automata.py
	mkdir -p $$(dirname $@)
	./clean_image.py $< $@

# crop card images
card_cache/%/raw/border_crop.png: card_cache/%/card_image.png card_cache/%/raw
	python ./crop-card-border.py $* $@

card_cache/%/raw/titleline_crop.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop $(TITLELINE_W)x$(TITLELINE_H)+$(TITLELINE_X)+$(TITLELINE_Y) +repage $@

card_cache/%/raw/typeline_crop.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop $(TYPELINE_W)x$(TYPELINE_H)+$(TYPELINE_X)+$(TYPELINE_Y) +repage $@

card_cache/%/raw/textbox_crop.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop $(TEXTBOX_W)x$(TEXTBOX_H)+$(TEXTBOX_X)+$(TEXTBOX_Y) +repage $@

card_cache/%/raw/powerbox_crop.png: card_cache/%/card_image.png card_cache/%/raw
	convert $< -crop $(POWERBOX_W)x$(POWERBOX_H)+$(POWERBOX_X)+$(POWERBOX_Y) +repage $@

# download card image
card_cache/%/card_image.png: card_cache/%/card.json
	bash -c "curl $$(jq '.image_uris.png' $<) -o $@"
	sleep 0.2


# downloading allcards json
all_cards:
	mkdir $@
card_cache/%/raw:
	mkdir $@

all_cards/allCards.json.xz: all_cards/
	curl https://www.mtgjson.com/files/AllPrintings.json.xz > all_cards/allCards.json.xz

all_cards/allCards.json: all_cards/allCards.json.xz
	rm -f all_cards/allCards.json
	unxz -k all_cards/allCards.json.xz
