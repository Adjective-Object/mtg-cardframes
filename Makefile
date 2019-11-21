
TITLELINE_X := 54
TITLELINE_Y := 56
TITLELINE_W := 637
TITLELINE_H := 48

TYPELINE_X := 56
TYPELINE_Y := 594
TYPELINE_W := 632
TYPELINE_H := 45

TEXTBODY_X := 58
TEXTBODY_Y := 655
TEXTBODY_W := 628
TEXTBODY_H := 285

POWERBOX_X := 590
POWERBOX_Y := 930
POWERBOX_W := 104
POWERBOX_H := 46

FRAMES = out/frames/red_commons.png

.DEFAULT: FRAMES

# don't ever delete intermediates -- we want to have on-disk caching.
.SECONDARY:

# include make rules for calculating frame dependencies
include $(patsubst out/frames/%.png,queries/frames/%/make_rule.make,$(FRAMES))

out/frames/%.png: queries/frames/%/make_rule.make

queries/frames/%/make_rule.make: queries/frames/%/ids.txt ./meta/make_frame_makefile.py
	./meta/make_frame_makefile.py $* $< > $@

# get query result and depset from legends
queries/frames/%/ids.txt: queries/frames/%.txt
	./query-scryfall.py "$$(cat $<)" > $@

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
queries/frames/%:
	mkdir $@

all_cards/allCards.json.xz: all_cards/
	curl https://www.mtgjson.com/files/AllPrintings.json.xz > all_cards/allCards.json.xz

all_cards/allCards.json: all_cards/allCards.json.xz
	rm -f all_cards/allCards.json
	unxz -k all_cards/allCards.json.xz
