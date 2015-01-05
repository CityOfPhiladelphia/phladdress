import re
from phladdress.data import DIRS, SUFFIXES, UNIT_TYPES, LONG_ORDINALS_STD

# DEV
from phladdress.test.test_addrs import TEST_ADDRS


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

		# addr = addr.strip()
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

	def is_numeral(self, test):
		# Digit or ordinal
		if test.isdigit() or self.is_ordinal(test):
			return True

		# TODO: for better peformance this could return the numeral type so we don't have to check again

		return False


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

		return tokens


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

		# Components to return
		comps = {}

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
		# TODO: this is kinda erratic, because it will parse out fractionals if it's a range but not otherwise
		# TODO: handle 1092 - 1100 RIDGE AVE
		street_num_comps = street_num_re.match(input_addr).groupdict()
		street_num_full = street_num_comps['full']
		comps['street_num'] = street_num_comps if street_num_comps['high'] else street_num_full
		
		# Remove street num and tokenize
		addr = addr[len(street_num_full) + 1:]
		tokens = addr.split()


		'''
		PREDIR
		'''

		predir = None

		# Check if first token is a directional
		if tokens[0] in DIRS:
			predir = tokens[0]
			del tokens[0]

		comps['predir'] = predir


		'''
		UNIT
		'''

		# TODO: #8

		unit_type = None
		unit_num = None

		# Get length of remaining tokens to make sure there are enough to hold a unit
		token_len = len(tokens)

		# Loop through unit types and compare to last two tokens
		# If a match is found, store values and drop the unit-related tokens

		# TODO: this might make more sense to do
		# if tokens[-2] in UNIT_TYPES
		# etc

		for a_unit_type in UNIT_TYPES:
			# Case 1: FL 15
			if token_len >= 2 and a_unit_type == tokens[-2]:
				unit_type = a_unit_type
				unit_num = tokens[-1]

				del tokens[-2:]
				break

			# Case 2: REAR or 15TH FLOOR or FIRST FLOOR
			if a_unit_type == tokens[-1]:
				unit_type = a_unit_type

				# Check if preceding token is a number or ordinal
				if self.is_numeral(tokens[-2]):
					unit_num = tokens[-2]

					del tokens[-2:]
					break

				del tokens[-1]
				break

		# comps['unit_type'] = unit_type
		# comps['unit_num'] = unit_num


		'''
		POSTDIR
		'''

		postdir = None

		# Check if first token is a directional
		if tokens[0] in DIRS:
			postdir = tokens[0]
			del tokens[0]

		comps['postdir'] = postdir


		
		'''
		SUFFIX
		'''

		suffix = None

		if tokens[-1] in SUFFIXES:
			suffix = tokens[-1]

			del tokens[-1]

		comps['suffix'] = suffix


		'''
		STREET NAME
		'''

		std_street_name_tokens = self.standardize_street_name(tokens)
		street_name = ' '.join(std_street_name_tokens)
		comps['street_name'] = street_name


		'''
		STANDARDIZE
		'''

		# Street name
		street_name = self.standardize_street_name(street_name)

		# Unit num
		if unit_num:
			unit_num = self.standardize_unit_num(unit_num)
		
		comps['unit'] = ' '.join([unit_type, unit_num]) if unit_num else None


		# 

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
	TEST = '1234 EIGHTH ST #008'

	print TEST
	comps = parser.parse(TEST)
	ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
	print ordered
	print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])	


	# VERBOSE

	# for a_test in TEST_ADDRS:
	# 	print a_test
	# 	comps = parser.parse(a_test)
	# 	ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
	# 	print ordered
	# 	print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])
	# 	print


	# TIME
	# from datetime import datetime
	# start = datetime.now()
	# for i in range(0, 750000):
	# 	parser.parse('1234 MARKET ST 08TH FL')
	# print 'Took {}'.format(datetime.now() - start)