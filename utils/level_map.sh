#!/bin/bash

set -euE

for level in {1..9}; do
	python3 ./utils/spider.py --level $level --region Europe > graphs/Europe_$level.gv
	gv2map graphs/Europe_$level.gv images/0$level/_FULL_EUROPE.png
done
for level in {10..18}; do
	python3 ./utils/spider.py --level $level --region Europe > graphs/Europe_$level.gv
	gv2map graphs/Europe_$level.gv images/$level/_FULL_EUROPE.png
done
