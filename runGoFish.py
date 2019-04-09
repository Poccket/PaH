import modDisp
import modFile
import modList
import modUI
import modPlayers
import modHelper
import random
import math
import time
import modGetch
import sys


ui = modUI.Screen()
human_player = modPlayers.Player("Player", {'hand': [], 'matches': []})
robot_player = modPlayers.Player("Robot", {'hand': [], 'matches': []})
system = modPlayers.Player("System", groups=['system'])

deck = modFile.read_list("decks/cardFrench.txt")
turn = True
control_scheme = True
try:
    f = open('gofish.score', 'r')
    f_cont = f.read()
    f.close()
    scores = [int(s) for s in f_cont.split() if s.isdigit()]
    if len(scores) >= 2 and modHelper.is_int(scores[0]) and modHelper.is_int(scores[1]):
        wins_in_session = scores[0]
        loss_in_session = scores[1]
    else:
        wins_in_session = 0
        loss_in_session = 0
except FileNotFoundError:
    f = open('gofish.score', 'w')
    f.write('w 0 l 0')
    f.close()
    wins_in_session = 0
    loss_in_session = 0


def score_file():
    f = open('gofish.score', 'w')
    f.write('w ' + str(wins_in_session) + ' l ' + str(loss_in_session))
    f.close()


def menu_print(selection: int = 1):
    ui_mid = math.floor(ui.height / 2)
    ui.clean()
    menu_items = ["Go Fish!",
                  "-- Start   --",
                  "-- Resize: -- " + str(ui.width) + "x" + str(ui.height),
                  "-- Input:  -- ",
                  "-- Quit    --",
                  "-- Wins:   -- " + str(wins_in_session) + " / " + str(loss_in_session), "",
                  "up/down and enter to select"]
    menu_items[3] = menu_items[3] + ("Arrow" if control_scheme else "Type")
    for index, item in enumerate(menu_items):
        if index == selection:
            item = item.replace('--', '[[', 1)
            item = item.replace('--', ']]')
        else:
            item.replace('[[', '--')
            item.replace(']]', '--')
        for num in range(0, (math.floor(ui.width / 2) - 24)):
            item = " " + item
        ui.line(ui_mid, "insert", item)
    ui.print()


