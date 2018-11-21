# file.py
#	functions for reading or writing to files

def readAsList(fileName):
	'''
	readAsList(str fileName)
		Reads files into a list, splitting at newlines.
	'''
	fileOpen = open(fileName, "r")
	return fileOpen.read().splitlines()

def readAsRaw(fileName):
	''' 
	readFileAsRaw(str fileName)
		Reads files into a string, no splitting.
	'''
	fileOpen = open(fileName, "r")
	return fileOpen.read()