# list_manip.py
# functions for manipulating and creating lists.
from typing import List


def merge_everyother(listlist: list) -> List[str]:
	"""Merges lists into a single list"""
	if type(listlist) != list:
		raise TypeError("item 'listList' must be a list")
	output = []
	length = len(max(listlist, key=len))
	
	for vItem in range(0, length):
		for vList in listlist:
			if vItem <= len(vList)-1:
				output.append(vList[vItem])

	return output
