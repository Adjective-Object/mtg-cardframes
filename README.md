# MTG cardframe kludge

A kludge of scripts for extracting a _mostly_ clean set of blank magic card frame PNGs

## Overview

This tool supports

- legend frames
- separate creature & non-creature frames
- enchantment creature frames

It does not yet support any of:

- extracting enchanment creatures & power boxes into their own overlays with [triangulation matting](https://github.com/Adjective-Object/CSC320/blob/master/p4/p4.py)
- Cards with identity-based outside their assigned face colours (e.g. [Polluted Delta](https://scryfall.com/card/ktk/239/polluted-delta) and the other multicoloured lands)
- split-devotion frames (e.g. [Elite Headhunter](https://scryfall.com/card/eld/209/elite-headhunter))
- adventure creature frames
- storybook creatures
- vehicle frames

I would like to support planeswalkers, but don't think there are enough available for the approach these scripts take.

## Usage

1.  In bash:

    ```sh
    yarn
    virtualenv create ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ./RUN_EVERYTHING.sh
    ```

    This should create some card frames

2.  cross your fingers

## Approach

- Select cards, segmented by categories we care about, using scryfall search
- Get the (approximate) mean of each pixel on cards, grouped under the categories
- Crop common elements that are shared between cards and get the mean for the subelements
- Take the ouput of this and run a cellular automata on it to remove any lingering text
  - This operates on lab darkenss only -- this could probably be determined by full LAB difference with the mean colour of the region.
- Create output images by layering each of the card parts over the mean card frames
