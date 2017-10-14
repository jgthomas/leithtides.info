

"""
Select the relevant tide based on its proximity to the current
time, and build a tense-appropriate string for use in voice
interfaces such as Alexa.

"""

import json
import os
import datetime as dt

import tide_update


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
    """
    Return date objects corresponding to the two high and low
    tide times for today.

    We are only interested in the time, but want to do operations that
    require a date object, so year, month and day are set to (1900, 1, 1)
    for all date objects.

    """
    low_tide, high_tide = load_tide_data(tides)
    low = [dt.datetime.strptime(tide, '%H:%M') for tide in low_tide]
    high = [dt.datetime.strptime(tide, '%H:%M') for tide in high_tide]
    return [low, high]


def normalise_now():
    """
    Set a date object to the time now, factoring out year, month
    and day to match the values in the tide datetime objects.

    """
    time_now = dt.datetime.now().time()
    return dt.datetime(1900, 1, 1, time_now.hour, time_now.minute)


def weight_tides(tides, now=None):
    """
    Report the upcoming tide unless the previous tide was under
    two hours ago, and thus still the reality on the ground now.

    tides  :  datetime objects indicating the time of two tides
    now    :  setting a time for present, used for testing purposes


    """
    first_tide, *_ = tides
    first_weight = 0
    second_weight = 0

    threshold = 4 * (60 * 60)

    if now is None:
        now = normalise_now()

    opposite_tide_window = first_tide + dt.timedelta(seconds=threshold)

    if abs(now - first_tide) < abs(now - opposite_tide_window):
        first_weight += 1
    else:
        second_weight += 1
    return (first_weight, second_weight)


def build_tide_message(tide_data, intro, now=None):
    """
    Return tense-appropriate statement reporting times of tides.

    tides  :  list of datetime objects of tide times
    intro  :  string to begin tide times report
    now    :  setting a time for present, used for testing purposes

    """
    future = 'will be at'
    past = 'was at'

    if now is None:
        now = normalise_now()

    if len(tide_data) == 1:
        only_tide, *_ = tide_data
        str_only_tide = only_tide.strftime('%H:%M')
        if only_tide.time() > now.time():
            tide_msg = '{} {} {}'.format(intro, future, str_only_tide)
        else:
            tide_msg = '{} {} {}'.format(intro, past, str_only_tide)
    else:
        first_tide , second_tide = tide_data
        weight_first_tide, weight_second_tide = weight_tides(tide_data, now)

        str_first_tide = first_tide.strftime('%H:%M')
        str_second_tide = second_tide.strftime('%H:%M')

        if weight_first_tide > weight_second_tide:
            if first_tide.time() > now.time():
                tide_msg = '{} {} {}'.format(intro, future, str_first_tide)
            else:
                tide_msg = '{} {} {}'.format(intro, past, str_first_tide)
        else:
            if second_tide.time() > now.time():
                tide_msg = '{} {} {}'.format(intro, future, str_second_tide)
            else:
                tide_msg = '{} {} {}'.format(intro, past, str_second_tide)
    return tide_msg



def tide_message(tide_times, specific_tide="both", now=None):
    """
    Return response for low, high, or both tide times.

    tides          :  list of datetime objects
    specific_tide  :  "low", "high", or "both"
    now            :  datetime object, used for testing purposes

    """
    low_intro = 'Low tide in leith'
    high_intro = 'High tide in leith'
    high_intro_second = 'High tide'

    if specific_tide == "low":
        return build_tide_message(tide_times, low_intro, now=now)

    if specific_tide == "high":
        return build_tide_message(tide_times, high_intro, now=now)

    low_times, high_times = tide_times

    low_msg = build_tide_message(low_times, low_intro, now=now)
    high_msg = build_tide_message(high_times, high_intro_second, now=now)
    return '. '.join([low_msg, high_msg])
