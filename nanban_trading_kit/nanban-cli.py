#!/usr/bin/env python3

import argparse

from .nanban import total_load, sell, read_all
from .nanban.liners import liners


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bazaar', action='store_true', help='Учитывать базар')
    parser.add_argument('--fleet', action='store_true', help='Учитывать флот')
    parser.add_argument('--sell', action='store_true', help='Едем продавать')
    parser.add_argument('--liner', action='store_true', help='Расписание лайнеров')
    args = parser.parse_args()
    bazaar, fleet, cargo, sellers, hints, eu_items = read_all()
    if args.sell:
        sell(fleet, sellers, hints)
    elif args.liner:
        liners()
    else:
        total_load(cargo, bazaar, fleet, eu_items, count_bazaar=args.bazaar, count_fleet=args.fleet, per_toon=True)


if __name__ == '__main__':
    main()
