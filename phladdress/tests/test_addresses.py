TEST_ADDRESSES = [

	# Basic address
	{
		'input': '1234 MARKET ST',
		'expected_results': {
			'components': {
				'address': {
					'full': '1234',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1234',
					'low_fractional': None,
					'low_num': 1234,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1234 MARKET ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1234 MARKET ST',
			'standardized_address': '1234 MARKET ST',
			'type': 'address'
		}
	},


	# Unit: pound, no space
	{
		'input': '1234 MARKET ST #4',
		'expected_results': {
			'components': {
				'address': {
					'full': '1234',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1234',
					'low_fractional': None,
					'low_num': 1234,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1234 MARKET ST # 4',
				'unit': {
					'num': '4',
					'type': '#'
				}
			},
			'input_address': '1234 MARKET ST #4',
			'standardized_address': '1234 MARKET ST # 4',
			'type': 'address'
		}
	},


	# Unit: pound, space
	{
		'input': '1234 MARKET ST # 4',
		'expected_results': {
			'components': {
				'address': {
					'full': '1234',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1234',
					'low_fractional': None,
					'low_num': 1234,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1234 MARKET ST # 4',
				'unit': {
					'num': '4',
					'type': '#'
				}
			},
			'input_address': '1234 MARKET ST # 4',
			'standardized_address': '1234 MARKET ST # 4',
			'type': 'address'
		}
	},


	# Unit full
	{
		'input': '1234 MARKET ST FLOOR 15',
		'expected_results': {
			'components': {
				'address': {
					'full': '1234',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1234',
					'low_fractional': None,
					'low_num': 1234,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1234 MARKET ST FL 15',
				'unit': {
					'num': '15',
					'type': 'FL'
				}
			},
			'input_address': '1234 MARKET ST FLOOR 15',
			'standardized_address': '1234 MARKET ST FL 15',
			'type': 'address'
		}

	},


	# Inverted unit with ordinal
	{
		'input': '1234 MARKET ST 15TH FLOOR',
		'expected_results': {
			'components': {
				'address': {
					'full': '1234',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1234',
					'low_fractional': None,
					'low_num': 1234,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1234 MARKET ST FL 15',
				'unit': {
					'num': '15',
					'type': 'FL'
				}
			},
			'input_address': '1234 MARKET ST 15TH FLOOR',
			'standardized_address': '1234 MARKET ST FL 15',
			'type': 'address'
		}

	},


	# Standard numeric + front/rear unit
	{
		'input': '337 S CAMAC ST APT 2R',
		'expected_results': {
			'components': {
				'address': {
					'full': '337',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '337',
					'low_fractional': None,
					'low_num': 337,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'S CAMAC ST',
					'name': 'CAMAC',
					'postdir': None,
					'predir': 'S',
					'suffix': 'ST'
				},
				'street_address': '337 S CAMAC ST APT 2R',
				'unit': {
					'num': '2R',
					'type': 'APT'
				}
			},
			'input_address': '337 S CAMAC ST APT 2R',
			'standardized_address': '337 S CAMAC ST APT 2R',
			'type': 'address'
		}
	},


	# Ordinal floor + front/rear
	{
		'input': '337 S CAMAC ST 2ND FLOOR REAR',
		'expected_results': {
			'components': {
				'address': {
					'full': '337',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '337',
					'low_fractional': None,
					'low_num': 337,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'S CAMAC ST',
					'name': 'CAMAC',
					'postdir': None,
					'predir': 'S',
					'suffix': 'ST'
				},
				'street_address': '337 S CAMAC ST FL 2 REAR',
				'unit': {
					'num': '2 REAR',
					'type': 'FL'
				}
			},
			'input_address': '337 S CAMAC ST 2ND FLOOR REAR',
			'standardized_address': '337 S CAMAC ST FL 2 REAR',
			'type': 'address'
		}
	},


	# Unit type in street name
	{
		'input': '1 GREENHILL APARTMENT DR',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'GREENHILL APARTMENT DR',
					'name': 'GREENHILL APARTMENT',
					'postdir': None,
					'predir': None,
					'suffix': 'DR'
				},
				'street_address': '1 GREENHILL APARTMENT DR',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1 GREENHILL APARTMENT DR',
			'standardized_address': '1 GREENHILL APARTMENT DR',
			'type': 'address'
		}
	},


	# Unit num looks like a street suffix
	{
		'input': '1010 RACE ST # PK',
		'expected_results':{
			'components': {
				'address': {
					'full': '1010',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1010',
					'low_fractional': None,
					'low_num': 1010,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'RACE ST',
					'name': 'RACE',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1010 RACE ST # PK',
				'unit': {
					'num': 'PK',
					'type': '#'
				}
			},
			'input_address': '1010 RACE ST # PK',
			'standardized_address': '1010 RACE ST # PK',
			'type': 'address'
		}
	},


	# Redundant pound sign
	{
		'input': '834 CHESTNUT ST # PH 108',
		'expected_results': {
			'components': {
				'address': {
					'full': '834',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '834',
					'low_fractional': None,
					'low_num': 834,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'CHESTNUT ST',
					'name': 'CHESTNUT',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '834 CHESTNUT ST PH 108',
				'unit': {
					'num': '108',
					'type': 'PH'
				}
			},
			'input_address': '834 CHESTNUT ST # PH 108',
			'standardized_address': '834 CHESTNUT ST PH 108',
			'type': 'address'
		}
	},

	# Unit type in street name
	{
		'input': '1 FRONT ST',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'FRONT ST',
					'name': 'FRONT',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1 FRONT ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1 FRONT ST',
			'standardized_address': '1 FRONT ST',
			'type': 'address'
		}
	},


	# Unit type in street name and has unit
	{
		'input': '1 FRONT ST FRONT',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'FRONT ST',
					'name': 'FRONT',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1 FRONT ST FRNT',
				'unit': {
					'num': '',
					'type': 'FRNT'
				}
			},
			'input_address': '1 FRONT ST FRONT',
			'standardized_address': '1 FRONT ST FRNT',
			'type': 'address'
		}
	},


	# Protected street name, has suffix
	{
		'input': '1 COBBS CREEK PKWY',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'COBBS CREEK PKWY',
					'name': 'COBBS CREEK',
					'postdir': None,
					'predir': None,
					'suffix': 'PKWY'
				},
				'street_address': '1 COBBS CREEK PKWY',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1 COBBS CREEK PKWY',
			'standardized_address': '1 COBBS CREEK PKWY',
			'type': 'address'
		}
	},


	# Street name could be mistaken for predir/postdir
	{
		'input': '1 E ST',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'E ST',
					'name': 'E',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1 E ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1 E ST',
			'standardized_address': '1 E ST',
			'type': 'address'
		}
	},


	# Street name could be mistaken for unit
	{
		'input': '124 S PIER',
		'expected_results': {
			'components': {
				'address': {
					'full': '124',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '124',
					'low_fractional': None,
					'low_num': 124,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'S PIER',
					'name': 'PIER',
					'postdir': None,
					'predir': 'S',
					'suffix': None
				},
				'street_address': '124 S PIER',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '124 S PIER',
			'standardized_address': '124 S PIER',
			'type': 'address'
		}
	},


	# Junk after suffix, contains a unit type
	{	'input': '124 NAUDAIN ST ENTER ON SIDE',
		'expected_results': {
			'components': {
				'address': {
					'full': '124',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '124',
					'low_fractional': None,
					'low_num': 124,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'NAUDAIN ST',
					'name': 'NAUDAIN',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '124 NAUDAIN ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '124 NAUDAIN ST ENTER ON SIDE',
			'standardized_address': '124 NAUDAIN ST',
			'type': 'address'
		}
	},


	{
		'input': '2250 N 16TH ST # 02ND FRONT',
		'expected_results': {
			'components': {
				'address': {
					'full': '2250',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '2250',
					'low_fractional': None,
					'low_num': 2250,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'N 16TH ST',
					'name': '16TH',
					'postdir': None,
					'predir': 'N',
					'suffix': 'ST'
				},
				'street_address': '2250 N 16TH ST FRNT 2',
				'unit': {
					'num': '2',
					'type': 'FRNT'
				}
			},
			'input_address': '2250 N 16TH ST # 02ND FRONT',
			'standardized_address': '2250 N 16TH ST FRNT 2',
			'type': 'address'
		}
	},


	# Postdir
	{
		'input': '201 N INDEPENDENCE MALL W',
		'expected_results': {
			'components': {
				'address': {
					'full': '201',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '201',
					'low_fractional': None,
					'low_num': 201,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'N INDEPENDENCE MALL W',
					'name': 'INDEPENDENCE',
					'postdir': 'W',
					'predir': 'N',
					'suffix': 'MALL'
				},
				'street_address': '201 N INDEPENDENCE MALL W',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '201 N INDEPENDENCE MALL W',
			'standardized_address': '201 N INDEPENDENCE MALL W',
			'type': 'address'
		}
	},


	# Postdir in street name. This is from OPA.
	{
		'input': '201 N INDEPENDENCE W MALL',
		'expected_results': {
			'components': {
				'address': {
					'full': '201',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '201',
					'low_fractional': None,
					'low_num': 201,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'N INDEPENDENCE MALL W',
					'name': 'INDEPENDENCE',
					'postdir': 'W',
					'predir': 'N',
					'suffix': 'MALL'
				},
				'street_address': '201 N INDEPENDENCE MALL W',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '201 N INDEPENDENCE W MALL',
			'standardized_address': '201 N INDEPENDENCE MALL W',
			'type': 'address'
		}

	},


	# Street name w/dir
	{
		'input': '1 SOUTH ST',
		'expected_results': {
			'components': {
				'address': {
					'full': '1',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1',
					'low_fractional': None,
					'low_num': 1,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': 'SOUTH ST',
					'name': 'SOUTH',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1 SOUTH ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '1 SOUTH ST',
			'standardized_address': '1 SOUTH ST',
			'type': 'address'
		}
	},


	# Street name common
	{
		'input': '2200 BEN FRANKLIN PKW',
		'expected_results': {
			'components': {
				'address': {
					'full': '2200',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '2200',
					'low_fractional': None,
					'low_num': 2200,
					'low_parity': 'E',
					'low_suffix': ''
				},
				'street': {
					'full': 'BENJAMIN FRANKLIN PKWY',
					'name': 'BENJAMIN FRANKLIN',
					'postdir': None,
					'predir': None,
					'suffix': 'PKWY'
				},
				'street_address': '2200 BENJAMIN FRANKLIN PKWY',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '2200 BEN FRANKLIN PKW',
			'standardized_address': '2200 BENJAMIN FRANKLIN PKWY',
			'type': 'address'
		}
	},


	{
		'input': '1136A SOUTH ST #A',
		'expected_results': {
			'components': {
				'address': {
					'full': '1136A',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '1136A',
					'low_fractional': None,
					'low_num': 1136,
					'low_parity': 'E',
					'low_suffix': 'A'
				},
				'street': {
					'full': 'SOUTH ST',
					'name': 'SOUTH',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '1136A SOUTH ST # A',
				'unit': {
					'num': 'A',
					'type': '#'
				}
			},
			'input_address': '1136A SOUTH ST #A',
			'standardized_address': '1136A SOUTH ST # A',
			'type': 'address'
		}
	},


	# Ordinal street missing ordinal suffix
	{
		'input': '133 10 ST',
		'expected_results': {
			'components': {
				'address': {
					'full': '133',
					'high': None,
					'high_fractional': None,
					'high_num': None,
					'high_num_full': None,
					'high_parity': None,
					'high_suffix': None,
					'low': '133',
					'low_fractional': None,
					'low_num': 133,
					'low_parity': 'O',
					'low_suffix': ''
				},
				'street': {
					'full': '10TH ST',
					'name': '10TH',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_address': '133 10TH ST',
				'unit': {
					'num': None,
					'type': None
				}
			},
			'input_address': '133 10 ST',
			'standardized_address': '133 10TH ST',
			'type': 'address'
		}
	},


################################################################################
# INTERSECTIONS
################################################################################

	# Basic intersection
	{
		'input': '4TH ST & CARPENTER LN',
		'expected_results': 
		{
			'components': {
				'street_1': {
					'full': '4TH ST',
					'name': '4TH',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_2': {
					'full': 'CARPENTER LN',
					'name': 'CARPENTER',
					'postdir': None,
					'predir': None,
					'suffix': 'LN'
				}
			},
			'input_address': '4TH ST & CARPENTER LN',
			'standardized_address': '4TH ST & CARPENTER LN',
			'type': 'intersection'
		}
	},


	# Ordinal intersection missing ordinal suffix
	{
		'input': '4 & CARPENTER',
		'expected_results': 
		{
			'components': {
				'street_1': {
					'full': '4TH',
					'name': '4TH',
					'postdir': None,
					'predir': None,
					'suffix': None
				},
				'street_2': {
					'full': 'CARPENTER',
					'name': 'CARPENTER',
					'postdir': None,
					'predir': None,
					'suffix': None
				}
			},
			'input_address': '4 & CARPENTER',
			'standardized_address': '4TH & CARPENTER',
			'type': 'intersection'
		}
	},


	# Plural street suffix
	{
		'input': 'MARKET & BROAD STS',
		'expected_results': {
			'components': {
				'street_1': {
					'full': 'MARKET ST',
					'name': 'MARKET',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				},
				'street_2': {
					'full': 'BROAD ST',
					'name': 'BROAD',
					'postdir': None,
					'predir': None,
					'suffix': 'ST'
				}
			},
			'input_address': 'MARKET & BROAD STS',
			'standardized_address': 'MARKET ST & BROAD ST',
			'type': 'intersection'
		}
	},
]