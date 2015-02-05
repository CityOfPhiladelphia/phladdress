import csv
from fuzzywuzzy import fuzz
from phladdress.parser import Parser

print 'Starting...'

IN_FILE = 'C:/temp/li_addrs.csv'
OUT_FILE = 'C:/temp/compute_similarity_out.csv'
parser = Parser()



with open(IN_FILE) as f, open(OUT_FILE, 'w+') as f_out:
# with open(IN_FILE) as f:
	f_out.write('TEST_ADDR,STD_ADDR,SIMILARITY\n')

	r = csv.reader(f)
	r.next()
	i = 2
	# TARGET_LINE = 570000

	for row in r:
		
		# if i == 10:
		# 	break

		# if i < TARGET_LINE:
		# 	i += 1
		# 	continue

		test_addr = row[0]

		try:
			result = parser.parse(test_addr)
		except:
			print 'line {}'.format(i)
			print test_addr
			import traceback
			print traceback.format_exc()
			break

		# if i == TARGET_LINE:
		# 	print str(i) + ': ' + test_addr + ' ==> ' + result['full_address']
		# 	break

		# if i % 10000 == 0:
		# 	print str(i) + ': ' + test_addr + ' ==> ' + result['full_address']

		# Compute similarity
		full_addr = result['full_address']

		test_addr_clean = ' '.join(test_addr.split())
		test_addr_clean = test_addr_clean.lstrip('0')
		sim = fuzz.ratio(test_addr_clean, full_addr)
		f_out.write(','.join([str(x) for x in test_addr, full_addr, sim]) + '\n') 

		i += 1