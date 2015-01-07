import csv

DIRS_STD = {
	'N': 'N',
	'NO': 'N',
	'NORTH': 'N',
	'S': 'S',
	'SO': 'S',
	'SOUTH': 'S',
	'E': 'E',
	'EAST': 'E',
	'W': 'W',
	'WEST': 'W'
}

DIRS = set(DIRS_STD.keys())


LONG_ORDINALS_STD = {
	'FIRST': '1ST',
	'SECOND': '2ND',
	'THIRD': '3RD',
	'FOURTH': '4TH',
	'FIFTH': '5TH',
	'SIXTH': '6TH',
	'SEVENTH': '7TH',
	'EIGHTH': '8TH',
	'NINTH': '9TH',
	'TENTH': '10TH',
	'ELEVENTH': '11TH',
	'TWELFTH': '12TH',
	'THIRTEENTH': '13TH',
	'FOURTEENTH': '14TH',
	'FIFTEENTH': '15TH',
	'SIXTEENTH': '16TH',
	'SEVENTEENTH': '17TH',
	'EIGHTEENTH': '18TH',
	'NINETEENTH': '19TH',
	'TWENTIETH': '20TH',
}


'''
STREET NAMES
'''

with open('./data/street_names_with_suffix.csv') as f:
	reader = csv.DictReader(f)
	STREET_NAMES_WITH_SUFFIX = set([x['STREET_NAME'] for x in reader])

with open('./data/street_names_with_dir.csv') as f:
	reader = csv.DictReader(f)
	STREET_NAMES_WITH_DIR = set([x['STREET_NAME'] for x in reader])


'''
SUFFIXES
'''

# Make suffix lists
with open('./data/suffixes.csv') as f:
	reader = csv.DictReader(f)

	# Dict to convert common suffixes to standard
	SUFFIXES_STD = {x['COMMON']: x['STANDARD'] for x in reader}

	# Set to look up suffixes
	SUFFIXES = set(SUFFIXES_STD.keys())


'''
UNIT TYPES
'''

with open('./data/unit_types.csv') as f:
	reader = csv.DictReader(f)

	# Dict to convert common unit types to standard
	UNIT_TYPES_STD = {x['COMMON']: x['STANDARD'] for x in reader}

	# Set to look up unit types
	UNIT_TYPES = set(UNIT_TYPES_STD.keys())