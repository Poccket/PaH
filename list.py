# list.py
#	functions for manipulating and creating lists.

def merge_everyOther(listList=[], **kwargs):
	'''
	Merges lists into a single list

	Merges lists, taking the first of each and inserting it into a new list, then the second of each, and so on.

	Parameters:
	listList	(list)	:	List of all the lists to be merged
	Returns:
	list				:	A merged list
	'''
	output = []
	length = len(max(listList, key=len))
	
	for vItem in range(0, length):
		for vList in listList:
			if vItem <= len(vList)-1:
				output.append(vList[vItem])

	return output
