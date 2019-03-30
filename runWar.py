import modDisp
import modFile
import modList
import random
import shutil
import math

while True:
	deck = modFile.read_list("decks/cardFrench.txt")
	available = list(range(len(deck)))
	x = None
	turn = True
	human_hand = []
	robot_hand = []

	while len(available) > 0:
		while x not in available:
			x = random.randrange(0, len(deck))
		if turn:
			human_hand.append(deck[x])
		else:
			robot_hand.append(deck[x])
		available.remove(x)
		turn = not turn

	scr_columns, scr_rows = shutil.get_terminal_size((70, 100))
	max_cards = math.floor(scr_columns / 14)
	rows_needed = math.ceil(len(human_hand) / max_cards)

	hand_blocks = []
	for x in human_hand:
		hand_blocks.append(modDisp.as_block(x, aslist=True))

	hand_display = modList.merge_alternate(hand_blocks, endchar="list")

	row_startingCard = 0

	for x in range(0,rows_needed):
		for z in hand_display:
			for y in range(row_startingCard, max_cards+row_startingCard):
				if y < len(z):
					if z == hand_display[0]: print(f'{y:02}', end='')
					else: print('  ', end='')
					print(z[y], end='')
			print('')
		row_startingCard += max_cards

	select = input("Enter a number to select a card, or anything else to exit> ")

	try:
		slt = int(select)-1
	except ValueError:
		break
	if int(select) not in list(range(0,27)):
		break

	print(modDisp.as_block(human_hand[slt], heavyblocks=True))

	input("Enter to restart")