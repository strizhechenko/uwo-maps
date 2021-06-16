# coding=utf-8
import datetime
import json

import yaml
from flask import Flask, render_template, request

from .nanban import read_all, total_load
from .nanban.liners import Liner

app = Flask(__name__)


@app.route('/data')
def data():
    with open('./cache.json') as fd:
        return json.load(fd)


def _add(d: dict, toon: str, good: str, amount: int):
    if toon not in d:
        d[toon] = dict()
    d[toon][good] = int(amount)


def write_all(bazaar, fleet):
    with open('bazaar.yml', 'w') as fd:
        yaml.dump(bazaar, fd, yaml.SafeDumper, default_flow_style=False)
    with open('fleet.yml', 'w') as fd:
        yaml.dump(fleet, fd, yaml.SafeDumper, default_flow_style=False)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        bazaar, fleet = {}, {}
        print(request.form)
        action = 'recalculate'
        for k, v in request.form.items():
            if v == '':
                action = k
                continue
            cat, toon, good = k.split('_')
            _add(bazaar if cat == 'bazaar' else fleet, toon, good, v)
        if action == 'rewrite':
            write_all(bazaar, fleet)
        _, _, cargo, sellers, hints, eu_items = read_all()
    else:
        bazaar, fleet, cargo, sellers, hints, eu_items = read_all()
    print('bazaar', bazaar)
    print('fleet', fleet)
    _data = {
        'bazaar': bazaar,
        'fleet': fleet,
        'sellers': sellers,
        'hints': hints,
        'eu_items': eu_items
    }
    liners = (Liner(35, 'London', 'Nagasaki'), Liner(25, 'London', 'Colony'))
    now = datetime.datetime.now()
    load = total_load(cargo, bazaar, fleet, eu_items, count_fleet=True, count_bazaar=True, per_toon=True)
    print(load)
    return render_template('dashboard.html', liners=liners, now=now, load=load, bazaar=bazaar, fleet=fleet)


@app.route('/')
def index():
    _data = data()
    return render_template('index.html', data=_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
