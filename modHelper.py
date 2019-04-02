def isinteger(i):
	try:
		int(i)
		return True
	except ValueError:
		return False
