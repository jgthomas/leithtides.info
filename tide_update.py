

import re
import json
import feedparser

from constants import URL, TIDE_FILE


HT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - High Tide')
LT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - Low Tide')


def save_to_json(filename, words):
    """ Save data to JSON file. """
    with open(filename, 'w') as outfile:
        json.dump(words, outfile)


def get_tide_times(url):
    tide = feedparser.parse(url)
    tide_data = tide['entries'][0]['summary']
    high_tide = re.findall(HT_MATCH, tide_data)
    low_tide = re.findall(LT_MATCH, tide_data)
    return (low_tide, high_tide)


def main():
    tides = get_tide_times(URL)
    save_to_json(TIDE_FILE, tides)


if __name__ == '__main__':

    main()
