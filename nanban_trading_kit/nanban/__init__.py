from collections.__init__ import Counter
from operator import itemgetter

import yaml
from colorama import Fore

from .prints import bools, header


def read_all():
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
    return bazaar, fleet, cargo, sellers, hints, eu_items


def total_load(cargo, bazaar, fleet, eu_items, count_fleet=True, count_bazaar=True, per_toon=False):
    """ TODO: заменить на возврат дикта"""
    results = {}
    if count_fleet and not count_bazaar:
        header("Only things in fleet (go EU case, use --sell)", Fore.LIGHTMAGENTA_EX)
    elif count_bazaar and not count_fleet:
        header("Only things in bazaar (liner case)", Fore.LIGHTMAGENTA_EX)
    else:
        print(f'Fleet: {bools[count_fleet]} Bazaar: {bools[count_bazaar]}')
    c = Counter()
    b = bazaar if count_bazaar else {}
    f = fleet if count_fleet else {}
    results['per_toon'] = bazaar_per_toon(bazaar, count_bazaar, per_toon)
    results['per_goods'] = bazaar_per_goods(b, c, f)
    results['calc'] = {}
    fleet_cargo = sum(cargo.values()) - 200 - 24 * 2
    results['calc']["Fleet cargo (const)"] = fleet_cargo
    # col('Total', sum(c.values()))
    ea = sum(v for k, v in c.items() if k not in eu_items)
    results['calc']['EA (has)'] = ea
    wine = int(c['Wine'] + c['Raisins'] * success_rate)
    results['calc']['EA (with nanban)'] = wine + ea
    lack = fleet_cargo - wine - ea
    # color = Fore.RED if lack > 0 else Fore.LIGHTGREEN_EX
    results['calc']['Lack'] = lack
    results['calc']['Wine ~'] = wine
    results['calc']['EA goods to buy'] = fleet_cargo - ea
    if fleet_cargo - ea - wine > 100 and not count_fleet:
        header("I'm a liar go by sea!", Fore.YELLOW)
        results['calc']['Дефицит'] = fleet_cargo - ea - wine
    elif fleet_cargo - ea - wine < 100 and count_fleet:
        header("Probably you don't need fleet, go liner", Fore.YELLOW)
        # liners()
        # total_load(cargo, bazaar, fleet, eu_items, count_fleet=False)
    return results


def bazaar_per_goods(b, c, f):
    d = Counter()
    for toon in b.values():
        c.update(toon)
    for toon in f.values():
        c.update(toon)
    for key in 'Wine', 'Raisins':
        d[key] = c[key]
    for key, v in sorted(c.items(), key=itemgetter(1)):
        d[key] = c[key]
    return d


def bazaar_per_toon(bazaar, count_bazaar, per_toon):
    result = {}
    if count_bazaar and per_toon:
        header("Current bazaar per toon")
        for toon, things in bazaar.items():
            result[toon] = sum(Counter(things).values())
    return result


def calc_deals(deals):
    while sum(deals.values()) > 0:
        calc_deal(deals)


def calc_deal(deals):
    for good, amount in sorted(deals.items(), key=itemgetter(1), reverse=True):
        print(f'{good}: {deals[good]}')
        deals[good] = 0


def sell(fleet, sellers, hints):
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


success_rate = 1.86
