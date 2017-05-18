

import re
import feedparser
from flask import Flask, render_template
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, "/alexa_skill")


HT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - High Tide')
LT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - Low Tide')

URL = 'https://www.tidetimes.org.uk/leith-tide-times.rss'


def get_tide_times(url):
    tide = feedparser.parse(url)
    tide_data = tide['entries'][0]['summary']
    high_tide = re.findall(HT_MATCH, tide_data)
    low_tide = re.findall(LT_MATCH, tide_data)
    return (low_tide, high_tide)


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
    low_tides, high_tides = get_tide_times(URL)
    return render_template('base.html', low_tides=low_tides, high_tides=high_tides)


@ask.launch
def tide_report():
    tides = get_tide_times(URL)
    welcome_msg = tide_message(tides)
    return statement(welcome_msg)


if __name__ == '__main__':

    app.run()
