

import re
import feedparser
from flask import Flask
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, "/")


HT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - High Tide')
LT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - Low Tide')

URL = 'https://www.tidetimes.org.uk/leith-tide-times.rss'

tide = feedparser.parse(URL)

tide_data = tide['entries'][0]['summary']

high_tide = re.findall(HT_MATCH, tide_data)
low_tide = re.findall(LT_MATCH, tide_data)


def tide_message(times):
    if len(times) == 2:
        first, second = times
        msg = f'low tide in leith is at {first} and at {second}'
    else:
        first, *_ = times
        msg = f'low tide in leith is at {first}'
    return msg


@ask.launch
def tide_report():
    welcome_msg = tide_message(low_tide)
    return statement(welcome_msg)


if __name__ == '__main__':

    app.run()
