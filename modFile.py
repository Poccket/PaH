# file.py
#	functions for reading or writing to files

def readAsList(fileName):
	'''
	Reads files into a list.

        Takes in a filename, reads it into a buffer, then returns the buffer as a list, splitting items at newlines.

        Parameters:
        fileName    (str)   :   The name of the file to read
        Returns:
        list                :   A list of the contents of the file
	'''
	fileOpen = open(fileName, "r")								#	set fileOpen as the file, with option 'r' for reading.
	return fileOpen.read().splitlines()							#	return an array version of the file, where it splits at newlines.

def readAsRaw(fileName):
	'''
	Reads files into a string.

        Takes in a filename, reads it into a buffer, then returns the buffer as a string.

        Parameters:
        fileName    (str)   :   The name of the file to read
        Returns:
        str                 :   A string of the contents of the file
	'''
	fileOpen = open(fileName, "r")								#	set fileOpen as the file, with option 'r' for reading.
	return fileOpen.read()										#	return a string version of the file, with no manipulation.
