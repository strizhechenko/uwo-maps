# coding=utf-8
import datetime
import json

from flask import Flask, render_template, request

from .nanban import read_all, total_load
from .nanban.liners import Liner

app = Flask(__name__)


@app.route('/data')
def data():
    with open('./cache.json') as fd:
        return json.load(fd)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        print(request.form)
    else:
        bazaar, fleet, cargo, sellers, hints, eu_items = read_all()
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
    return render_template('dashboard.html', liners=liners, now=now, load=load)


@app.route('/')
def index():
    _data = data()
    return render_template('index.html', data=_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
