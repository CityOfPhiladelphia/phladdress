import csv
import os

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

'''
ORDINALS
'''

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

# with open('./data/street_names_with_suffix.csv') as f:
with open(os.path.join(os.path.dirname(__file__), './data/street_names_with_suffix.csv')) as f:
	reader = csv.DictReader(f)
	STREET_NAMES_WITH_SUFFIX = set([x['STREET_NAME'] for x in reader])

with open(os.path.join(os.path.dirname(__file__), './data/street_names_with_dir.csv')) as f:
	reader = csv.DictReader(f)
	STREET_NAMES_WITH_DIR = set([x['STREET_NAME'] for x in reader])

# Common abbreviations
ABBRS_STD = {
	'AVE': 'AVENUE',
	'CRK': 'CREEK',
	'CTR': 'CENTER',
	'MT': 'MOUNT',
	# 'PK': 'PARK',			# This is widely used for PIKE
}

ABBRS = set(ABBRS_STD.keys())

SAINTS_STD = {
	# Base name => standardized name
	'ALBAN': 'ALBANS',
	'ANDREW': 'ANDREW',
	'BERNARD': 'BERNARD',
	'CHARLES': 'CHARLES',
	'CHRISTOPHER': 'CHRISTOPHER',
	'DAVID': 'DAVIDS',
	'DENIS': 'DENIS',
	'GEORGE': 'GEORGES',
	'JAMES': 'JAMES',
	# 'JOHN': 'JOHN',
	'JOHN NEUMANN': 'JOHN NEUMANN',
	'JOSEPH': 'JOSEPHS',
	'LUKE': 'LUKES',
	'MALACHY': 'MALACHYS',
	'MARK': 'MARKS',
	'MARTIN': 'MARTINS',
	'MICHAEL': 'MICHAEL',
	'PAUL': 'PAUL',
	'PETER': 'PETERS',
	'THOMAS': 'THOMAS',
	'VINCENT': 'VINCENT',
}

SAINTS = set(SAINTS_STD.keys())

# Street name common
# This includes common nicknames and spelling errors
with open(os.path.join(os.path.dirname(__file__), './data/street_names_common.csv')) as f:
	reader = csv.DictReader(f)
	STREET_NAMES_COMMON_STD = {x['COMMON']: x['STANDARD'] for x in reader}

STREET_NAMES_COMMON = set(STREET_NAMES_COMMON_STD.keys())

# Postdir streets
with open(os.path.join(os.path.dirname(__file__), './data/streets_with_predir.csv')) as f:
	reader = csv.DictReader(f)
	STREETS_WITH_PREDIR = set(['{} {}'.format(x['street_name'], x['street_suffix']) for x in reader])

# Postdir streets
with open(os.path.join(os.path.dirname(__file__), './data/streets_with_postdir.csv')) as f:
	reader = csv.DictReader(f)
	STREETS_WITH_POSTDIR = set(['{} {}'.format(x['street_name'], x['street_suffix']) for x in reader])

'''
SUFFIXES
'''

# Make suffix lists
with open(os.path.join(os.path.dirname(__file__), './data/suffixes.csv')) as f:
	reader = csv.DictReader(f)

	# Dict to convert common suffixes to standard
	SUFFIXES_STD = {x['COMMON']: x['STANDARD'] for x in reader}

	# Set to look up suffixes
	SUFFIXES = set(SUFFIXES_STD.keys())

'''
UNIT TYPES
'''

with open(os.path.join(os.path.dirname(__file__), './data/unit_types.csv')) as f:
	reader = csv.DictReader(f)

	# Dict to convert common unit types to standard
	UNIT_TYPES_STD = {x['COMMON']: x['STANDARD'] for x in reader}

	# Set to look up unit types
	UNIT_TYPES = set(UNIT_TYPES_STD.keys())

'''
CORRECTIONS

These resolve common disagreements between address sources. For example, OPA 
uses JAMESTOWN ST whereas Streets calls it JAMESTOWN AVE. We standardize to 
one or the other.
'''

with open(os.path.join(os.path.dirname(__file__), './data/street_corrections.csv')) as f:
	reader = csv.DictReader(f)
	street_full_attrs = ['FROM_PREDIR', 'FROM_NAME', 'FROM_SUFFIX', 'FROM_POSTDIR']
	CORRECTIONS = {}

	for row in reader:
		street_full = ' '.join([row[x] for x in street_full_attrs if row[x]])
		if street_full in CORRECTIONS:
			raise ValueError('Duplicate street correction entry')
		CORRECTIONS[street_full] = {x: row[x] for x in ['TO_PREDIR', 'TO_NAME', 'TO_SUFFIX', 'TO_POSTDIR']}
