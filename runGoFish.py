import modDisp
import modFile
import modList
import modHelper
import random
import shutil
import math
import time
import os

print("---")
print("Make sure your terminal size is large enough, or you'll get an error!")
print("---")

ui = []
scr_columns, scr_rows = shutil.get_terminal_size((70, 100))
for a in list(range(scr_rows)):
	ui.append("")


def uiprint(inp="", line=-1, push=False, doprint=False):
	try:
		del ui[scr_rows+1]
	except IndexError:
		pass
	if push:
		ui.insert(line, inp)
	else:
		ui[line] = inp
	if doprint:
		os.system('cls' if os.name == 'nt' else 'clear')
		for item in reversed(ui):
			print(item)


def colorcheck(inp):
	if "Heart" in inp:
		return "Red"
	if "Diamond" in inp:
		return "Red"
	if "Club" in inp:
		return "Black"
	if "Spade" in inp:
		return "Black"
	if "JOKER" in inp:
		return ""
	return "UH OH SOMETHINGS BROKEN"


def rankcheck(inp):
	if "Ace" in inp:
		return "ace"
	if "King" in inp:
		return "King"
	if "Queen" in inp:
		return "Queen"
	if "Jack" in inp:
		return "Jack"
	if "Ten" in inp:
		return "ten"
	if "Nine" in inp:
		return "nine"
	if "Eight" in inp:
		return "eight"
	if "Seven" in inp:
		return "seven"
	if "Six" in inp:
		return "six"
	if "Five" in inp:
		return "five"
	if "Four" in inp:
		return "four"
	if "Three" in inp:
		return "three"
	if "Two" in inp:
		return "two"
	if "JOKER" in inp:
		return "Joker"
	return "UH OH SOMETHINGS BROKEN"


deck = modFile.read_list("decks/cardFrench.txt")
available = list(range(len(deck)))
turn = True
human_hand = []
robot_hand = []


def dealcard():
	if len(deck) != 0:
		card = None
		while card not in available:
			card = random.randrange(0, len(deck))
		available.remove(card)
	else:
		card = False
	return card


while len(available) > 44:
	if turn:
		human_hand.append(deck[dealcard()])
	else:
		robot_hand.append(deck[dealcard()])
	turn = not turn

