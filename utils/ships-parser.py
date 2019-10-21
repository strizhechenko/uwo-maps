#!/usr/bin/env python3
# coding: utf-8

from requests import get
import bs4
from jinja2 import Template

wiki = 'https://unchartedwaters.fandom.com'
my_adv = 29
my_trade = 58
my_battle = 16


def ship_url_list(list_url):
    """ Список URL кораблей """
    data = get(list_url).text
    soup = bs4.BeautifulSoup(data, "html.parser")
    table = soup.find('table', attrs={'class': 'UWtable burlywood'})
    rows = table.find_all('tr')
    c = 0
    for row in rows:
        c += 1
        cell = row.find('td')
        if cell:
            if cell.attrs.get('class') == 'nfo imgbox':
                continue
            link = cell.find('a')
            if link and not link.attrs.get('class') and link.attrs.get('href'):
                yield link.attrs['href']


def parse_ship(ship_url):
    data = get(ship_url).text
    soup = bs4.BeautifulSoup(data, "html.parser")
    adv = soup.find('a', attrs={'title': 'Adventure'})
    adv, trade, battle = [int(level) for level in adv.parent.text.strip().split()]
    if max(adv - my_adv, trade - my_trade, battle - my_battle) <= 3:
        hold = soup.find('a', attrs={'title': 'Hold'})
        if hold:
            hold = int(hold.parent.parent.find_all('td', attrs={'style': "width: 50px"})[2].text.strip())
            print(ship_url, adv, trade, battle, hold)


def main():
    for ship_url in ship_url_list(wiki + '/wiki/Ships/Trade_Ships'):
        parse_ship(wiki + ship_url)


if __name__ == '__main__':
    main()
