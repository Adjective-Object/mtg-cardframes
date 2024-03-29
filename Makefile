
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

.DEFAULT_GOAL = default

# include make rules for calculating frame dependencies
include ./regions.make

regions.make: config.json gen_makefile.py
	python ./gen_makefile.py > regions.make


default: $(REGION_title_line_OUT) $(REGION_power_box_OUT) $(REGION_text_body_OUT) $(REGION_frame_OUT) 

# don't ever delete intermediates -- we want to have on-disk caching.
.SECONDARY:

# download card image
card_cache/%/card_image.png: card_cache/%/card.json
	bash -c "curl $$(jq '(.image_uris//.card_faces[0].image_uris).png' $<) -o $@"
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
