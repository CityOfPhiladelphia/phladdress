from phladdress.parser import Parser
from datetime import datetime

TIMES = 600000
TEST_ADDRESS = '123456 WEST BOB JONES DRIVE SOUTH # 5'

start = datetime.now()
parser = Parser()

for i in range(0, TIMES):
	# if i % 20000 == 0:
		# print(i)
	parser.parse(TEST_ADDRESS)

duration = datetime.now() - start
print('Took {} seconds'.format(duration))