# list_manip.py
# functions for manipulating and creating lists.
from typing import List


def merge_alternate(listlist: list) -> List[str]:
	"""
	Merges lists into one list.

	Creates a single list from a set of lists by alternating through the lists.
	For example, Item from A, Item from B, Item from C, Item from A and so on.

	:param listlist: A list of the lists to merge.
	:return: The merged lists as a single list
	"""
	if type(listlist) != list:
		raise TypeError("item 'listList' must be a list")
	output = []
	length = len(max(listlist, key=len))
	
	for vItem in range(0, length):
		for vList in listlist:
			if vItem <= len(vList)-1:
				output.append(vList[vItem])

	return output
