# coding=utf-8

import argparse

from covid.utils import url2soup


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--adv', default=90, type=int)
    parser.add_argument('--trade', default=90, type=int)
    parser.add_argument('--battle', default=90, type=int)
    return parser.parse_args()


def ship_list():
    """ Возвращаем список торговых кораблей"""
    soup = url2soup("https://unchartedwaters.fandom.com/wiki/Ships/Battle_Ships")
    ships = soup.find('table')
    links = [ship.find('a') for ship in ships.children]
    return [link for link in links if link != -1 and link.attrs['href'].startswith('/wiki/')]


def ship_process(link, args=None):
    url = "https://unchartedwaters.fandom.com" + (link if isinstance(link, str) else link.attrs['href'])
    ship_soup = url2soup(url)
    ship_data = ship_soup.find('table', attrs={'class': 'BioTable'})
    adv, trade, battle = ship_data.find('table').find_all('tr')[2].text.strip().split()
    if args is not None:
        for key in ['adv', 'trade', 'battle']:
            if int(locals()[key]) > getattr(args, key):
                return
    raw_data = ship_data.find('table', attrs={"style": not None}).find_all('tr')
    raw_data = [item.text.strip() for item in raw_data if item.text.strip()]
    sails = raw_data[8].split()[2]
    vsail, hsail, rowing, dura = raw_data[3].split()
    sailors, guns, cargo_hold = raw_data[6].split()
    sailors_req = sailors.split('/')[0]
    print("\t".join([url, adv, trade, battle, cargo_hold, sailors_req, hsail, vsail, sails]))


def main():
    args = parse_args()
    for link in ship_list():
        ship_process(link, args)


if __name__ == '__main__':
    main()
