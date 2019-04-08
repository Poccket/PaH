"""Functions for manipulating files"""
from typing import List


def read_list(filename: str) -> List[str]:
    """Reads files into a list of lines

    :param filename: The file name
    :return: A list of the file's contents
    """
    return open(filename, "r").read().splitlines()
    # Opens a file, and then reads it into a list. Each list item is a line from the file.


def read_raw(filename: str) -> str:
    """Reads files into a string, without any changes

    :param filename: The file name
    :return: The file's contents
    """
    return open(filename, "r").read()
    # Opens a file, and then reads it into a string.
