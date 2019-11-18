#!/usr/bin/env bash

set -ex

python ./get_all_assets.py
python ./get_all_borders.py
python ./get_text_bodies.py
python ./get_title_lines.py
python ./get_type_lines.py
python ./get_power_boxes.py
python ./create_layered_images.py
