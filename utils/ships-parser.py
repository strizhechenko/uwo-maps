#!/usr/bin/env python3
# coding: utf-8

from requests import get
import bs4
from jinja2 import Template

wiki = 'https://unchartedwaters.fandom.com'
my_adv = 29
my_trade = 58
my_battle = 16


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--first')
#     parser.add_argument('--second')
#     parser.add_argument('--route', default='to_india')
#     return parser.parse_args()


# def city_url(city: str) -> str:
#     city = city.replace(" ", "_")
#     url = 'https://unchartedwaters.fandom.com/wiki/{0}/Market'.format(city)
#     if head(url).status_code == 404:
#         url = 'https://unchartedwaters.fandom.com/wiki/{0}'.format(city)
#     return url
#
#
# def market_table_separate(data: str):
#     soup = bs4.BeautifulSoup(data, "html.parser")
#     market_table = None
#     market_keeper = soup.find('span', id="Market_Keeper")
#     if market_keeper:
#         market_table = market_keeper.find_next('table')
#     if not market_table:
#         market_table = soup.find('table', {'style': "width: 100%;;"})
#     if not market_table:
#         market_table = soup.find('table', {'style': "width: 100%;"})
#     # Some cities has list of language table first
#     if market_table:
#         if any('Language' in item.text for item in market_table.contents if isinstance(item, bs4.Tag)):
#             market_table = market_table.find_next('table', {'style': "width: 100%;"})
#     return market_table
#
#
# def parse_market_table(market_table) -> set:
#     goods = set()
#     for link in market_table.find_all('a'):
#         href = link.attrs.get('href', '')
#         if not href.startswith('/wiki/'):
#             continue
#         if ':' in href:
#             continue
#         if 'Investing' in href:
#             continue
#         good = href.split('/')[-1]
#         goods.add(good)
#     return goods
#
#
# def fetch_market_goods(city: str) -> set:
#     url = city_url(city)
#     request = get(url)
#     market_table = market_table_separate(request.content)
#     if not market_table:
#         return {"Have no idea what they sale"}
#     return parse_market_table(market_table)
#
#
# def common(first, second) -> dict:
#     first = fetch_market_goods(first)
#     second = fetch_market_goods(second)
#     return {
#         "first": first,
#         "second": second,
#         "common": first & second
#     }


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
