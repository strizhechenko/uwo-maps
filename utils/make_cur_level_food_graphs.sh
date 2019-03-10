#!/bin/bash

set -xeuE

declare LEVEL="$1"

mkdir -p graphs "images/$LEVEL"
python3 ./utils/spider.py --region Europe --level "$LEVEL" --recipes --no-make-graph \
	| while read -r recipe; do
		python3 ./utils/spider.py --region Europe \
			--level "$LEVEL" \
			--recipe "$recipe" > "graphs/$recipe.gv"
		gv2map "graphs/$recipe.gv" "images/$LEVEL/$recipe.png"
	done
