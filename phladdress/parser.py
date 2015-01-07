import re
from phladdress.data import DIRS, DIRS_STD, SUFFIXES, SUFFIXES_STD, UNIT_TYPES, UNIT_TYPES_STD, LONG_ORDINALS_STD, STREET_NAMES_WITH_SUFFIX, STREET_NAMES_WITH_DIR

# DEV
from phladdress.test.test_addrs import TEST_ADDRS


'''
NOTES
'''

# Handle these:
#	1 SOUTH ST
#	1 EAST SOUTH ST
#	101 S INDEPENDENCE MALL E
# 	41ST ST DR
#	1132 BIG ST REAR OFFICE

# TODO
	# intersections and PO boxes
	# expand high range nums
	# take non-addressable street names out of street_names_with_suffix (i.e. WHATEVER ST RAMP)
	# handle garbage at end
	# how should 41ST ST DR look in street_names_with_suffix?
	# extra credit: expand suffixes in street names (e.g. 41ST ST DR => 41ST STREET DR)


'''
REGEX
'''

intersection_re = re.compile('(?P<street_1>.*)(AND|&|AT|\+)(?P<street_2>)')
# street_num_re = re.compile('(?P<full>(?P<low>\w+( (?P<low_fractional>1/2))?)(-(?P<high>\w+( (?P<high_fractional>1/2))?))?)')
street_num_re = re.compile('(?P<full>(?P<low>\w+( 1/2)?)(-(?P<high>\w+( 1/2)?))?)')
# zip_re = re.compile('(?P<full>(?P<zip_5>\d{5})(-(?P<zip_4>\d{4}))?)$')


