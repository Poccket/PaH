import modDisp
import modFile
import modList
import modHelper
import modUI
import modPlayers
import random
import math
import time
# import os

# os.system('mode con: cols=120 lines=40')

print("---")
print("Make sure your terminal size is large enough, or you'll get an error!")
print("---")

ui = modUI.Screen()
human_player = modPlayers.Player("Player", {'hand': [], 'matches': []})
robot_player = modPlayers.Player("Robot", {'hand': [], 'matches': []})
system = modPlayers.Player("System", groups=['system'])

messages = []
chat_height = 0
curr_height = 0

deck = modFile.read_list("decks/cardFrench.txt")
available = list(range(len(deck)))
turn = True

suits = {
	"colors": {
		"Heart": "Red",
		"Diamond": "Red",
		"Club": "Black",
		"Spade": "Black",
		"JOKER": "wild"
	},
	"cards": {
		"Ace": "ace",
		"King": "king",
		"Queen": "queen",
		"Jack": "jack",
		"Ten": "ten",
		"Nine": "nine",
		"Eight": "eight",
		"Seven": "seven",
		"Six": "six",
		"Five": "five",
		"Four": "four",
		"Three": "three",
		"Two": "two",
		"JOKER": "card"

	}
}


def colorcheck(inp):
	for card, color in suits["colors"].items():
		if card in inp:
			return color
	return "Error"


def rankcheck(inp):
	for card, color in suits["cards"].items():
		if card in inp:
			return color
	return "Error"


def dealcard():
	if len(deck) != 0:
		card = None
		while card not in available:
			card = random.randrange(0, len(deck))
		available.remove(card)
	else:
		card = False
	return card


def send(usr, msg):
	global chat_height
	messages.append("<" + usr.name + "> " + msg)
	if len(messages) > 20:
		del messages[0]
	for a in range(chat_height, ui.height):
		ui.line(a, "clear")
	ui.line(chat_height-1, "clear")
	ui.line(chat_height-5, "clear")
	for msg in messages:
		ui.line(chat_height, "insert", msg)
	ui.print()


def printhand():
	global curr_height
	global chat_height

	# -- UI Variables --
	# The amount of cards that can fit on one row
	max_cards = math.floor(ui.width / 14)
	# The amount of rows needed to display all of the player's cards
	rows_needed = math.ceil(len(human_player.hands['hand']) / max_cards)
	# The height that the cards will start printing at.
	curr_height = math.ceil(rows_needed * 12)-1
	# Exactly 6 rows above the cards (Where chat is printed)
	chat_height = math.ceil(rows_needed * 12) + 5

	hand_blocks = []
	for i in human_player.hands['hand']:
		hand_blocks.append(modDisp.as_block(i, aslist=True))

	hand_display = modList.merge_alternate(hand_blocks, endchar="list")

	startrow = 0

	curr_line = ""
	for i in range(0, rows_needed):
		for z in hand_display:
			for y in range(startrow, max_cards+startrow):
				if y < len(z):
					if z == hand_display[0]:
						curr_line += f'{y:02}'
					else:
						curr_line += '  '
					curr_line += z[y]
			ui.line(curr_height, "change", curr_line)
			curr_height -= 1
			curr_line = ""
		startrow += max_cards
	ui.print()


while len(available) > 44:
	if turn:
		human_player.hands['hand'].append(deck[dealcard()])
	else:
		robot_player.hands['hand'].append(deck[dealcard()])
	turn = not turn

human_match_count = 0
robot_match_count = 0


def update_scores():
	global human_match_count
	global robot_match_count
	human_match_count = math.ceil(len(human_player.hands['matches']) / 2)
	human_hand_count = len(human_player.hands['hand'])
	robot_match_count = math.ceil(len(robot_player.hands['matches']) / 2)
	robot_hand_count = len(robot_player.hands['hand'])
	ui.line(chat_height-2, "change", "     PLAY   ROBO   DECK")
	ui.line(chat_height-3, "change", "HAND  {}     {}     {} "
									.format(f'{human_hand_count:02}', f'{robot_hand_count:02}', len(available)))
	ui.line(chat_height-4, "change", "WINS  {}     {}"
									.format(f'{human_match_count:02}', f'{robot_match_count:02}'))


