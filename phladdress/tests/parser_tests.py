from phladdress.parser import Parser
from phladdress.tests.test_addresses import TEST_ADDRESSES

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

TOP_LEVEL_COMPS = {
	'address': 			['address', 'street', 'unit',],
	'intersection': 	['street_1', 'street_2',],
}

def run_tests():
	parser = Parser()

	for test_address in TEST_ADDRESSES:
		input_address = test_address['input']
		# print('\n' + input_address)
		expected = test_address['expected_results']
		parsed = parser.parse(input_address)
		parsed_address = parsed['standardized_address']
		from_to = '{} => {}'.format(input_address, parsed_address)
		parsed_type = parsed['type']
		dots = '.' * (75 - len(from_to))
		status = 'OK'

		if expected == parsed:
			line_out = '{} => {} {} OK'.format(input_address, parsed_address, \
				dots)
			print(line_out)
			continue
			
		# Handle diffs
		line_out = '{} => {} {} FAILED'.format(input_address, parsed_address, \
			dots)
		print(line_out)

		diffs = DictDiffer(expected, parsed).changed()
		diffs_comps = DictDiffer(expected['components'], \
			parsed['components']).changed()

		if len(diffs) > 0:
			diffs = [x for x in diffs if x != 'components']
			for comp_set in TOP_LEVEL_COMPS[parsed_type]:
				comp_diffs = DictDiffer(
					parsed['components'][comp_set],
					expected['components'][comp_set]
				)
				for comp_diff in comp_diffs.changed():
					diffs.append('{}.{}: {}'.format(comp_set, comp_diff, parsed['components'][comp_set][comp_diff]))

		# Check standardized manually, since it's not in a top level comp
		if expected['standardized_address'] != \
			parsed['standardized_address']:
			diffs.append('standardized_address')

		for diff in diffs:
			print('    - {}'.format(diff))

if __name__ == '__main__':
	run_tests()