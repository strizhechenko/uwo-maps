# coding=utf-8

from bs4 import BeautifulSoup
from requests_filecache import get
import argparse

ENDPOINT = 'https://unchartedwaters.fandom.com'


def parse_args():
    """ Разбор аргументов """
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', required=True)
    return parser.parse_args()


def links_to_cities(region):
    """ Находит ссылки на города """
    url = ENDPOINT + '/wiki/Region/' + region
    data = get(url)
    soup = BeautifulSoup(data, 'html.parser')
    links = set()
    for _map in soup.findAll('map'):
        for area in _map:
            if area.attrs['shape'] == 'circle':
                links.add(area.attrs['href'])
    return links


def fetch_markets(region):
    """ Скачивает данные по рынкам """
    for link in links_to_cities(region):
        get(ENDPOINT + link + '/Market')


def parse_market(url):
    """ Сбор данных о конкретном рынке """
    data = get(url)
    soup = BeautifulSoup(data, 'html.parser')
    market_table = soup.find('table', {'style': "width: 100%;;"})
    if not market_table:
        market_table = soup.find('table', {'style': "width: 100%;"})
    links = set()
    if market_table:
        for link in market_table.find_all('a'):
            href = link.attrs.get('href', '')
            if not href.startswith('/wiki/'):
                continue
            if ':' in href:
                continue
            if 'Investing' in href:
                continue
            links.add(href)
    return links


def main():
    args = parse_args()
    for city in links_to_cities(args.region):
        for good in parse_market(ENDPOINT + city + '/Market'):
            get(ENDPOINT + good)


if __name__ == '__main__':
    main()
