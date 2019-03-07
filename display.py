# display.py

block = {																		#	The 'block' dictionary, with two lists.
	'heavy': ["┏", "┓", "┗", "┛", "┃", "━"],									#		The first list, 'heavy', contains heavy block building characters.
	'light': ["┌", "┐", "└", "┘", "│", "─"]										#		The second list, 'light', contains light block building characters.
}																				#	The lists are ordered as such: DOWN-RIGHT DOWN-LEFT UP-RIGHT UP-LEFT VER HOR

def asBlock(text="", width=10, height=10, heavyBlocks=False, doCompensate=True, asList=False, **kwargs):
	'''
	Displays text in a block, created from ASCII characters.

	Takes input as text, and creates a block from ASCII block building characters, containing the text inside (with wrapped text)
	Two options are available for the characters, heavy and light, as seen below:
	Heavy:┏┓┗┛┃━		Light: ┌┐└┘│─

	Parameters:
	text		(str)	:	The text to use in the block
	width		(int)	:	The width of the block in characters, discluding the sides unless doCompensate is set as False
	height		(int)	:	The height of the block in characters, discluding the top/bottom unless doCompensate is set as False
	heavyBlocks	(bool)	:	Whether or not to use the heavy set of ASCII block building characters
	doCompensate    (bool)	:	If set to False, width and height will be of the block, not the area containing the text
    asList          (bool)  :       If set to True, each line will be an item in a list.
	Returns:
	str			:	The text contained within an ASCII block
    OR
    list                    :       The text contained within an ASCII block
	'''
	try:																		#	Attempt to set all the variables as the right type
		text =			str(text)
		width =			int(width)
		height =		int(height)
		heavyBlocks =	bool(heavyBlocks)
		doCompensate =	bool(doCompensate)
		asList =		bool(asList)
	except Exception as e:														#	If any throw an error, return the error and quit.
		return e

	if heavyBlocks:																#	Check to see if heavyBlocks is set to True
		weight = "heavy"														#		If it is, set the weight to 'heavy'
	else:
		weight = "light"														#		If not, set the weight to 'light'

	if doCompensate:															#	Check to see if doCompensate is true, which it is by default
		width += 2																#		If it is, we add 2 to the width and height to get a 'true' width and height
		height += 2																#		instead of the width/height of the text area
	currHeight = 1																#	currHeight keeps track of the line we're on, to compare to the height, set to 1 for now
	if asList:
		output = []
		output.append(block[weight][0])
	else:
		output = block[weight][0]												#	And we'll set the output as DOWN-RIGHT, which is always the first character.
	x = width - 2																#	Here we set x to the width minus 2, which is the length of the straight upper line
	while x > 0:																#	Then, while x is bigger than 0
		if asList:
			output[currHeight-1] += block[weight][5]
		else:
			output += block[weight][5]											#		add a HOR to output
		x -= 1																	#		and remove 1 from x
																				#	Which leaves up with the upper straight line and the NW corner.
	if asList:
		output[currHeight-1] += block[weight][1]
		output.append("")
	else:
		output += block[weight][1]+ '\n'										#	Finally we add the DOWN-LEFT, which completes the first line of the block.
	currHeight += 1																#	Then, since we added a newline, and have moved to line 2, add one to currHeight

	if text:																	#	Check if text is a valid variable, ie; not empty, null or undefined.
		counter = 0																#		Then we set counter to 0, which keeps track of the amount of characters on the line
		limit = (width-2)*(height-2)											#		Set limit to (width minus 2) times (height minus 2), aka the max characters allowed
		text = text[:limit]														#		Then, simply cut out any characters that wouldn't fit.

		if currHeight < height:													#	Check if currHeight is already smaller than height, so we don't exceed it by doing this
			if asList:
				output[currHeight-1] += block[weight][4]
			else:
				output += block[weight][4]										#		Add a VER to the output, the first line of the left wall

		for x in text:															# 	And for every letter in text
			if currHeight < height:												# 		check to make sure currHeight hasn't past height, if it hasn't,
				if counter < width-2:											#			check if the characters on line is smaller than the width allowed, if so
					if asList:
						output[currHeight-1] += x
					else:
						output += x												#				add the letter to the output
					counter += 1												#				and add 1 to the counter
				else:															#			if the characters on the line are more than the width
					if asList:
						output[currHeight-1] += block[weight][4]
						output[currHeight] += block[weight][4] + x
					else:
						output += block[weight][4] + "\n" + block[weight][4]+ x	# 				add a VER, newline, VER and the letter to the output
					currHeight += 1												#				then since we're on a newline we add 1 to currHeight
					counter = 1													#				and set the counter to 1, since it's a newline and we've put a character in

		if currHeight < height:													#	if the currHeight isn't past height
			while counter < width-2:											#		then while the counter isn't past the width minus 2
				if asList:
					output[currHeight-1] += " "
				else:
					output += " "												#			add blank filler space to the output
				counter += 1													#			and add one to counter since we're adding a character
			if asList:
				output[currHeight-1] += block[weight][4]
				output.append("")
			else:
				output += block[weight][4] + '\n'								#		after that, add a VER and a newline
			currHeight += 1														#		then add to currHeight since we made a newline

	while currHeight < height:													# then, while currHeight is less than height, so we don't overshoot
		if asList:
			output[currHeight-1] += block[weight][4]
		else:
			output += block[weight][4]											#	add a VER to the output
		counter = 0																#	set the counter to 0
		while counter < width-2:												#	and then, while counter is less than width minus 2
			if asList:
				output[currHeight-1] += " "
			else:
				output += " "													#		add a blank space to output
			counter += 1														#		and one to the counter
		if asList:
			output[currHeight-1] += block[weight][4]
			output.append("")
		else:
			output += block[weight][4] + '\n'									#	close the line with a VER and a newline added to output
		currHeight += 1															# 	add one to currHeight, because newline

	x = width - 2																# Set x to width minus 2, which is the length of the bottom straight line.
	if asList:
		output[currHeight-1] += block[weight][2]
	else:
		output += block[weight][2]												# add a UP-RIGHT to the output, the third corner.
	while x > 0:																# then, while x is bigger than 0,
		if asList:
			output[currHeight-1] += block[weight][5]
		else:
			output += block[weight][5]											# 	add a HOR line,
		x -= 1																	# 	and remove 1 from x
	if asList:
		output[currHeight-1] += block[weight][3]
	else:
		output += block[weight][3]												# add the final block, a UP-LEFT, to close the box, and protect it from 3p1c h4x0rz
	return output																# return output to whatever called the function
