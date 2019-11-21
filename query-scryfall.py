#!/usr/bin/env python3

import os, sys, json, urllib.parse
import requests
import config

def save_card_if_new(card):
    card_path = os.path.join(config.CARD_DATA_DIR, card["id"])
    card_json_path = os.path.join(card_path, config.CARD_JSON_NAME)
    if os.path.isfile(card_json_path):
        return

    if not os.path.isdir(config.CARD_DATA_DIR):
        os.mkdir(config.CARD_DATA_DIR)
    
    if not os.path.isdir(card_path):
        os.mkdir(card_path)

    with open(card_json_path, 'w') as f:
        sys.stderr.write("caching card %s to %s\n" % (card['name'], card_path))
        json.dump(card, f)

def query_scryfall(query_string):
    sys.stderr.write("querying scryfall with \"%s\"\n" % query_string)
    page_url ='https://api.scryfall.com/cards/search?q=' + urllib.parse.quote(query_string)
    cards = []
    while page_url:
        sys.stderr.write("making request to scryfall for page %s\n" % page_url)
        response = requests.get(page_url)
        if response.status_code != 200:
            raise Exception("got bad response from server: " + response.text)
    
        response_body = response.json()
        page_url = response_body["next_page"] if "next_page" in response_body else None

        for card in response_body["data"]:
            save_card_if_new(card)
            cards.append(card)
    
    return cards

if __name__ == "__main__":
    cards = query_scryfall(''.join(sys.argv[1:]))
    print(" ".join((c["id"] for c in cards)))
