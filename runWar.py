import modDisp
import modFile
import modList
import random

input('Please enter full-screen, then press enter. This demo requires a terminal size of at least 130 characters wide.')

while True:
	deck = modFile.read_list("cardFrench.txt")
	available = list(range(len(deck)))
	x = None
	turn = True
	human_deck = []
	robot_deck = []

	while len(available) > 0:
		while x not in available:
			x = random.randrange(0, len(deck))
		if turn:
			human_deck.append(deck[x])
		else:
			robot_deck.append(deck[x])
		available.remove(x)
		turn = not turn

	deck_display_upper = []
	deck_display_lower = []

	deck_half = len(human_deck) % 2

	for x in human_deck[:(len(human_deck)//2)+deck_half]:
		deck_display_upper.append(modDisp.as_block(x, aslist=True))
	deck_display = modList.merge_alternate(deck_display_upper, endchar="\n")
	for x in human_deck[(len(human_deck)//2)+deck_half:]:
		deck_display_lower.append(modDisp.as_block(x, aslist=True))
	deck_display.extend(modList.merge_alternate(deck_display_lower, endchar="\n"))
	print("Your deck:")
	for x in deck_display:
		print(x, end='')
	print('', flush=True)

	select = input("Enter a number to select a card, or anything else to exit> ")

	try:
		slt = int(select)-1
	except:
		break
	if int(select) not in list(range(0,27)):
		break

	print(modDisp.as_block(human_deck[slt], heavyblocks=True))

	input("Enter to restart")