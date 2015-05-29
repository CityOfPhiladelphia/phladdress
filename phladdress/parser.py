import re
from difflib import SequenceMatcher
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
	# intersections and PO boxes
	# take non-addressable street names out of street_names_with_suffix (i.e. WHATEVER ST RAMP)
	# handle garbage at end
	# how should 41ST ST DR look in street_names_with_suffix?
	# extra credit: expand suffixes in street names (e.g. 41ST ST DR => 41ST STREET DR)
	# expand words like CTR => CENTER?


'''
REGEX
'''

# Street num
# street_num_re = re.compile('(?P<full>(?P<low>[1-9](\w+)?( 1/2)?)(-(?P<high>\w+( 1/2)?))?)')
# street_num_re = re.compile('(?P<leading_zeros>0+)?(?P<full>(?P<low>\w+( (?P<low_fractional>1/2))?)(-(?P<high>\w+( (?P<high_fractional>1/2))?))?)')
low_num_pat = '(?P<low>(?P<low_num>\d+)(?P<low_suffix>[A-Z]?(?![\w]))(( )(?P<low_fractional>1/2))?)'
hyphen_pat = '((?<= )?-(?= )?)?'
high_num_pat = '(?P<high>(?P<high_num>\d+)(?P<high_suffix>[A-Z]?(?![\w]))(( )(?P<high_fractional>1/2))?)?'
street_num_pat = '^(0+)?(?P<full>' + low_num_pat + hyphen_pat + high_num_pat + ')'
street_num_re = re.compile(street_num_pat)

# Misc
intersection_re = re.compile('(?P<street_1>.*)(AND|&|AT)(?P<street_2>)')
# zip_re = re.compile('(?P<full>(?P<zip_5>\d{5})(-(?P<zip_4>\d{4}))?)$')
saints_re = re.compile('^(ST|SAINT) ({})'.format('|'.join(SAINTS)))


'''
PARSER
'''

class Parser:
	'Address parser'

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
	PARSE
	'''

	def parse(self, input_addr):
		'''
		Parse an address string into standardized components. This only does line 1 for now.
		'''

		# Lint
		addr = self.lint(input_addr)

		# Address type: single address, range, P.O. box, or intersection
		addr_type = None


		'''
		STREET NUM
		'''

		# Returns a dict of primary address components
		street_num_search = street_num_re.search(addr)
		street_num = None
		street_num_comps = None

		# Check if there's a street num
		if street_num_search:
			street_num_comps = street_num_search.groupdict()
			street_num = street_num_comps['full']

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

			# Remove street num
			addr = street_num_re.sub('', addr)[1:]

		# Tokenize
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

		# Approach 1: just parse it
		if tokens[-1] in SUFFIXES:
			suffix = tokens[-1]
			del tokens[-1]

		# Approach 2: check for suffix in name
		# TODO: this is capturing the AVE of 7015 RIDGE AVE as part of the street name

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

		# Predir
		predir = DIRS_STD[predir] if predir else None

		# Suffix
		suffix = SUFFIXES_STD[suffix] if suffix else None

		# Unit
		# unit = None

		if unit_type:
			unit_type = UNIT_TYPES_STD[unit_type]

			if unit_num:
				unit_num = self.standardize_unit_num(unit_num)
				unit = ' '.join([unit_type, unit_num]) if unit_num else None

			else:
				unit = unit_type
		
		# Street name
		street_name = self.standardize_street_name(tokens)

		# Postdir
		if postdir:
			# Make sure it's a postdir street
			matches = [x for x in STREETS_WITH_POSTDIR if x['street_name'] == street_name and x['suffix'] == suffix]
			if len(matches) > 0:
				postdir = DIRS_STD[postdir]
			else:
				postdir = None


		'''
		RETURN
		'''

		# Concatenate comps
		unit_comps = {
			'type': unit_type,
			'num': unit_num,
		}

		full_addr_comps = [street_num, predir, street_name, suffix, postdir, unit_type, unit_num]
		full_addr = ' '.join([str(comp) for comp in full_addr_comps if comp])

		street_full_comps = [predir, street_name, suffix, postdir]
		street_full = ' '.join([str(comp) for comp in street_full_comps if comp])
		street_full_comps = {
			'predir': predir,
			'name': street_name,
			'suffix': suffix,
			'postdir': postdir,
			'full': street_full
		}

		# Get similarity
		# similarity = self.calculate_similarity(input_addr, full_addr)
		# similarity = round(similarity, 2)

		comps = {
			'type': addr_type,
			'street_address': full_addr,
			'address': street_num_comps,
			'street': street_full_comps,
			'unit': unit_comps,
			# 'similarity': similarity,
		}

		return comps


'''
TEST
'''

# if __name__ == '__main__':
# 	parser = Parser()

	# test = [
	# 	'1310 ST ALBANS PL',
	# ]
	# for a_test in test:
	# 	print a_test
	# 	comps = parser.parse(a_test)
	# 	print pprint(comps)
	# 	print ''


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
	# for i in range(0, 500000):
	# 	parser.parse('00717  S CHRIS COLUMBUS BLV #407')
	# print 'Took {}'.format(datetime.now() - start)


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
