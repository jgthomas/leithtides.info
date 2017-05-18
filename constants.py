
# Tide information source
URL = 'https://www.tidetimes.org.uk/leith-tide-times.rss'

# Matches low and high tide data
HT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - High Tide')
LT_MATCH = re.compile(r'([0-9][0-9]:[0-9][0-9]) - Low Tide')

TIDE_FILE = '/data/tide_times.json'
