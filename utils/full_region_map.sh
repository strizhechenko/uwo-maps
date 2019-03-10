#!/usr/bin/env bash

python3 spider.py --make-graph --region $1 > $1.gv
gv2map $1.gv $1.png
open $1.png
