import re
# from difflib import SequenceMatcher
from phladdress.data import *

# DEV
import sys
from pprint import pprint
# from phladdress.test.test_addrs import TEST_ADDRS

'''
NOTES
'''

# TODO
	# Standardize #REAR to just REAR as suffix type
	# Should street_names_common have a column for suffix? So 1234 THE PARKWAY => 1234 BENJAMIN FRANKLIN PKWY
	# take non-addressable street names out of street_names_with_suffix (i.e. WHATEVER ST RAMP)
	# how should 41ST ST DR look in street_names_with_suffix?
	# Restructure common name routine so we can convert AYRDALECRESCENT ST => AYRDALE CRESCENT

'''
SET UP
'''

# Street num
# low_num_pat = '(?P<low>(?P<low_num>\d+)(?P<low_suffix>[A-Z]?(?![\w]))(( )(?P<low_fractional>1/2))?)'
low_num_pat = '(?P<low>(?P<low_num>\d+)-?(?P<low_suffix>[A-Z]?(?![\w]))(( )(?P<low_fractional>1/2))?)'
hyphen_pat = '((?<= )?-(?= )?)?'
high_num_pat = '(?P<high>(?P<high_num>\d+)(?P<high_suffix>[A-Z]?(?![\w]))(( )(?P<high_fractional>1/2))?)?'
street_num_pat = '^(0+)?(?P<full>' + low_num_pat + hyphen_pat + high_num_pat + ')'
street_num_re = re.compile(street_num_pat)
street_num_fields = ['full', 'low', 'low_num', 'low_suffix', 'low_fractional', \
	'high', 'high_num', 'high_num_full', 'high_suffix', 'high_fractional']

# Address type regex
single_address_re = re.compile('^\d+\w?(-\w+)?( \d/\d)?( .+)+$')
intersection_pat = '^(?P<street_1>[A-Z0-9 ]+)( AND | ?& ?| ?\+ ?| AT )(?P<street_2>[A-Z0-9 ]+)$'
intersection_re = re.compile(intersection_pat)
po_box_re = re.compile('^P(\.|OST)? ?O(\.|FFICE)? ?BOX (?P<num>\w+)$')
street_name_re = re.compile('^\w+( \w+)+$')  # TODO: this is not mutually exclusive with po_box_re

# Misc
# zip_re = re.compile('(?P<full>(?P<zip_5>\d{5})(-(?P<zip_4>\d{4}))?)$')
saints_re = re.compile('^(ST|SAINT) ({})'.format('|'.join(SAINTS)))


'''
PARSER
'''

