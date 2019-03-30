# list.py
#	functions for manipulating and creating lists.

def merge_everyOther(listA=[], listB=[], listC=[], listD=[], listE=[], listF=[], listG=[], listH=[], listI=[], listJ=[], **kwargs):
	'''
	Merges two lists into a single list

	Merges two lists, taking the first of each and inserting it into a new list, then the second of each, and so on.

	Parameters:
	listA-J		(list)	:	The set of list, maximum being 10, minimum being 2.
	Returns:
	list				:	A merged list
	'''
	output = []
	length = 0
	x = 0

	if len(listA) > length: length = len(listA)
	if len(listB) > length: length = len(listB)
	if len(listC) > length: length = len(listC)
	if len(listD) > length: length = len(listD)
	if len(listE) > length: length = len(listE)
	if len(listF) > length: length = len(listF)
	if len(listG) > length: length = len(listG)
	if len(listH) > length: length = len(listH)
	if len(listI) > length: length = len(listI)
	if len(listJ) > length: length = len(listJ)

	while x < length:
		if len(listA) > x: output.append(listA[x])
		if len(listB) > x: output.append(listB[x])
		if len(listC) > x: output.append(listC[x])
		if len(listD) > x: output.append(listD[x])
		if len(listE) > x: output.append(listE[x])
		if len(listF) > x: output.append(listF[x])
		if len(listG) > x: output.append(listG[x])
		if len(listH) > x: output.append(listH[x])
		if len(listI) > x: output.append(listI[x])
		if len(listJ) > x: output.append(listJ[x])
		x += 1

	return output
