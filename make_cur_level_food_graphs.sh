#!/bin/bash

set -xeuE

declare LEVEL="$1"

mkdir -p graphs images
python3 spider.py --region Europe --level "$LEVEL" --recipes --no-make-graph \
	| while read -r recipe; do
		python3 spider.py --region Europe \
			--level "$LEVEL" \
			--recipe "$recipe" > "graphs/$recipe.gv"
		gv2map "graphs/$recipe.gv" "images/$recipe.png"
	done