class Parser:
	'''
	UTILITY FUNCTIONS
	'''

	def lint(self, addr):
		'''
		Remove punctuation and extra whitespace
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

	def calculate_similarity(self, a, b):
	    return SequenceMatcher(None, a, b).ratio()

	def parity(self, num):
		try:
			if num % 2 == 0:
				return 'E'
			return 'O'
		except:
			raise Exception('Not a number: {}').format(num)

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
		Note: this takes tokens and returns a string
		'''
		first_token = tokens[0]
		
		# Check for ordinals
		if self.is_ordinal(first_token):
			tokens[0] = self.standardize_ordinal_street_name(first_token)
		elif first_token.isdigit():
			tokens[0] = self.ordinalize(first_token)
		# Check for abbreviations
		for i, token in enumerate(tokens):
			if token in ABBRS:
				tokens[i] = ABBRS_STD[token]

		# Checks after this use the concatenated string
		street_name = ' '.join(tokens)
		# Check for common name
		if street_name in STREET_NAMES_COMMON:
			street_name = STREET_NAMES_COMMON_STD[street_name]

		# Check for saint
		saint_comps = saints_re.match(street_name)
		if saint_comps:
			saint = saint_comps.group(2)
			saint = SAINTS_STD[saint]
			street_name = 'SAINT {}'.format(saint)

		return street_name

	def standardize_unit_num(self, unit_num):
		'''
		Handles ordinal unit nums
		'''
		# Strip leading zeros
		unit_num = unit_num.lstrip('0')

		if self.is_ordinal(unit_num):
			# FIRST => 1
			if unit_num in LONG_ORDINALS_STD:
				std = LONG_ORDINALS_STD[unit_num]
				return std[:-2]
			# 1ST => 1
			return unit_num[:-2]
		return unit_num

	'''
	PARSING
	'''

	def parse(self, input_addr):
		'''
		Parse an address string into standardized components. This only does line 1 for now.
		'''
		# Validate input
		if input_addr in (None, ''):
			raise ValueError('No address')
		addr = self.lint(input_addr)

		# Address type: single address, range, P.O. box, or intersection
		addr_type = None
		
		# Check type
		if single_address_re.search(addr):
			comps = self.parse_single_address(addr)
			return {
				'input_address': input_addr,
				'standardized_address': comps['street_address'],
				'components': comps,
				'type': 'address'
			}
		
		intersection_search = intersection_re.search(addr)
		if intersection_search:
			# return self.parse_intersection(intersection_search)
			street_1_comps = self.parse_street(intersection_search.group('street_1'))
			street_2_comps = self.parse_street(intersection_search.group('street_2'))
			return {
				'input_address': input_addr,
				'standardized_address': input_addr,
				'components': {
					'street_1': street_1_comps,
					'street_2': street_2_comps
				},
				'type': 'intersection',
			}
		
		po_box_search = po_box_re.search(addr)
		if po_box_search:
			std = self.parse_po_box(addr)
			return {
				'input_address': input_addr,
				'standardized_address': std,
				'type': 'po box'
			}

		if street_name_re.search(addr):
			comps = self.parse_street(addr)[0]
			return {
				'input_address': input_addr,
				'standardized_address': comps['full'],
				'components': comps,
				'type': 'street'
			}

		raise ValueError('Address format not recognized: {}'.format(addr))

	def parse_street(self, input_street, unit_type=None, unit_num=None):
		tokens = input_street.split(' ')
		
		# If there's a unit num, make sure it isn't actually the suffix
		# (e.g. 101 GREENHILL APARTMENT DR => 101 GREENHILL APT DR)
		input_unit_type = unit_type
		input_unit_num = unit_num

		if unit_num and unit_num in SUFFIXES:
			suffix = unit_num
			# tokens.append(unit_type)
			tokens += [unit_type, unit_num]
			unit_num = None
			unit_type = None
			reset_unit = True
		else:
			reset_unit = False

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
		POSTDIR
		'''

		postdir = None

		# If there are no tokens left
		if len(tokens) == 0:
			# But there's a unit type, we probably swallowed it by mistake and
			# it's actually the street name
			if unit_type:
				tokens = [unit_type]
				unit_type = None
				reset_unit = True

				if unit_num:
					tokens.append(unit_num)
					unit_num = None

		# Check if first token is a directional
		if tokens[-1] in DIRS:
			postdir = tokens[-1]
			del tokens[-1]

		'''
		SUFFIX
		'''

		suffix = None

		if len(tokens) == 0:
			# TODO: not sure if this will happen, but handle it gracefullish
			raise

		# Approach 1: just parse it
		if tokens[-1] in SUFFIXES:
			suffix = tokens[-1]
			del tokens[-1]

		# Edge case: GREENHILL APARTMENT DR. Don't capture APT DR as a unit.
		# elif unit_num and unit_num in SUFFIXES:
		# 	suffix = unit_num
		# 	tokens.append(unit_type)
		# 	unit_num = None
		# 	unit_type = None

		# Edge case: 1701 JOHN F KENNEDY BLVD COMCAST CENTER
		# Start at the second token and find the first suffix. Everything after
		# that is probably garbage. CENTER is not currently a suffix but is
		# USPS-valid.
		# We start at the second token because: 1901 AVENUE OF THE ARTS
		if suffix is None and len(tokens) > 1:
			for i in range(1, len(tokens) - 2):
				token = tokens[i]
				if token in SUFFIXES and ' '.join(tokens[:i + 1]) not in STREET_NAMES_WITH_SUFFIX:
					suffix = token
					del tokens[i:]
					break

		# Approach 2: check for suffix in name
		# TODO: this is capturing the AVE of 7015 RIDGE AVE as part of the street name
		# because there's a RIDGE AVE RAMP or something.

		# Check that remaining tokens aren't a protected street name
		# name_has_suffix_test = ' '.join(tokens)
		# name_has_suffix = name_has_suffix_test in STREET_NAMES_WITH_SUFFIX

		# if not name_has_suffix and tokens[-1] in SUFFIXES:
		# 	suffix = tokens[-1]
		# 	del tokens[-1]

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

		# TODO: should check suffix and postdir too, right?

		'''
		STANDARDIZE
		'''

		street_name = self.standardize_street_name(tokens)

		# Suffix
		if suffix:
			suffix = SUFFIXES_STD[suffix]

		# Predir
		if predir:
			if suffix:
				# Make sure it's a predir street
				street_base = ' '.join([street_name, suffix])
				if street_base in STREETS_WITH_PREDIR:
					predir = DIRS_STD[predir]
				else:
					predir = None

		# Postdir
		if postdir:
			# Make sure it's a postdir street
			# matches = [x for x in STREETS_WITH_POSTDIR if x['street_name'] == street_name and x['street_suffix'] == suffix]
			# if len(matches) > 0:
			street_base = '{} {}'.format(street_name, suffix)
			if street_base in STREETS_WITH_POSTDIR:
				postdir = DIRS_STD[postdir]
			else:
				postdir = None


		street_full_comps = [predir, street_name, suffix, postdir]
		street_full = ' '.join([str(comp) for comp in street_full_comps if comp])
		comps = {
			'predir': predir,
			'name': street_name,
			'suffix': suffix,
			'postdir': postdir,
			'full': street_full
		}

		return comps, reset_unit

	def parse_single_address(self, addr):
		'''
		STREET NUM
		'''

		# Returns a dict of primary address components
		street_num_search = street_num_re.search(addr)
		street_num = None

		# Check if there's a street num
		if street_num_search:
			street_num_comps = street_num_search.groupdict()

			# Single address
			if not street_num_comps['high']:
				addr_type = 'single'
				street_num_comps['high_num_full'] = None
			# Range
			else:
				addr_type = 'range'
				low = street_num_comps['low_num']
				high = street_num_comps['high_num']
				len_high = len(high)

				# Expand high num to full number (100-3 MAIN ST => 103)
				high_full = None

				if len_high <= len(low):
					high_full = int(low[:-len_high] + high)
					
					# if high_full < low:
					# 	raise Exception('Invalid address range: {}'.format(street_num))
				else:
					high_full = int(high)

				# Return ints
				street_num_comps['high_num'] = int(street_num_comps['high_num'])
				street_num_comps['high_num_full'] = high_full

			# Make low num an integer
			street_num_comps['low_num'] = int(street_num_comps['low_num'])

			# Get parity
			street_num_comps['low_parity'] = self.parity(street_num_comps['low_num'])
			street_num_comps['high_parity'] = self.parity(street_num_comps['high_num']) if street_num_comps['high_num'] else None

			# Edge case: 281-A HERMITAGE ST in PWD parcels
			if '-' in street_num_comps['low']:
				street_num_comps['low'] = street_num_comps['low'].replace('-', '')
				street_num_comps['full'] = street_num_comps['full'].replace('-', '')
			
			street_num = street_num_comps['full']

			# Remove street num
			addr = street_num_re.sub('', addr)[1:]

		# If there's no address (i.e. PO boxes), return None for all fields
		else:
			# street_num_comps = {field: None for field in street_num_fields}
			raise  # We shouldn't need this handler anymore

		# Tokenize
		tokens = addr.split()

		'''
		UNIT
		'''

		unit_type = None
		unit_num = None

		len_tokens = len(tokens)
		last_token = tokens[-1] if len_tokens >= 2 else None

		if last_token:
			# Only take the second-to-last token if there at least 3 tokens total (test case: 1 FRONT ST)
			second_to_last_token = tokens[-2] if len(tokens) >= 3 else None

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
		STREET
		'''

		street_comps, reset_unit = self.parse_street(' '.join(tokens), \
			unit_type=unit_type, unit_num=unit_num)
		if reset_unit:
			unit_num = None
			unit_type = None

		'''
		STANDARDIZE
		'''

		# Unit
		if unit_type:
			unit_type = UNIT_TYPES_STD[unit_type]

			if unit_num:
				# unit_num = self.standardize_unit_num(unit_num)
				unit = ' '.join([unit_type, unit_num]) if unit_num else None

			else:
				unit = unit_type

		'''
		RETURN
		'''

		predir = street_comps['predir']
		street_name = street_comps['name']
		suffix = street_comps['suffix']
		postdir = street_comps['postdir']

		# Concatenate comps
		unit_comps = {
			'type': unit_type,
			'num': unit_num,
		}

		full_addr_comps = [street_num, predir, street_name, suffix, postdir, unit_type, unit_num]
		full_addr = ' '.join([str(comp) for comp in full_addr_comps if comp])

		# Get similarity
		# similarity = self.calculate_similarity(input_addr, full_addr)
		# similarity = round(similarity, 2)

		return {
			'street_address': full_addr,
			'address': street_num_comps,
			'street': street_comps,
			'unit': unit_comps,
		}

	def parse_po_box(self, input_addr):
		search = po_box_re.search(input_addr)
		num = search.group('num')
		return 'PO BOX {}'.format(num)

