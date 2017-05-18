

import json
from flask import Flask, render_template
from flask_ask import Ask, statement

from constants import TIDE_FILE


app = Flask(__name__)

ask = Ask(app, "/alexa_skill")


def load_from_json(filename):
    """ Get data from JSON file. """
    with open(filename, 'r') as infile:
        todays_words = json.load(infile)
    return todays_words


def tide_message(tides):
    low, high = tides
    if len(low) == 2:
        first, second = low
        msg = 'low tide in leith is at {} and at {}'.format(first, second)
    else:
        first, *_ = low
        msg = 'low tide in leith is at {}'.format(first)
    return msg


@app.route('/')
def show_tides():
    low_tides, high_tides = load_from_json(TIDE_FILE)
    return render_template('base.html', low_tides=low_tides, high_tides=high_tides)


@ask.launch
def tide_report():
    tides = load_from_json(TIDE_FILE)
    welcome_msg = tide_message(tides)
    return statement(welcome_msg)


if __name__ == '__main__':

    app.run()