while True:
	# -- Win conditions --
	# If human player's hand is empty
	if len(human_player.hands['hand']) < 1:
		send(system, "Human hand exhausted! Ending game.")
		human_player.hands['hand'] = human_player.hands['matches']
		printhand()
		break
	# If robot player's hand is empty
	if len(robot_player.hands['hand']) < 1:
		send(system, "Robot hand exhausted! Ending game.")
		human_player.hands['hand'] = human_player.hands['matches']
		printhand()
		break
	# If deck is empty
	if len(available) < 0:
		send(system, "Deck exhausted! Ending game.")
		human_player.hands['hand'] = human_player.hands['matches']
		printhand()
		break

	# -- Match checking --
	# Check for matches in the player's hand.
	for c1 in human_player.hands['hand']:
		for c2 in human_player.hands['hand']:
			if c1 != c2 and rankcheck(c1) == rankcheck(c2) and colorcheck(c1) == colorcheck(c2):
				send(human_player, "Match in my hand.")
				human_player.hands['matches'].extend((c1, c2))
				human_player.hands['hand'] = [e for e in human_player.hands['hand'] if e not in (c1, c2)]
				update_scores()
	# Check for matches in the robot's hand.
	for c1 in robot_player.hands['hand']:
		for c2 in robot_player.hands['hand']:
			if c1 != c2 and rankcheck(c1) == rankcheck(c2) and colorcheck(c1) == colorcheck(c2):
				send(robot_player, "Got a match here!")
				robot_player.hands['matches'].extend((c1, c2))
				robot_player.hands['hand'] = [e for e in robot_player.hands['hand'] if e not in (c1, c2)]
				update_scores()

	printhand()
	# Update scores
	update_scores()


	gofish = True
	if turn:
		select = "Not a number!"
		while not modHelper.isinteger(select) or int(select) > len(human_player.hands['hand'])-1:
			select = input("Pick a card to play> ")
			if modHelper.isinteger(select) and int(select) > len(human_player.hands['hand'])-1:
				print("That number is too big!")
			if not modHelper.isinteger(select):
				print("Need to input a number!")
		select = int(select)
		send(human_player, "Do you have a {} {}?"
										.format(colorcheck(human_player.hands['hand'][select]), rankcheck(human_player.hands['hand'][select])))

		for x in robot_player.hands['hand']:
			if rankcheck(x) == rankcheck(human_player.hands['hand'][select]) and colorcheck(x) == colorcheck(human_player.hands['hand'][select]):
				gofish = False
				human_player.hands['matches'].extend((x, human_player.hands['hand'][select]))
				robot_player.hands['hand'] = [e for e in robot_player.hands['hand'] if e not in (x, '')]
				human_player.hands['hand'] = [e for e in human_player.hands['hand'] if e not in (human_player.hands['hand'][select])]
				time.sleep(1)
				send(robot_player, "Yeah, here you go.")
				time.sleep(1)
				update_scores()
				break

		if gofish:
			time.sleep(1)
			send(robot_player, "Sorry, I don't. Go fish.")
			card_in = dealcard()
			if card_in is not False:
				human_player.hands['hand'].append(deck[card_in])

		turn = not turn
	else:
		select = random.randrange(0, len(robot_player.hands['hand']))
		time.sleep(2)
		send(robot_player, "Got a {} {}?"
							.format(colorcheck(robot_player.hands['hand'][select]), rankcheck(robot_player.hands['hand'][select])))
		gofish = True
		for x in human_player.hands['hand']:
			if rankcheck(x) == rankcheck(robot_player.hands['hand'][select]) and colorcheck(x) == colorcheck(robot_player.hands['hand'][select]):
				gofish = False
				robot_player.hands['matches'].extend((x, robot_player.hands['hand'][select]))
				robot_player.hands['hand'] = [e for e in robot_player.hands['hand'] if e not in (robot_player.hands['hand'][select])]
				human_player.hands['hand'] = [e for e in human_player.hands['hand'] if e not in (x, '')]
				time.sleep(1)
				send(human_player, "Yup, here you go.")
				time.sleep(1)
				update_scores()
				time.sleep(2)
				break
		if gofish:
			time.sleep(1)
			send(human_player, "Don't have it, Go fish.")
			card_in = dealcard()
			if card_in is not False:
				robot_player.hands['hand'].append(deck[card_in])

		turn = not turn

if human_match_count == robot_match_count:
	send(system, "There was a tie!")
elif human_match_count > robot_match_count:
	send(system, "You won! Congratulations!")
elif robot_match_count > human_match_count:
	send(system, "You lost! Try again!")
ui.print()

input("Press enter to exit>")
