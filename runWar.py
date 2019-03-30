import modDisp
import modFile
import modList
import random

input('Please enter full-screen, then press enter. This demo requires a terminal size of at least 130 characters wide.')

while True:
	deck = modFile.read_list("cardFrench.txt")
	available = list(range(52))
	x = None
	turn = True
	human_deck = []
	robot_deck = []

	while len(available) > 0:
		while x not in available:
			x = random.randrange(0, 52)
		if turn:
			human_deck.append(deck[x])
		else:
			robot_deck.append(deck[x])
		available.remove(x)
		turn = not turn

	deck_display_upper = []
	deck_display_lower = []
	for x in human_deck[:13]:
		deck_display_upper.append(modDisp.as_block(x, aslist=True))
	deck_display = modList.merge_alternate(deck_display_upper)
	for x in human_deck[13:]:
		deck_display_lower.append(modDisp.as_block(x, aslist=True))
	deck_display.extend(modList.merge_alternate(deck_display_lower))
	print("Your deck:")
	y = 1
	z = 11
	a = 1
	for x in deck_display:
		if z == 11:
			print(f'{a:02}', end='')
			a += 1
		else:
			print('  ', end='')
		if y == 13:
			print(x)
			y = 0
			if z == 11:
				z = 0
			else:
				z += 1
		else:
			print(x, end='')
		y += 1
	print('', flush=True)

	select = input("Enter a number to select a card, or anything else to exit")

	try:
		slt = int(select)
	except:
		break
	if int(select) not in list(range(27)):
		break

	print(modDisp.as_block(human_deck[slt], height=25, width=25, heavyblocks=True))

	input("Enter to restart")