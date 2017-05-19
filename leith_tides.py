

import json
import os
import datetime as dt
from flask import Flask, render_template
from flask_ask import Ask, statement

import tide_update
from constants import TIDE_FILE


app = Flask(__name__)

ask = Ask(app, "/alexa_skill")


def load_tide_data(filename):
    """
    Load tide data from file.

    If file does not exist, call the update
    module and create file, then load.

    """
    if not os.path.isfile(filename):
        tide_update.main()
    with open(filename, 'r') as infile:
        todays_tides = json.load(infile)
    return todays_tides


def get_date_object(tides):
    low_tide, high_tide = load_tide_data(tides)
    low = [dt.datetime.strptime(tide, '%H:%M') for tide in low_tide]
    high = [dt.datetime.strptime(tide, '%H:%M') for tide in high_tide]
    return [low, high]


def normalise_now():
    time_now = dt.datetime.now().time()
    return dt.datetime(1900, 1, 1, time_now.hour, time_now.minute)


def build_message(tides):
    low_intro = 'low tide in leith'
    high_intro = 'high tide'
    
    now = normalise_now()
    print(now)
    low_times, high_times = get_date_object(tides)
    print(low_times)
    print(high_times)

    if len(low_times) == 1:
        only_low, *_ = low_times
        str_only_low = only_low.strftime('%H:%M')
        if only_low.time() > now.time():
            low_msg = '{} will be at {}'.format(low_intro, str_only_low)
        else:
            low_msg = '{} was at {}'.format(low_intro, str_only_low)
    else:
        first_low, second_low = low_times
        str_first_low = first_low.strftime('%H:%M')
        str_second_low = second_low.strftime('%H:%M')
        if abs(now - first_low) < abs(now - second_low):
            if first_low.time() > now.time():
                low_msg = '{} will be at {}'.format(low_intro, str_first_low)
            else:
                low_msg = '{} was at {}'.format(low_intro, str_first_low)
        else:
            if second_low.time() > now.time():
                low_msg = '{} will be at {}'.format(low_intro, str_second_low)
            else:
                low_msg = '{} was at {}'.format(low_intro, str_second_low)

    if len(high_times) == 1:
       only_high, *_ = high_times
       str_only_high = only_high.strftime('%H:%M')
       if only_high.time() > now.time():
           high_msg = '{} will be at {}'.format(high_intro, str_only_high)
       else:
           high_msg = '{} was at {}'.format(high_intro, str_only_high)
    else:
        first_high, second_high = high_times
        str_first_high = first_high.strftime('%H:%M')
        str_second_high = second_high.strftime('%H:%M')
        if abs(now - first_high) < abs(now - second_high):
            if first_high.time() > now.time():
                high_msg = '{} will be at {}'.format(high_intro, str_first_high)
            else:
                high_msg = '{} was at {}'.format(high_intro, str_first_high)
        else:
            if second_high.time() > now.time():
                high_msg = '{} will be at {}'.format(high_intro, str_second_high)
            else:
                high_msg = '{} was at {}'.format(high_intro, str_second_high)

    return ' '.join([low_msg, high_msg])


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
    low_tides, high_tides = load_tide_data(TIDE_FILE)
    return render_template('base.html', low_tides=low_tides, high_tides=high_tides)


@ask.launch
def tide_report():
    tides = load_tide_data(TIDE_FILE)
    welcome_msg = tide_message(tides)
    return statement(welcome_msg)


if __name__ == '__main__':

    app.run()