suits = {
    "colors": {
        "Heart": "red",
        "Diamond": "red",
        "Club": "black",
        "Spade": "black",
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

rand_messages = {
        "query":     ["Got a ", "Have a ", "What about a ", "Do you have a "],
        "handmatch": ["Got a match!", "Match in my hand", "Match! Nice.", "Match here!"],
        "have":      [["Yeah, ", "Yup, ", "Mhm, ", "Nice, ", "Got me, "],
                      ["here you go", "take it", "here it is", "it's here", "I got it"]],
        "nothave":   [["Sorry, ", "Nope, ", "Afraid not, ", "No dice, ", "No luck"],
                      ["go fish", "gotta draw", "don't got it", "not in my hand"]]
}


def get_msg(msg_type):
    if msg_type not in ["query", "handmatch", "have", "nothave"]:
        return False
    if msg_type == "query" or msg_type == "handmatch":
        return rand_messages[msg_type][random.randrange(0, len(rand_messages[msg_type]))]
    if msg_type == "have" or msg_type == "nothave":
        return (rand_messages[msg_type][0][random.randrange(0, len(rand_messages[msg_type]))] +
                rand_messages[msg_type][1][random.randrange(0, len(rand_messages[msg_type][1]))])


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
    if msg is not None:
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


def printhand(selected: [list, int] = None):
    global curr_height
    global chat_height
    global max_cards
    # -- UI Variables --
    # The amount of cards that can fit on one row
    max_cards = math.floor(ui.width / 14)
    # The amount of rows needed to display all of the player's cards
    rows_needed = math.ceil(len(human_player.hands['hand']) / max_cards)
    # The height that the cards will start printing at.
    curr_height = math.ceil(rows_needed * 12)-1
    # Exactly 6 rows above the cards (Where chat is printed)
    chat_height = math.ceil(rows_needed * 12) + 5

    if type(selected) != list:
        selected = [selected]
    hand_blocks = []
    for a, y in enumerate(human_player.hands['hand']):
        if a in selected:
            hand_blocks.append(modDisp.as_block(y, aslist=True, blockset="double"))
        else:
            hand_blocks.append(modDisp.as_block(y, aslist=True, blockset="light"))

    hand_display = modList.merge_alternate(hand_blocks, 'm')

    startrow = 0

    curr_line = ""
    ui.clean()
    for i in range(0, rows_needed):
        for z in hand_display:
            for y in range(startrow, max_cards+startrow):
                if y < len(z):
                    if z == hand_display[0] and not control_scheme:
                        curr_line += f'{y:02}'
                    else:
                        curr_line += '  '
                    curr_line += z[y]
            ui.line(curr_height, "change", curr_line)
            curr_height -= 1
            curr_line = ""
        startrow += max_cards
    update_scores()
    send(None, None)
    ui.print()


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


def end_score():
    global wins_in_session
    global loss_in_session
    if human_match_count == robot_match_count:
        send(system, "There was a tie!")
    elif human_match_count > robot_match_count:
        send(system, "You won! Congratulations!")
        wins_in_session += 1
    elif robot_match_count > human_match_count:
        send(system, "You lost! Try again!")
        loss_in_session += 1
    input("Press enter to view matches ]")
    human_player.hands['hand'] = human_player.hands['matches']
    if len(human_player.hands['matches']) != 0:
        ui.height = (math.ceil(len(human_player.hands['matches']) / max_cards) + 1) * 12
        ui.clean()
        printhand()
    else:
        print("No matches! :(")


while True:
    score_file()
    ui.clean(True)
    abort_game = False
    available = list(range(len(deck)))
    human_player.hands = {'hand': [], 'matches': []}
    robot_player.hands = {'hand': [], 'matches': []}
    messages = []
    chat_height = 0
    curr_height = 0
    max_cards = 0

    finish = False
    select = 1
    while not finish:
        menu_print(select)
        keyp = None
        while keyp not in ['up', 'down', 'select']:
            keyp = modGetch.get_arrow()
        if keyp == 'up':
            if select > 1:
                select = select - 1
            else:
                select = 4
        if keyp == 'down':
            if select < 4:
                select = select + 1
            else:
                select = 1
        if keyp == 'select':
            if select == 1:
                finish = not finish
            if select == 2:
                ui.width, ui.hieght = ui.auto_size()
            if select == 3:
                control_scheme = not control_scheme
            if select == 4:
                sys.exit()

    while len(available) > 44:
        if turn:
            human_player.hands['hand'].append(deck[dealcard()])
        else:
            robot_player.hands['hand'].append(deck[dealcard()])
        turn = not turn

    human_match_count = 0
    robot_match_count = 0
    while not abort_game:
        # -- Win conditions --
        # If human player's hand is empty
        if len(human_player.hands['hand']) < 1:
            send(system, "Human hand exhausted! Ending game.")
            break
        # If robot player's hand is empty
        if len(robot_player.hands['hand']) < 1:
            send(system, "Robot hand exhausted! Ending game.")
            break
        # If deck is empty
        if len(available) < 0:
            send(system, "Deck exhausted! Ending game.")
            break

        # -- Match checking --
        # Check for matches in the robot's hand.
        for c1 in robot_player.hands['hand']:
            for c2 in robot_player.hands['hand']:
                if c1 != c2 and rankcheck(c1) == rankcheck(c2) and colorcheck(c1) == colorcheck(c2):
                    send(robot_player, get_msg("handmatch"))
                    robot_player.hands['matches'].extend((c1, c2))
                    robot_player.hands['hand'] = [e for e in robot_player.hands['hand'] if e not in (c1, c2)]
                    update_scores()

        printhand()
        # Update scores
        update_scores()

        gofish = True
        if turn:
            loop = False
            if control_scheme:
                select = 0
                finish = False
                while not finish:
                    printhand(select)
                    print("left/right to move / enter to select / m to match / q to quit game")
                    keyp_2 = None
                    while keyp_2 not in ['right', 'left', 'select', 'escape', 'match']:
                        keyp_2 = modGetch.get_arrow()
                    if keyp_2 == 'left':
                        if select > 0:
                            select = select - 1
                        else:
                            select = len(human_player.hands['hand'])-1
                    if keyp_2 == 'right':
                        if select < len(human_player.hands['hand'])-1:
                            select = select + 1
                        else:
                            select = 0
                    if keyp_2 == 'select':
                        finish = not finish
                    if keyp_2 == 'escape':
                        printhand(select)
                        conf = None
                        while conf not in ['y', 'n']:
                            conf = input("are you sure you want to exit? [y/n] ")
                            conf = conf.lower()[:1]
                        if conf == 'y':
                            abort_game = True
                            break
                        else:
                            continue

                    if keyp_2 == 'match':
                        if control_scheme:
                            match_selects = [0, -1]
                            curr_select = 0
                            while not finish:
                                printhand(match_selects)
                                print("left/right to move / enter to select / m to stop matching")
                                keyp_2 = None
                                while keyp_2 not in ['right', 'left', 'select', 'match']:
                                    keyp_2 = modGetch.get_arrow()
                                if keyp_2 == 'left':
                                    if match_selects[curr_select] > 0:
                                        match_selects[curr_select] = match_selects[curr_select] - 1
                                    else:
                                        match_selects[curr_select] = len(human_player.hands['hand']) - 1
                                    if match_selects[0] == match_selects[1]:
                                        if match_selects[curr_select] > 0:
                                            match_selects[curr_select] = match_selects[curr_select] - 1
                                        else:
                                            match_selects[curr_select] = len(human_player.hands['hand']) - 1
                                if keyp_2 == 'right':
                                    if match_selects[curr_select] < len(human_player.hands['hand']) - 1:
                                        match_selects[curr_select] = match_selects[curr_select] + 1
                                    else:
                                        match_selects[curr_select] = 0
                                    if match_selects[0] == match_selects[1]:
                                        if match_selects[curr_select] < len(human_player.hands['hand']) - 1:
                                            match_selects[curr_select] = match_selects[curr_select] + 1
                                        else:
                                            match_selects[curr_select] = 0
                                if keyp_2 == 'select':
                                    if curr_select == 0:
                                        curr_select += 1
                                        time.sleep(1)
                                    else:
                                        if human_player.hands['hand'][match_selects[0]] !=\
                                                human_player.hands['hand'][match_selects[1]] and \
                                                rankcheck(human_player.hands['hand'][match_selects[0]]) ==\
                                                rankcheck(human_player.hands['hand'][match_selects[1]]) and \
                                                colorcheck(human_player.hands['hand'][match_selects[0]]) ==\
                                                colorcheck(human_player.hands['hand'][match_selects[1]]):
                                            send(human_player, get_msg("handmatch"))
                                            human_player.hands['matches'].extend(
                                                (human_player.hands['hand'][match_selects[0]],
                                                 human_player.hands['hand'][match_selects[1]]))
                                            human_player.hands['hand'] = [e for e in human_player.hands['hand']
                                                                          if e not in (
                                                                          human_player.hands['hand'][match_selects[0]],
                                                                          human_player.hands['hand'][match_selects[1]])]
                                            update_scores()
                                            match_selects = [0, -1]
                                            curr_select = 0
                                        else:
                                            send(system, "That's not a match!")
                                if keyp_2 == 'match':
                                    break

            elif not control_scheme:
                select = "None, but not None"
                while True:
                    printhand()
                    print("enter number to select / m to match / q to quit")
                    select = input("Enter selection: ")
                    if modHelper.is_int(select) and int(select) in list(range(0, len(human_player.hands['hand'])-1)):
                        break
                    if select == 'q':
                        conf = None
                        while conf not in ['y', 'n']:
                            conf = input("are you sure you want to exit? [y/n] ")
                            conf = conf.lower()[:1]
                        if conf == 'y':
                            abort_game = True
                            break
                        else:
                            continue
                    if select == 'm':
                        match_selects = [-1, -1]
                        curr_select = 0
                        finish = False
                        while not finish:
                            match_selects[curr_select] = "Like, it's None but it's not NONE, you know?"
                            printhand()
                            print("enter number to select / m to stop matching")
                            match_selects[curr_select] = input("Enter selection: ")
                            if modHelper.is_int(match_selects[curr_select]) and \
                                    int(match_selects[curr_select]) in \
                                    list(range(0, len(human_player.hands['hand']) - 1)):
                                if curr_select == 0:
                                    curr_select += 1
                                    time.sleep(1)
                                else:
                                    match_selects[0] = int(match_selects[0])
                                    match_selects[1] = int(match_selects[1])
                                    if human_player.hands['hand'][match_selects[0]] != \
                                            human_player.hands['hand'][match_selects[1]] and \
                                            rankcheck(human_player.hands['hand'][match_selects[0]]) == \
                                            rankcheck(human_player.hands['hand'][match_selects[1]]) and \
                                            colorcheck(human_player.hands['hand'][match_selects[0]]) == \
                                            colorcheck(human_player.hands['hand'][match_selects[1]]):
                                        send(human_player, get_msg("handmatch"))
                                        human_player.hands['matches'].extend(
                                            (human_player.hands['hand'][match_selects[0]],
                                             human_player.hands['hand'][match_selects[1]]))
                                        human_player.hands['hand'] = [e for e in human_player.hands['hand']
                                                                      if e not in (
                                                                          human_player.hands['hand'][match_selects[0]],
                                                                          human_player.hands['hand'][match_selects[1]])]
                                        update_scores()
                                        match_selects = [0, -1]
                                        curr_select = 0
                                    else:
                                        send(system, "That's not a match!")
                            if match_selects[curr_select] == 'm':
                                break
                # while not modHelper.is_int(select) or \
                #        int(select) not in list(range(0, len(human_player.hands['hand'])-1)):
                #    select = input("Enter selection:")
                if not abort_game:
                    select = int(select)
            if abort_game:
                break
            send(human_player, get_msg("query") + "{} {}?"
                                                  .format(colorcheck(human_player.hands['hand'][select]),
                                                          rankcheck(human_player.hands['hand'][select])))
            for x in robot_player.hands['hand']:
                if rankcheck(x) == rankcheck(human_player.hands['hand'][select]) and \
                        colorcheck(x) == colorcheck(human_player.hands['hand'][select]):
                    gofish = False
                    human_player.hands['matches'].extend((x, human_player.hands['hand'][select]))
                    robot_player.hands['hand'] = [e for e in robot_player.hands['hand'] if e not in (x, '')]
                    human_player.hands['hand'] = [e for e in human_player.hands['hand']
                                                  if e not in (human_player.hands['hand'][select])]
                    time.sleep(1)
                    send(robot_player, get_msg("have"))
                    time.sleep(1)
                    update_scores()
                    break

            if gofish:
                time.sleep(1)
                send(robot_player, get_msg("nothave"))
                card_in = dealcard()
                if card_in is not False:
                    input("Press enter to draw ]")
                    human_player.hands['hand'].append(deck[card_in])

            turn = not turn
        else:
            select = random.randrange(0, len(robot_player.hands['hand']))
            time.sleep(2)
            send(robot_player, get_msg("query") + "{} {}?"
                 .format(colorcheck(robot_player.hands['hand'][select]), rankcheck(robot_player.hands['hand'][select])))
            gofish = True
            removeMe = None
            for w, x in enumerate(human_player.hands['hand']):
                if rankcheck(x) == rankcheck(robot_player.hands['hand'][select]) and \
                        colorcheck(x) == colorcheck(robot_player.hands['hand'][select]):
                    gofish = False
                    removeMe = w
                    break

            conf = None
            while conf not in ['y', 'n']:
                conf = input("Do you have a {} {}? [y/n] "
                             .format(colorcheck(robot_player.hands['hand'][select]),
                                     rankcheck(robot_player.hands['hand'][select])))
                conf = conf.lower()[:1]
            if gofish:
                if conf == 'y':
                    send(system, "Erm.. afraid you actually don't.")
                    time.sleep(1)
                    send(human_player, get_msg("nothave"))
                if conf == 'n':
                    send(human_player, get_msg("nothave"))
            else:
                if conf == 'y':
                    send(human_player, get_msg("have"))
                if conf == 'n':
                    send(human_player, get_msg("nothave"))
                    send(robot_player, "Hmm..")
                    time.sleep(3)
                    if random.randrange(0, 10) > 6:
                        send(robot_player, "You're bluffing!")
                        time.sleep(1)
                        send(system, "You got caught!")
                    else:
                        time.sleep(2)
                        send(system, "You got away with the bluff!")
                        gofish = True
            time.sleep(1)

            if gofish:
                card_in = dealcard()
                if card_in is not False:
                    robot_player.hands['hand'].append(deck[card_in])
            else:
                robot_player.hands['matches'].extend((human_player.hands['hand'][removeMe],
                                                      robot_player.hands['hand'][select]))
                robot_player.hands['hand'] = [e for e in robot_player.hands['hand']
                                              if e not in (robot_player.hands['hand'][select])]
                human_player.hands['hand'] = [e for e in human_player.hands['hand']
                                              if e not in (human_player.hands['hand'][removeMe], '')]
            turn = not turn
    if not abort_game:
        end_score()
        input("Press enter to exit ]")
