#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s <query_name> <path_to_ids_fil>" % sys.argv[0])
        exit(1)

    query_name = sys.argv[1]
    in_path = sys.argv[2]
    card_ids = open(in_path, 'r').read().strip().split(' ')

    print("out/frames/%s.png: %s\n\t./composite.py $<"%(
        query_name,
        ' '.join(["card_cache/%s/raw/border_crop.png" % card_id for card_id in card_ids])
    ))