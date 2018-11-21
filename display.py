# display.py

block = {
	'heavy': ["┏", "┓", "┗", "┛", "┃", "━"], 
	'light': ["┌", "┐", "└", "┘", "│", "─"]
}

def asBlock(text, width, height, heavyB):
	try:
		text = str(text)
		width = int(width)
		height = int(height)
		heavyB = bool(heavyB)
	except Exception as e:
		return e
	if heavyB:
		heavy = "heavy"
	else:
		heavy = "light"
	currHeight = 1
	output = block[heavy][0]
	x = width - 2
	while x > 0:
		output += block[heavy][5]
		x -= 1
	output += block[heavy][1]+ '\n'
	currHeight += 1
	if text:
		maxWidth = width - 2
		counter = 0
		if currHeight < height:
			output += block[heavy][4]
		for x in text:
			if currHeight < height:
				if counter < maxWidth-1:
					output += x
					counter += 1
				else:
					output += block[heavy][4] + "\n" + block[heavy][4] + x
					currHeight += 1
					counter = 1
		if currHeight < height:
			while counter < maxWidth:
				output += " "
				counter += 1
			output += block[heavy][4] + '\n'
			currHeight += 1
	while currHeight < height:
		output += block[heavy][4]
		counter = 0
		while counter < maxWidth:
			output += " "
			counter += 1
		output += block[heavy][4] + '\n'
		currHeight += 1
	x = width - 2
	output += block[heavy][2]
	while x > 0:
		output += block[heavy][5]
		x -= 1
	output += block[heavy][3]
	print(currHeight)
	return output

'''
TO-DO:
check height!
cannot go past height when writing text to output
finish creating block pieces until reached given height
'''