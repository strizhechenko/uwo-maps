#!/usr/bin/env python

import argparse
import requests
import bs4
from routes import to_india
from jinja2 import Template


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('first')
    parser.add_argument('second')
    return parser.parse_args()


def city_url(city: str) -> str:
    return 'https://unchartedwaters.fandom.com/wiki/{0}/Market'.format(city)


def market_table_separate(data: str):
    soup = bs4.BeautifulSoup(data, "html.parser")
    market_table = soup.find('table', {'style': "width: 100%;;"})
    if not market_table:
        market_table = soup.find('table', {'style': "width: 100%;"})
    return market_table


def parse_market_table(market_table) -> set:
    goods = set()
    for link in market_table.find_all('a'):
        href = link.attrs.get('href', '')
        if not href.startswith('/wiki/'):
            continue
        if ':' in href:
            continue
        if 'Investing' in href:
            continue
        good = href.split('/')[-1]
        goods.add(good)
    return goods


def fetch_market_goods(city: str) -> set:
    city = city.replace(" ", "_")
    url = city_url(city)
    request = requests.get(url)
    if request.status_code == 404:
        url = 'https://unchartedwaters.fandom.com/wiki/{0}'.format(city)
        request = requests.get(url)
    market_table = market_table_separate(request.content)
    if not market_table:
        return set()
    return parse_market_table(market_table)


def diff(first, second):
    first = fetch_market_goods(first)
    second = fetch_market_goods(second)
    for good in first - second:
        yield good


def main():
    prev = None
    template = Template(open("goods.jinja2").read())
    for city in to_india:
        if prev:
            print(template.render({
                "first": prev,
                "second": city,
                "first_url": city_url(prev),
                "second_url": city_url(city),
                "goods": diff(prev, city)
            }))
        prev = city


if __name__ == '__main__':
    main()