class Parser:

	'''
	UTILITY FUNCTIONS
	'''

	def lint(self, addr):
		'''
		Remove extraneous punctuation and whitespace
		'''

		addr = ' '.join(addr.split())
		addr = addr.replace('.', '')
		addr = addr.replace(',', '')
		addr = addr.upper()

		return addr


	def is_ordinal(self, test):
		# Short ordinal
		if test[:-2].isdigit() and test[-2:] in ['TH', 'ST', 'ND', 'RD']:
			return True

		# Long ordinal
		if test in LONG_ORDINALS_STD:
			return True

		return False


	def is_numeric(self, test):
		# Digit or ordinal
		if self.is_ordinal(test) or test.isdigit():
			return True

		# TODO: for better peformance this could return the numeral type so we don't have to check again

		return False


	def ordinalize(self, num):
		if not num.isdigit():
			raise Exception('Cannot ordinalize {}'.format(num))

		last_digit = num[-1]
		suffix = None

		if last_digit > 3:
			suffix = 'TH'
		elif last_digit == 1:
			suffix = 'ST'
		elif last_digit == 2:
			suffix = 'ND'
		elif last_digit== 3:
			suffix = 'RD'

		return num + suffix


	'''
	STANDARDIZE
	'''

	def standardize_ordinal_street_name(self, name):
		# Remove leading zeros
		name = name.lstrip('0')

		# Check LONG_ORDINAL dict
		if name in LONG_ORDINALS_STD:
			return LONG_ORDINALS_STD[name]

		return name


	def standardize_street_name(self, tokens):
		'''
		Standardize a street name
		Note: this take tokens instead of a string so we don't have to split.
		'''
		
		# Check for ordinal street
		if self.is_ordinal(tokens[0]):
			tokens[0] = self.standardize_ordinal_street_name(tokens[0])
		elif tokens[0].isdigit():
			tokens[0] = self.ordinalize(tokens[0])

		return ' '.join(tokens)


	def standardize_unit_num(self, unit_num):
		'''
		Handles ordinal unit nums
		'''

		# Strip leading zeros
		unit_num = unit_num.lstrip('0')

		# 1ST => 1
		if unit_num[:-2].isdigit():
			return unit_num[:-2]

		# FIRST => 1
		if unit_num in LONG_ORDINALS_STD:
			std = LONG_ORDINALS_STD[unit_num]
			return std[:-2]

		return unit_num


	'''
	PARSE
	'''

	def parse(self, input_addr):
		'''
		Parse an address string into standardized components. This only does line 1 for now.
		'''

		# Lint
		addr = self.lint(input_addr)

		# TODO: Determine address type
			# Street address
			# Intersection
			# PO Box


		'''
		STREET NUM
		'''

		# This returns a string for a single address or a dictionary for a range
		# TODO: this is kinda inconsistent, because it will parse out fractionals if it's a range but not otherwise
		# TODO: handle 1092 - 1100 RIDGE AVE
		street_num_comps = street_num_re.match(input_addr).groupdict()
		street_num_full = street_num_comps['full']
		street_num = street_num_comps if street_num_comps['high'] else street_num_full
		
		# Remove street num and tokenize
		addr = addr[len(street_num_full) + 1:]
		tokens = addr.split()


		'''
		PREDIR
		'''

		predir = None

		# Save the predir candidate so we can check later if it's a legit part of the street name
		predir_candidate = tokens[0]

		# Check if first token is a directional
		if predir_candidate in DIRS:
			predir = predir_candidate
			del tokens[0]


		'''
		UNIT
		'''

		# TODO: do we handle APTA, FL2?

		unit_type = None
		unit_num = None

		last_token = tokens[-1]
		second_to_last_token = tokens[-2] if len(tokens) >= 2 else None

		# Case: #18
		if last_token[0] == '#':
			unit_type = '#'
			unit_num = last_token[1:]
			del tokens[-1]

		# Case 1: FL 15
		elif second_to_last_token and second_to_last_token in UNIT_TYPES:
			unit_type = second_to_last_token
			unit_num = last_token
			del tokens[-2:]

		# Case 2: REAR or 15TH FLOOR or FIRST FLOOR
		elif last_token in UNIT_TYPES:
			unit_type = last_token
			del tokens[-1]

			# Check if preceding token is numeral
			if second_to_last_token and self.is_numeric(second_to_last_token):
				unit_num = second_to_last_token
				del tokens[-1]
				

		'''
		POSTDIR
		'''

		postdir = None

		# Check if first token is a directional
		if tokens[-1] in DIRS:
			postdir = tokens[-1]
			del tokens[-1]

		
		'''
		SUFFIX
		'''

		suffix = None

		# Check that remaining tokens aren't a protected street name
		name_has_suffix_test = ' '.join(tokens)
		name_has_suffix = name_has_suffix_test in STREET_NAMES_WITH_SUFFIX

		if not name_has_suffix and tokens[-1] in SUFFIXES:
			suffix = tokens[-1]
			del tokens[-1]


		'''
		STREET NAME
		'''

		# Predir precautions
		if predir:
			# If there are no tokens left, give up the predir
			if len(tokens) == 0:
				tokens = [predir]
				predir = None

			# Make sure the predir + remaining tokens aren't a protected name
			else:
				name_has_predir_tokens = [predir_candidate] + tokens
				name_has_predir_test = ' '.join(name_has_predir_tokens)
				name_has_predir = name_has_predir_test in STREET_NAMES_WITH_DIR

				if name_has_predir:
					tokens = name_has_predir_tokens
					predir = None


		'''
		STANDARDIZE
		'''

		# Predir
		predir = DIRS_STD[predir] if predir else None

		# Street name
		street_name = self.standardize_street_name(tokens)

		# Unit
		unit = None

		if unit_type:
			unit_type = UNIT_TYPES_STD[unit_type]

			if unit_num:
				unit_num = self.standardize_unit_num(unit_num)
				unit = ' '.join([unit_type, unit_num]) if unit_num else None

			else:
				unit = unit_type
				

		# Suffix
		suffix = SUFFIXES_STD[suffix] if suffix else None

		
		'''
		RETURN
		'''

		comps = {
			'street_num': street_num,
			'predir': predir,
			'street_name': street_name,
			'suffix': suffix,
			'postdir': postdir,
			'unit': unit
		}

		return comps


'''
TEST
'''

if __name__ == '__main__':
	parser = Parser()

	FIELDS = [
		'street_num',
		'predir',
		'street_name',
		'suffix',
		'postdir',
		'unit',
	]


	# JUST ONE

	# TEST = '12 41st St Dr'
	# print TEST
	# comps = parser.parse(TEST)
	# ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
	# print ordered
	# print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])	


	# MULTIPLE

	# for a_test in TEST_ADDRS:
	# 	print a_test
	# 	comps = parser.parse(a_test)
	# 	print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])
	# 	ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
	# 	print ordered
	# 	print


	# TIME

	# from datetime import datetime
	# start = datetime.now()
	# for i in range(0, 750000):
	# 	parser.parse('1234 MARKET ST 80TH FLOOR')
	# print 'Took {}'.format(datetime.now() - start)


	# 311 FILE
	path = "/Users/rmartin/Development/phladdress/meta/311addronly.csv"
	start = 1000
	stop = 1010
	i = 0
	with open(path) as f:
		import csv
		for row in csv.reader(f):
			row = row[0]
			if i < start:
				i += 1
				continue
			if stop < i:
				break
			print row
			comps = parser.parse(row)
			print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])
			ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
			print ordered
			print

			i += 1