DIRS = [
	'N',
	'NO',
	'NORTH',
	'S',
	'SO',
	'SOUTH',
	'E',
	'EAST',
	'W',
	'WEST',
]


UNIT_TYPES = [
	'#',
	'APT',
	'FL',
	'FLOOR',
	'UNIT',
	'BSMT',
	'LOBBY',
	'REAR',
]


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

# Make list of street names that have a token from SUFFIXES_ALL
	# Loop over distinct street names
		# Split into tokens
		# Loop over tokens
			# If token in SUFFIXES ALL
				# Add to watch list

# List of streets that have a dir in the name?


'''
SUFFIXES
'''

# Load suffixes from JSON
# Create
	# List of all suffixes (std + common)			SUFFIXES_ALL
	# Dict of all suffixes => std 					SUFFIXES_STD_DICT