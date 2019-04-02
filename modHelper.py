def isinteger(i):
	"""
	Checks if an object is an integer

	:param i: Input object
	:return: boolean
	"""
	try:
		int(i)
		return True
	except ValueError:
		return False
