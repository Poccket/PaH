# file.py
# functions for reading or writing to files
from typing import List


def readaslist(filename: str) -> List[str]:
	"""Reads files into a list."""
	fileopen = open(filename, "r")  # set fileOpen as the file, with option 'r' for reading.
	return fileopen.read().splitlines()  # return an array version of the file, where it splits at newlines.


def readasraw(filename: str) -> str:
	"""Reads files into a string."""
	fileopen = open(filename, "r")  # set fileOpen as the file, with option 'r' for reading.
	return fileopen.read()  # return a string version of the file, with no manipulation.
