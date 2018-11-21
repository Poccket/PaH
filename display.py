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
	output += block[heavy][1]+ '\n' + block[heavy][4]
	currHeight += 1
	if text:
		maxWidth = width - 2
		counter = 0
		for x in text:
			if currHeight < height:
				if counter < maxWidth:
					output += x
					counter += 1
				else:
					output += block[heavy][4] + "\n" + block[heavy][4] + x
					currHeight += 1
					counter = 1
		while counter < maxWidth:
			output += " "
			counter += 1
		output += block[heavy][4]
	print(currHeight)
	return output

'''
TO-DO:
check height!
cannot go past height when writing text to output
finish creating block pieces until reached given height
'''