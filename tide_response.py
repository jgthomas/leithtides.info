

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
    Select which of two tide times to report

    tides  :  datetime objects indicating the time of two tides
    now    :  setting a time for present, used for testing purposes

    Always reports the upcoming tide unless the previous tide was under
    two hours ago, and thus still the reality on the ground now.

    """
    first_tide, second_tide = tides
    first_weight = 0
    second_weight = 0

    threshold = 4 * (60 * 60)
    opposite_tide_window = first_tide + dt.timedelta(seconds=threshold)

    if now is None:
        now = normalise_now()

    if abs(now - first_tide) < abs(now - opposite_tide_window):
        first_weight += 1
    else:
        second_weight += 1
    return (first_weight, second_weight)


def build_message(tides, now=None):
    low_intro = 'Low tide in leith'
    high_intro = 'High tide'
    future = 'will be at'
    past = 'was at'

    low_times, high_times = tides

    if now is None:
        now = normalise_now()

    # Generate low tide message
    if len(low_times) == 1:
        only_low, *_ = low_times
        str_only_low = only_low.strftime('%H:%M')
        if only_low.time() > now.time():
            low_msg = '{} {} {}'.format(low_intro, future, str_only_low)
        else:
            low_msg = '{} {} {}'.format(low_intro, past, str_only_low)
    else:
        first_low, second_low = low_times
        weight_first_low, weight_second_low = weight_tides(low_times)

        str_first_low = first_low.strftime('%H:%M')
        str_second_low = second_low.strftime('%H:%M')

        if weight_first_low > weight_second_low:
            if first_low.time() > now.time():
                low_msg = '{} {} {}'.format(low_intro, future, str_first_low)
            else:
                low_msg = '{} {} {}'.format(low_intro, past, str_first_low)
        else:
            if second_low.time() > now.time():
                low_msg = '{} {} {}'.format(low_intro, future, str_second_low)
            else:
                low_msg = '{} {} {}'.format(low_intro, past, str_second_low)

    # Generate high tide message
    if len(high_times) == 1:
        only_high, *_ = high_times
        str_only_high = only_high.strftime('%H:%M')
        if only_high.time() > now.time():
            high_msg = '{} {} {}'.format(high_intro, future, str_only_high)
        else:
            high_msg = '{} {} {}'.format(high_intro, past, str_only_high)
    else:
        first_high, second_high = high_times
        weight_first_high, weight_second_high = weight_tides(high_times)

        str_first_high = first_high.strftime('%H:%M')
        str_second_high = second_high.strftime('%H:%M')

        if weight_first_high > weight_second_high:
            if first_high.time() > now.time():
                high_msg = '{} {} {}'.format(high_intro, future, str_first_high)
            else:
                high_msg = '{} {} {}'.format(high_intro, past, str_first_high)
        else:
            if second_high.time() > now.time():
                high_msg = '{} {} {}'.format(high_intro, future, str_second_high)
            else:
                high_msg = '{} {} {}'.format(high_intro, past, str_second_high)

    return '. '.join([low_msg, high_msg])
