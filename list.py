# list.py
#	functions for manipulating and creating lists.

def merge_everyOther(listA, listB):
	'''
	Merges two lists into a single list

	Merges two lists, taking the first of each and inserting it into a new list, then the second of each, and so on.

	Parameters:
	listA		(list)	:	The first list, will be the first of each set
	listB		(list)	:	The second list, will be the second of each set
	Returns:
	list				:	A merged list
	'''
	output = []

	if len(listA) >= len(listB):
		lenSmall = len(listB)
	else:
		lenSmall = len(listA)

	print(str(lenSmall) + " " + str(len(listA)) + " " + str(len(listB)))
	x = 0
	while x < lenSmall:
		print(x)
		output.append(listA[x])
		output.append(listB[x])
		x += 1

	if len(listA) > len(listB):
		while x < len(listA):
			output.append(listA[x])
			x += 1
	elif len(listB) > len(listA):
		while x < len(listB):
			output.append(listB[x])
			x += 1

	return output
