#!/usr/bin/env python3
# coding: utf-8

import argparse
from requests import get, head
import bs4
from routes import routes
from jinja2 import Template

TEMPLATE = Template("""
===== {{ first }} -> {{ second }} =====

<hidden Все товары>
from: {{ first_url }}

{% for good in goods.first %}  * {{ good }}
{% endfor %}

to: {{ second_url }}

{% for good in goods.second %}  * {{ good }}
{% endfor %}
</hidden>

{% if goods.common %}
Общее (не покупать):

{% for good in goods.common %}  * {{ good }}
{% endfor %}
{% endif %}
""")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first')
    parser.add_argument('--second')
    parser.add_argument('--route', default='to_india')
    return parser.parse_args()


def city_url(city: str) -> str:
    city = city.replace(" ", "_")
    url = 'https://unchartedwaters.fandom.com/wiki/{0}/Market'.format(city)
    if head(url).status_code == 404:
        url = 'https://unchartedwaters.fandom.com/wiki/{0}'.format(city)
    return url


def market_table_separate(data: str):
    soup = bs4.BeautifulSoup(data, "html.parser")
    market_table = None
    market_keeper = soup.find('span', id="Market_Keeper")
    if market_keeper:
        market_table = market_keeper.find_next('table')
    if not market_table:
        market_table = soup.find('table', {'style': "width: 100%;;"})
    if not market_table:
        market_table = soup.find('table', {'style': "width: 100%;"})
    # Some cities has list of language table first
    if market_table:
        if any('Language' in item.text for item in market_table.contents if isinstance(item, bs4.Tag)):
            market_table = market_table.find_next('table', {'style': "width: 100%;"})
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
    url = city_url(city)
    request = get(url)
    market_table = market_table_separate(request.content)
    if not market_table:
        return {"Have no idea what they sale"}
    return parse_market_table(market_table)


def common(first, second) -> dict:
    first = fetch_market_goods(first)
    second = fetch_market_goods(second)
    return {
        "first": first,
        "second": second,
        "common": first & second
    }


def main():
    args = parse_args()
    prev = None
    my_route = routes[args.route]
    if args.first and args.second:
        my_route = [args.second]
        prev = args.first
    for city in my_route:
        if prev:
            print(TEMPLATE.render({
                "first": prev,
                "second": city,
                "first_url": city_url(prev),
                "second_url": city_url(city),
                "goods": common(prev, city),
            }))
        prev = city


if __name__ == '__main__':
    main()
