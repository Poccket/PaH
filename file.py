# file.py
#	functions for reading or writing to files

# readFileAsList(fileName)
#	Reads files into a list, splitting at newlines.
def readFileAsList(fileName):
	try:
		fileOpen = open(fileName, "r")
		return fileOpen.read().splitlines()
	except:
		return "There was an error!"

# readFileAsRaw(fileName)
#	Reads files into a string, no splitting.
def readFileAsRaw(fileName):
	try:
		fileOpen = open(fileName, "r")
		return fileOpen.read()
	except:
		return "There was en error!"