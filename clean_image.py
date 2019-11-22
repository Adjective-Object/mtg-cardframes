#!/usr/bin/env python3
from cleaning_cellular_automata import cleaning_cellular_automata
from imageio import imread, imwrite
import sys

if __name__ == "__main__":
    in_img = imread(sys.argv[1])
    out_img = cleaning_cellular_automata(in_img)
    imwrite(sys.argv[2], out_img)