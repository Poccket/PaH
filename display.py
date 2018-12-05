# display.py

block = {
	'heavy': ["┏", "┓", "┗", "┛", "┃", "━"], 
	'light': ["┌", "┐", "└", "┘", "│", "─"]
}

def asBlock(text="", width=10, height=10, heavyB=False, **kwargs):
	try:																		# gotta make sure that all of the variables are the right type
		text = str(text)
		width = int(width)
		height = int(height)
		heavyB = bool(heavyB)
	except Exception as e:														# throw an error if they're not, since we can't use them
		return e

	if heavyB:																	# check if $heavyB is true
		weight = "heavy"														# so we know if they wanna use the bold or light block pieces
	else:
		weight = "light"

	currHeight = 1																# create variable so we know the current height ($currHeight)
	output = block[weight][0]													# set $output to ┏, the first character of the block
	x = width - 2																# set $x to $width minus 2, which would be the length of the upper straight line
	while x > 0:																# and while $x is bigger than 0
		output += block[weight][5]												# 	add ━ to $output
		x -= 1																	# 	and remove 1 from $x
																				# 	this creates the upper straight line

	output += block[weight][1]+ '\n'											# add ┓, the second corner and a newline to $output
	currHeight += 1																# add one to $currHeight since we added a newline

	if text:																	# check if $text is valid, so we don't go through this if we don't really have text
		counter = 0																# 	set $counter to 0, which will be used to track the current length of the line
		limit = (width-2)*(height-2)											# 	set limit to ($width minus 2) times ($height minus 2), which is the number of characters in the box
		text = text[:limit]														# 	cut any characters that wouldn't fit out of $text

		if currHeight < height:													#	if the $currHeight is less than the total $height, as we don't wanna do this if the box is too small
			output += block[weight][4]											#		add ┃ to the $output, the first line of the left wall

		for x in text:															# 	and for every letter in $text, referred to as $x from now on
			if currHeight < height:												# 		if $currHeight is less than the total $height,
				if counter < width-2:											#			if $counter is less than the $width minus 2, so we know if the line is full
					output += x													#				add $x to the $output
					counter += 1												#				add 1 to the $counter
				else:															#			else, for when $counter isn't less since the line is full
					output += block[weight][4] + "\n" + block[weight][4]+ x 	# 				add the end of the line (┃), a newline, another ┃, and $x to the $output
					currHeight += 1												#				then add one to $currHeight, since we added a newline
					counter = 1													#				set the $counter back to 1, since it's a new line

		if currHeight < height:													#	if $currHeight is less than $height,
			while counter < width-2:											#		then while the $counter is smaller than $width minus 2
				output += " "													#			add a blank space to the $output, since the box would be broken if there's no air inside
				counter += 1													#			and add one to $counter since we're adding a character
			output += block[weight][4] + '\n'									#		add ┃ and a newline to $output
			currHeight += 1														#		then add to $currHeight since we made a newline

	while currHeight < height:													# then, while $currHeight is less than $height,
		output += block[weight][4]												#	add ┃ to $output
		counter = 0																#	set the $counter to 0
		while counter < width-2:												#	and then, while $counter is less than $width minus 2
			output += " "														#		add a blank space to $output
			counter += 1														#		and one to the counter
		output += block[weight][4] + '\n'										#	close the line with a ┃ and a newline added to $output
		currHeight += 1															# 	add one to $currHeight

	x = width - 2																# set $x to $width minus two, the length of the straight bottom line
	output += block[weight][2]													# add ┗ to start the final line
	while x > 0:																# then, while $x is bigger than 0,
		output += block[weight][5]												# 	add a straight line,
		x -= 1																	# 	take one from $x
	output += block[weight][3]													# add ┛ to $output, so the box is closed and protected from epic hackers
	return output																# return $output to whatever called the function
