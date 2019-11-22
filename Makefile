
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

# include make rules for calculating frame dependencies
include ./regions.make

.DEFAULT: $(REGION_frame_OUT) $(REGION_title_line_OUT)

# don't ever delete intermediates -- we want to have on-disk caching.
.SECONDARY:

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
