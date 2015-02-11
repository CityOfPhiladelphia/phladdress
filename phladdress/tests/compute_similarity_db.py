
from fuzzywuzzy import fuzz
from phladdress.parser import Parser

print 'Starting...'

# Set up parser
parser = Parser()

# Connect to DB
db = cx_Oracle.connect('gis_ulrs2/parcels2@gisexttst')
c = db.cursor()
# rows = c.execute('SELECT * FROM SNP_63TAXACCOUNTS')
rows = c.execute('SELECT * FROM SNP_37PWDACCOUNTS')

for i, row in enumerate(rows):
	# if i == 10:
	# 	break

	# Parse
	test_addr = row[1]
	try:
		comps = parser.parse(test_addr)
	except:
		print i, row

		import traceback
		print traceback.format_exc()
		break
	# full_addr = comps['full_address']
	
	# print '{} => {}'.format(test_addr.strip(), full_addr)





db.close()