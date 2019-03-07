# file.py
#	functions for reading or writing to files

def readAsList(fileName):
	'''
	readAsList(str fileName)
		Reads files into a list, splitting at newlines.
	'''
	fileOpen = open(fileName, "r")								#	set fileOpen as the file, with option 'r' for reading.
	return fileOpen.read().splitlines()							#	return an array version of the file, where it splits at newlines.

def readAsRaw(fileName):
	'''
	readFileAsRaw(str fileName)
		Reads files into a string, no splitting.
	'''
	fileOpen = open(fileName, "r")								#	set fileOpen as the file, with option 'r' for reading.
	return fileOpen.read()										#	return a string version of the file, with no manipulation.
