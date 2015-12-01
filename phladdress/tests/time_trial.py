from phladdress.parser import Parser
from datetime import datetime

TIMES = 500000
TEST_ADDRESS = '1234-36 MARKET ST'

start = datetime.now()
parser = Parser()

for i in range(0, TIMES):
	# if i % 20000 == 0:
		# print(i)
	parser.parse(TEST_ADDRESS)

duration = datetime.now() - start
print('Took {} seconds'.format(duration))