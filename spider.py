# coding=utf-8

from bs4 import BeautifulSoup
from bs4.element import Tag
from requests_filecache import get
import argparse

ENDPOINT = 'https://unchartedwaters.fandom.com'


def parse_args():
    """ Разбор аргументов """
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', required=True)
    parser.add_argument('--no-download', action='store_false', dest='download', default=True)
    parser.add_argument('--no-parse-books', action='store_false', dest='parse_books', default=True)
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


def links_to_cookbooks():
    books = get('https://unchartedwaters.fandom.com/wiki/Cook_books')
    soup = BeautifulSoup(books, 'html.parser')
    table = soup.find('table', {'class': 'UWtable burlywood'})
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 2:
            book_link = columns[2].find('a').attrs.get('href')
            if book_link:
                yield ENDPOINT + book_link


def parse_cookbook(book_link):
    """ Разбирает рецепты из кулинарной книги"""
    book = get(book_link)
    soup = BeautifulSoup(book, 'html.parser')
    table = soup.find('table', {'class': 'BookNfoTable'})
    if table:
        recipes = [content for content in table.contents if isinstance(content, Tag)]
        for recipe in recipes[1:-1]:
            yield parse_recipe(recipe)


def parse_recipe(recipe):
    """ Разбирает строку рецепта на уровень-название-ингридиенты """
    level, name, ingridients, result = [content for content in recipe.contents if isinstance(content, Tag)]
    level = int(level.text.strip())
    name = name.find('b').text if name.find('b') else name.contents[0].split('.')[1].strip()
    ingridients = [a.attrs['href'] for a in ingridients.find('tr').find_all('a')]
    return level, name, ingridients


def main():
    args = parse_args()
    if args.download:
        for city in links_to_cities(args.region):
            for good in parse_market(ENDPOINT + city + '/Market'):
                get(ENDPOINT + good)
    if args.parse_books:
        for book in links_to_cookbooks():
            for level, name, ingridients in parse_cookbook(book):
                print(level, name, ingridients)


if __name__ == '__main__':
    main()
