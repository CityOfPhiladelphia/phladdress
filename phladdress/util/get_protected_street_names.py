import csv

DIRS = [
	'N',
	'NO',
	'NORTH',
	'S',
	'SO',
	'SOUTH',
	'E',
	'EAST',
	'W',
	'WEST',
]

with open('../data/st_name_distinct.csv') as f_names, open('../data/suffixes.csv') as f_suffixes:
	names_reader = csv.reader(f_names)
	next(names_reader, None)
	names = [row[0] for row in names_reader]

	suffix_reader = csv.reader(f_suffixes)
	next(suffix_reader, None)
	suffixes = [row[0] for row in suffix_reader]

	suffix_streets = set()
	dir_streets = set()

	for name in names:
		words = name.split(' ')

		try:
			for word in words:
				
				did_flag = False

				if word in suffixes:
					suffix_streets.add(name)
					did_flag = True

				if word in DIRS:
					dir_streets.add(name)
					did_flag = True

				if did_flag:
					raise

		except:
			pass

print 'SUFFIX STREETS\n===================='
for x in sorted(suffix_streets):
	print x
print '\n'

print 'DIR STREETS\n===================='
for x in sorted(dir_streets):
	print x