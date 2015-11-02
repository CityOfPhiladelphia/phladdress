import re
# from difflib import SequenceMatcher
from phladdress.data import *

# DEV
import sys
from pprint import pprint
import logging

# TODO
	# Standardize #REAR to just REAR as suffix type
	# Should street_names_common have a column for suffix? So 1234 THE PARKWAY => 1234 BENJAMIN FRANKLIN PKWY
	# take non-addressable street names out of street_names_with_suffix (i.e. WHATEVER ST RAMP)
	# how should 41ST ST DR look in street_names_with_suffix?

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
street_name_re = re.compile('^\w+( \w+)*$')  # TODO: this is not mutually exclusive with po_box_re

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
		Remove punctuation and extra whitespace. Insert whitespace where needed.
		'''
		addr = addr.replace('#', '# ')
		addr = ' '.join(addr.split())
		addr = addr.replace('.', '')
		addr = addr.replace(',', '')
		addr = addr.upper()
		return addr

	def is_ordinal(self, test):
		''' Returns a tuple of True/False and the ordinal type '''
		# Short ordinal
		if test[:-2].isdigit() and test[-2:] in ['TH', 'ST', 'ND', 'RD']:
			return True, 'short_ord'		
		# Long ordinal
		elif test in LONG_ORDINALS_STD:
			return True, 'long_ord'
		return False, None

	def is_numeric(self, test):
		''' Returns a tuple of True/False and the numeral type '''
		# Ordinal
		ord_result, ord_type = self.is_ordinal(test)
		if ord_result is True:
			return ord_result, ord_type
		# Digit
		elif test.isdigit():
			return True, 'digit'
		return False, None 

	def ordinalize(self, num):
		if not num.isdigit():
			raise ValueError('Not a number: {}'.format(num))

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

	def reverse_enumerate(self, a_list):
		"""
		Returns a generator to traverse a list, with indexes, in reverse order
		"""
		for index in reversed(range(len(a_list))):
			yield index, a_list[index]

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
		unit_tokens = unit_num.split(' ')
		std_tokens = []
		
		for unit_token in unit_tokens:
			std_token = unit_token.lstrip('0')  # may not need this
			is_ord, ord_type = self.is_ordinal(std_token)
			if is_ord:
				if ord_type == 'long_ord':
					std_token = LONG_ORDINALS_STD[unit_token]
				else:
					std_token = std_token[:-2]
			std_tokens.append(std_token)

		std_unit_num = ' '.join(std_tokens)

		return std_unit_num
	

		# OLD METHOD

		# Strip leading zeros
		# unit_num = unit_num.lstrip('0')

		# if self.is_ordinal(unit_num):
		# 	# FIRST => 1
		# 	if unit_num in LONG_ORDINALS_STD:
		# 		std = LONG_ORDINALS_STD[unit_num]
		# 		return std[:-2]
		# 	# 1ST => 1
		# 	return unit_num[:-2]
		# return unit_num

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
		'''
		This returns a tuple of comps (dict) and a Boolean flag for whether
		the main parsing routine should null out the unit num and type.
		'''
		# logging.debug('\n** PARSE STREET **')
		# logging.debug('input_street: {}'.format(input_street))
		# logging.debug('unit_type: {}, unit_num: {}'.format(unit_type, unit_num))

		tokens = input_street.split(' ')
		assert len(tokens) > 0
		reset_unit = False
		
		'''
		PREDIR
		'''

		predir = None

		# Save the first token so we can check later if the predir is actually 
		# part of the street name
		predir_candidate = tokens[0]

		if predir_candidate in DIRS:
			# logging.debug('predir: {}'.format(predir_candidate))
			predir = predir_candidate
			del tokens[0]

		'''
		POSTDIR
		'''

		postdir = None

		# If there's a unit but no more tokens
		# Edge case: 124 S PIER
		if len(tokens) == 0 and unit_type is not None:
			# Give up unit type
			# logging.debug('no more tokens, give back unit: {}'.format( \
			# 	' '.join([unit_num, unit_type])))
			tokens = [unit_type]
			unit_type = None
			reset_unit = True

			if unit_num:
				tokens.append(unit_num)
				unit_num = None


		# Check if last token is a directional
		if tokens[-1] in DIRS:
			postdir = tokens[-1]
			del tokens[-1]

		'''
		SUFFIX
		'''

		suffix = None

		# Try last token
		# Problem: if there's junk on the end that has a suffix, this captures
		# it. Like 1 MARKET ST ENTER ON ALLEY
		# if tokens[-1] in SUFFIXES:
		# 	suffix = tokens[-1]
		# 	del tokens[-1]

		new_tokens = list(tokens)
		len_tokens = len(tokens)
		start_i = 1 if len_tokens > 1 else 0  # In case 
		for token_i in range(start_i, len_tokens):
			token = tokens[token_i]
			if token in SUFFIXES:
				# If it's part of a street name that contains a suffix and 
				# there's still one more token to parse as the suffix, skip.
				# Case: COBBS CREEK PKWY, CREEK is a suffix
				test = ' '.join(tokens[:token_i + 1])
				if test in STREET_NAMES_WITH_SUFFIX and len_tokens > \
					token_i + 1:
					# logging.debug('{} looks like a suffix but is part of {}' \
					# 	.format(token, test))
					continue
				else:
					# If there's any junk after the suffix, delete it.
					# Also clear out unit.
					# Case: 1 PINE ST ENTER AT REAR
					suffix = token
					# logging.debug('suffix: {}'.format(suffix))
					del new_tokens[token_i:]
					break
		tokens = new_tokens

		'''
		STREET NAME
		'''

		# Case: 1 E ST, E got parsed as predir, give up predir
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

		# TODO: should check suffix and postdir too?

		'''
		STANDARDIZE
		'''

		# Street name
		street_name = self.standardize_street_name(tokens)

		# Suffix
		if suffix:
			suffix = SUFFIXES_STD[suffix]

		# Predir
		if predir:
			predir = DIRS_STD[predir]

		# Postdir
		if postdir:
			postdir = DIRS_STD[postdir]

		# Apply street corrections. These fix common disagreements between
		# address sources, like JAMESTOWN AVE => JAMESTOWN ST.
		street_full = ' '.join([str(x) for x in [predir, street_name, suffix, postdir] if x])
		if street_full in CORRECTIONS:
			incorrect_street_full = street_full
			correction = CORRECTIONS[street_full]
			predir = correction['TO_PREDIR']
			street_name = correction['TO_NAME']
			suffix = correction['TO_SUFFIX']
			postdir = correction['TO_POSTDIR']
			street_full = ' '.join([str(x) for x in [predir, street_name, suffix, postdir] if x])

		# Remove unnecessary predir
		if predir:
			if suffix:
				# Make sure it's a predir street
				street_base = ' '.join([street_name, suffix])
				if street_base in STREETS_WITH_PREDIR:
					predir = DIRS_STD[predir]
				else:
					# logging.debug('removing unnecessary predir: {}'.format(predir))
					predir = None

		# Remove unnecessary postdir
		if postdir:
			# Make sure it's a postdir street
			# matches = [x for x in STREETS_WITH_POSTDIR if x['street_name'] == street_name and x['street_suffix'] == suffix]
			# if len(matches) > 0:
			street_base = '{} {}'.format(street_name, suffix)
			if street_base in STREETS_WITH_POSTDIR:
				postdir = DIRS_STD[postdir]
			else:
				# logging.debug('removing unnecessary postdir: {}'.format(postdir))
				postdir = None


		street_full = ' '.join([str(x) for x in [predir, street_name, suffix, postdir] if x])
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

					# If high num is same as low num (e.g. 826-26 N 3RD ST),
					# remove and re-parse.
					if high_full == int(low):
						street_num_full = street_num_comps['full']
						street_num_no_high = street_num_full[:street_num_full.find('-')]
						street_num_search = street_num_re.search(street_num_no_high)
						street_num_comps = street_num_search.groupdict()					
				else:
					high_full = int(high)

				# Return ints
				if street_num_comps['high_num']:
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

		# logging.debug('** PARSE UNIT **')
		# logging.debug('tokens: {}'.format(tokens))

		unit_num = None
		unit_type = None

		len_tokens = len(tokens)
		new_tokens = list(tokens)

		# Start at 1 so we don't swallow up street name tokens
		# (We only want to take a unit if there's something left for the street)
		for token_i in range(1, len_tokens):
			token = tokens[token_i]
			if token in UNIT_TYPES:
				if token == '#':
					next_token_i = token_i + 1

					# Case: 1 PINE ST # (pound is junk, no more tokens left)
					if next_token_i == len_tokens:
						del new_tokens[token_i]
						break

					next_token = tokens[next_token_i]

					next_next_token_i = next_token_i + 1
					next_next_token = tokens[next_next_token_i] if len_tokens > next_next_token_i else None

					# Case: # APT 1
					if next_token in UNIT_TYPES:
						# logging.debug('unit pattern: # UNIT (1)')
						unit_type = next_token
						unit_num = ' '.join(tokens[next_token_i + 1:])
						del new_tokens[token_i:]
					# Case: # 1ST FL, # 1 FL, # 1ST FL REAR
					elif self.is_numeric(next_token)[0] and \
						next_next_token is not None and \
						next_next_token in UNIT_TYPES:
						# logging.debug('unit pattern: # 1ST FL')
						unit_type = next_next_token
						del new_tokens[next_next_token_i]
						unit_num = ' '.join(new_tokens[next_token_i:])

					# Case: # 2, # 2 A
					else:
						# logging.debug('unit pattern: # 1')
						unit_type = '#'
						unit_num = ' '.join(tokens[next_token_i:])
						del new_tokens[token_i:]

				# It's a unit type other than #
				else:
					# If it has a suffix after, keep going
					# Edge cases: 1 FRONT ST, 1 APARTMENT DR
					next_token_i = token_i + 1
					if len_tokens > next_token_i:
						next_token = tokens[next_token_i]
						if next_token in SUFFIXES:
							# logging.debug("skipping {} because {} is a suffix".format(token, next_token))
							continue

					# If we're at least on the second token (so token_i doesn't end up -1)
					if token_i > 0:
						# Check the previous token to see if it's numeric
						prev_token_i = token_i - 1
						prev_token = tokens[prev_token_i]

						# Case: 2ND FLOOR or 2ND FLOOR REAR
						if self.is_numeric(prev_token)[0]:
							# logging.debug('unit pattern: 2ND FLOOR')
							unit_type = token
							remaining_tokens = [prev_token] + tokens[token_i + 1:]
							unit_num = ' '.join(remaining_tokens)
							del new_tokens[prev_token_i:]

					# Case: APT 1
					if unit_num is None:
						# logging.debug('unit pattern: UNIT (1)')
						unit_type = token
						remaining_tokens = tokens[token_i + 1:]
						unit_num = ' '.join(remaining_tokens)
						del new_tokens[token_i:]

				break

		# logging.debug('unit_type: {}, unit_num: {}'.format(unit_type, unit_num))
		tokens = new_tokens

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
				unit_num = self.standardize_unit_num(unit_num)
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


if __name__ == '__main__':
	# LOGGING_LEVEL = logging.DEBUG
	# logging.basicConfig(level=LOGGING_LEVEL, format='%(message)s')

	from phladdress.tests import parser_tests
	parser_tests.run_tests()

	###############################################
	# TO CREATE UNIT TESTS
	###############################################
	# parser = Parser()
	# parsed = parser.parse('834 CHESTNUT ST # PH 108')
	# import json
	# print(json.dumps(parsed, sort_keys=True, indent='\t').replace('"', '\'').replace('null', 'None'))
