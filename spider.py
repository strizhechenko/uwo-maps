# coding=utf-8

from bs4 import BeautifulSoup
from requests import get
import argparse
import os


def parse_args():
    """ Разбор аргументов """
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', required=True)
    return parser.parse_args()


def read_region(region):
    """ Читает страницу из кэша или скачивает и кэширует """
    os.makedirs('content/Region/', exist_ok=True)
    filename = 'content/Region/' + region + '.html'
    if not os.path.exists(filename):
        url = 'https://unchartedwaters.fandom.com/wiki/Region/'
        data = get(url + region).content.decode('utf-8')  # .encode('utf-8')
        with open(filename, 'w', encoding='utf-8') as fd:
            fd.write(data)
    else:
        with open(filename, 'r', encoding='utf-8') as fd:
            data = fd.read()
    return data


def parse_region(region):
    """ Находит ссылки на города """
    data = read_region(region)
    soup = BeautifulSoup(data, 'html.parser')
    for _map in soup.findAll('map'):
        for area in _map:
            if area.attrs['shape'] == 'circle':
                print(area.attrs['href'])


if __name__ == '__main__':
    args = parse_args()
    parse_region(args.region)