'''
TEST
'''

if __name__ == '__main__':
	parser = Parser()

	# test = [
	# 	'BRANDYWINE ST',
	# 	# '281-A HERMITAGE ST',
	# 	# '281-83 HERMITAGE ST',
	# 	# '281-A HERMITAGE ST',
	# 	# '1415-17 S ORIANNA',
	# 	# '2800 S 20TH ST',
	# 	# '792 S FRONT ST',
	# 	# '1 COBBS CREEK PKWY',
	# 	# 'COBBS CREEK PKWY & LOCUST',
	# 	# 'POST OFFICE BOX 213',
	# 	# 'NORTH 23RD ST'
	# ]
	# for a_test in test:
	# 	print(a_test)
	# 	comps = parser.parse(a_test)
	# 	print(pprint(comps))
	# 	print()

	# MULTIPLE

	# for a_test in TEST_ADDRS:
	# 	print a_test
	# 	comps = parser.parse(a_test)
	# 	print ' '.join([str(comps[x]) for x in FIELDS if comps[x]])
	# 	ordered = ', '.join([str(x) + ': ' + str(comps[x]) for x in FIELDS if comps[x]])
	# 	print ordered
	# 	print


	# TIME TRIAL

	# from datetime import datetime
	# start = datetime.now()
	# for i in range(0, 650000):
	# 	parser.parse('00717  S CHRIS COLUMBUS BLV #407')
	# print('Took {}'.format(datetime.now() - start))


	# 311 FILE

	# path = "/Users/rmartin/Development/phladdress/meta/311addronly.csv"
	# start = 2000
	# num = 10
	# i = 0
	# with open(path) as f:
	# 	end = start + num
	# 	import csv
	# 	for row in csv.reader(f):
	# 		row = row[0]
	# 		if i < start:
	# 			i += 1
	# 			continue
	# 		if end < i:
	# 			break
	# 		print row
	# 		comps = parser.parse(row)
	# 		print comps['full_address']
	# 		print comps
	# 		print

	# 		i += 1


	# TIME 311

	# path = "/Users/rmartin/Development/phladdress/meta/311addronly.csv"
	# from datetime import datetime
	# import csv
	# start = datetime.now()

	# errors = 0
	# count = 0

	# with open(path) as f:
	# 	reader = csv.reader(f)
	# 	reader.next()

	# 	for row in csv.reader(f):
	# 		try:
	# 			row = row[0]
	# 			results = parser.parse(row)
	# 		except:
	# 			errors += 1
	# 			# import traceback
	# 			# print traceback.format_exc()
	# 			# raise
	# 		finally:
	# 			count += 1

	# print 'Took {}'.format(datetime.now() - start)
	# print errors, 'errors'
	# print "processed {} rows".format(count)
