# file.py
# functions for reading or writing to files
from typing import List


def read_list(filename: str) -> List[str]:
	"""
	Reads files into a list of lines

	:param filename: The file name
	:return: A list of the file's contents
	"""
	fileopen = open(filename, "r")  # set fileOpen as the file, with option 'r' for reading.
	return fileopen.read().splitlines()  # return an array version of the file, where it splits at newlines.


def read_raw(filename: str) -> str:
	"""
	Reads files into a string, without any changes

	:param filename: The file name
	:return: The file's contents
	"""
	fileopen = open(filename, "r")  # set fileOpen as the file, with option 'r' for reading.
	return fileopen.read()  # return a string version of the file, with no manipulation.