human_win = []
robot_win = []
human_wins = 0
robot_wins = 0
while True:
	if len(human_hand) < 1:
		uiprint("Human hand exhausted! Ending game.", ui_height, True, True)
		break
	if len(robot_hand) < 1:
		uiprint("Robot hand exhausted! Ending game.", ui_height, True, True)
		break
	max_cards = math.floor(scr_columns / 14)
	rows_needed = math.ceil(len(human_hand) / max_cards)
	ui_height = math.ceil(rows_needed * 12) + 3
	curr_height = ui_height-4
	uiprint("Wins: {} ROB - YOU {}".format(robot_wins, human_wins), ui_height-2)

	for c1 in human_hand:
		for c2 in human_hand:
			if c1 != c2 and rankcheck(c1) == rankcheck(c2) and colorcheck(c1) == colorcheck(c2):
				uiprint("Player: Match in my hand.", ui_height, True, True)
				human_win.append(c1)
				human_win.append(c2)
				human_wins += 1
				uiprint("Wins: {} ROB - YOU {}".format(robot_wins, human_wins), ui_height - 2)
				uiprint("You have {} win(s)!".format(human_wins), ui_height, True, True)
				human_hand.remove(c2)
				human_hand.remove(c1)
	for c1 in robot_hand:
		for c2 in robot_hand:
			if c1 != c2 and rankcheck(c1) == rankcheck(c2) and colorcheck(c1) == colorcheck(c2):
				uiprint("Robot: Got a match here!", ui_height, True, True)
				robot_win.append(c1)
				robot_win.append(c2)
				robot_wins += 1
				uiprint("Wins: {} ROB - YOU {}".format(robot_wins, human_wins), ui_height - 2)
				uiprint("Robot has {} win(s)!".format(robot_wins), ui_height, True, True)
				robot_hand.remove(c1)
				robot_hand.remove(c2)

	hand_blocks = []
	for x in human_hand:
		hand_blocks.append(modDisp.as_block(x, aslist=True))

	hand_display = modList.merge_alternate(hand_blocks, endchar="list")

	row_startingCard = 0

	curr_line = ""
	for x in range(0, rows_needed):
		for z in hand_display:
			for y in range(row_startingCard, max_cards+row_startingCard):
				if y < len(z):
					if z == hand_display[0]:
						curr_line += f'{y:02}'
					else:
						curr_line += '  '
					curr_line += z[y]
			uiprint(curr_line, curr_height)
			curr_height -= 1
			curr_line = ""
		row_startingCard += max_cards
	uiprint(doprint=True)
	gofish = True
	if turn:
		select = "Not a number!"
		while not modHelper.isinteger(select) or int(select) > len(human_hand)-1:
			select = input("Pick a card to play> ")
			if modHelper.isinteger(select) and int(select) > len(human_hand)-1:
				print("That number is too big!")
			if not modHelper.isinteger(select):
				print("Need to input a number!")
		select = int(select)
		uiprint("Player: Do you have a {} {}?".format(colorcheck(human_hand[select]), rankcheck(human_hand[select])), ui_height, True, True)

		for x in robot_hand:
			if rankcheck(x) == rankcheck(human_hand[select]) and colorcheck(x) == colorcheck(human_hand[select]):
				gofish = False
				human_win.append(x)
				robot_hand.remove(x)
				human_win.append(human_hand[select])
				human_hand.remove(human_hand[select])
				human_wins += 1
				time.sleep(1)
				uiprint("Robot: Yeah, here you go.", ui_height, True, True)
				time.sleep(1)
				uiprint("Wins: {} ROB - YOU {}".format(robot_wins, human_wins), ui_height - 2)
				uiprint("You have {} win(s)!".format(human_wins), ui_height, True, True)
				break

		if gofish:
			time.sleep(1)
			uiprint("Robot: Sorry, I don't. Go fish.", ui_height, True, True)
			card_in = dealcard()
			if card_in:
				human_hand.append(deck[card_in])
			else:
				uiprint("Deck is empty! Ending game.", ui_height, True, True)
				break

		turn = not turn
	else:
		select = random.randrange(0, len(robot_hand))
		time.sleep(2)
		uiprint("Robot: Got a {} {}?".format(colorcheck(robot_hand[select]), rankcheck(robot_hand[select])), ui_height, True, True)
		gofish = True
		for x in human_hand:
			if rankcheck(x) == rankcheck(robot_hand[select]) and colorcheck(x) == colorcheck(robot_hand[select]):
				gofish = False
				robot_win.append(x)
				human_hand.remove(x)
				robot_win.append(robot_hand[select])
				robot_hand.remove(robot_hand[select])
				robot_wins += 1
				time.sleep(1)
				uiprint("Player: Yup, here you go.", ui_height, True, True)
				time.sleep(1)
				uiprint("Wins: {} ROB - YOU {}".format(robot_wins, human_wins), ui_height - 2)
				uiprint("Robot has {} win(s)!".format(robot_wins), ui_height, True, True)
				time.sleep(2)
				break
		if gofish:
			time.sleep(1)
			uiprint("Player: Don't have it, Go fish.", ui_height, True, True)
			card_in = dealcard()
			if card_in:
				robot_hand.append(deck[card_in])
			else:
				uiprint("Deck is empty! Ending game.", ui_height, True, True)
				break

		turn = not turn

if human_wins == robot_wins:
	uiprint("There was a tie!", ui_height, True, True)
elif human_wins > robot_wins:
	uiprint("You won! Congratulations!", ui_height, True, True)
elif robot_wins > human_wins:
	uiprint("You lost! Try again!", ui_height, True, True)