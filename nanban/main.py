#!/usr/bin/env python3

import argparse
from collections import Counter
from operator import itemgetter

import yaml
from colorama import Fore

from prints import col, wrap, header, bools

success_rate = 1.86


def read_all():
    global bazaar, fleet, cargo, sellers, hints, eu_items
    with open('bazaar.yml') as fd:
        bazaar = yaml.load(fd, yaml.SafeLoader)
    with open('fleet.yml') as fd:
        fleet = yaml.load(fd, yaml.SafeLoader)
    with open('cargo.yml') as fd:
        cargo = yaml.load(fd, yaml.SafeLoader)
    with open('sellers.yml') as fd:
        sellers = yaml.load(fd, yaml.SafeLoader)
    with open('hints.yml') as fd:
        hints = yaml.load(fd, yaml.SafeLoader)
    with open('goods.yml') as fd:
        eu_items = yaml.load(fd, yaml.SafeLoader)['eu']


def total_load(count_fleet=True, count_bazaar=True, per_toon=False):
    if count_fleet and not count_bazaar:
        header("Only things in fleet (go EU case, use --sell)", Fore.LIGHTMAGENTA_EX)
    elif count_bazaar and not count_fleet:
        header("Only things in bazaar (liner case)", Fore.LIGHTMAGENTA_EX)
    else:
        print(f'Fleet: {bools[count_fleet]} Bazaar: {bools[count_bazaar]}')
    c = Counter()
    b = bazaar if count_bazaar else {}
    f = fleet if count_fleet else {}
    bazaar_per_toon(count_bazaar, per_toon)
    bazaar_per_goods(b, c, f)
    header("Totals")
    fleet_cargo = sum(cargo.values()) - 200 - 24 * 2
    col("Fleet cargo (const)", fleet_cargo)
    # col('Total', sum(c.values()))
    ea = sum(v for k, v in c.items() if k not in eu_items)
    col('EA (has)', ea)

    wine = int(c['Wine'] + c['Raisins'] * success_rate)

    col('EA (with nanban)', wine + ea)
    lack = fleet_cargo - wine - ea
    color = Fore.RED if lack > 0 else Fore.LIGHTGREEN_EX
    col('Lack', wrap(lack, color))
    col('Wine ~', wine)
    col('EA goods to buy', fleet_cargo - ea)
    if fleet_cargo - ea - wine > 100 and not count_fleet:
        header("I'm a liar go by sea!", Fore.YELLOW)
        col('Дефицит', fleet_cargo - ea - wine)
    elif fleet_cargo - ea - wine < 100 and count_fleet:
        header("Probably you don't need fleet, go liner", Fore.YELLOW)
        total_load(count_fleet=False)


def bazaar_per_goods(b, c, f):
    header("Total goods")
    for toon in b.values():
        c.update(toon)
    for toon in f.values():
        c.update(toon)
    for item, count in c.items():
        print(f'{item:20}: {count}')


def bazaar_per_toon(count_bazaar, per_toon):
    if count_bazaar and per_toon:
        header("Current bazaar per toon")
        for toon, things in bazaar.items():
            col(toon, sum(Counter(things).values()))


def calc_deals(deals):
    while sum(deals.values()) > 0:
        calc_deal(deals)


def calc_deal(deals):
    for good, amount in deals.items():
        print(f'{good}: {deals[good]}')
        deals[good] = 0


def sell():
    header("Продаём")
    c = Counter()
    for toon in fleet.values():
        c.update(toon)
    dirty = set()
    goods_total = list()
    for seller, goods in sellers.items():
        for good in goods:
            if good in c:
                dirty.add(seller)
                goods_total.append((seller, good, c[good]))
        if seller in dirty:
            header(seller, color=Fore.YELLOW)
            print(hints[seller])
            deals = {good_[1]: good_[2] for good_ in goods_total if good_[0] == seller}
            calc_deals(deals)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bazaar', action='store_true', help='Учитывать базар')
    parser.add_argument('--fleet', action='store_true', help='Учитывать флот')
    parser.add_argument('--sell', action='store_true', help='Едем продавать')
    args = parser.parse_args()
    read_all()
    if args.sell:
        sell()
    else:
        total_load(count_bazaar=args.bazaar, count_fleet=args.fleet, per_toon=True)


if __name__ == '__main__':
    main()
