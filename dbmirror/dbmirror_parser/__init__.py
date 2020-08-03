# coding=utf-8

from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/data')
def data():
    with open('./cache.json') as fd:
        return json.load(fd)


@app.route('/')
def index():
    _data = data()
    return render_template('index.html', data=_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
