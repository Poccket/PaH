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
human_player = modPlayers.Player("Player", "LIGHTGREEN", {'hand': [], 'matches': []})
human_color = 1
robot_player = modPlayers.Player("Robot", "LIGHTRED", {'hand': [], 'matches': []})
robot_color = 0
system = modPlayers.Player("System", groups=['system'])

deck = modFile.read_list("decks/cardFrench.txt")

# Some setting definitions
turn = True
control_scheme = True
difficulty = 1
red_color = 0
blk_color = 3
ck = ["LIGHTRED", "LIGHTGREEN", "LIGHTBLUE", "LIGHTWHITE"]

resetting = False
prev_query = 0
diff = ["Easy", "Normal", "Hard"]
overall_scores = {}


def reset_scores():
    global overall_scores
    overall_scores = {
        "wins": 0,
        "losses": 0,
        "bluffs": 0,
        "bluffswon": 0,
        "matches": 0,
    }


def reset_settings():
    global control_scheme
    global turn
    global difficulty
    global human_color
    global robot_color
    global red_color
    global blk_color
    control_scheme = True
    turn = True
    difficulty = 1
    human_color = 1
    robot_color = 0
    red_color = 0
    blk_color = 3


reset_scores()

try:
    f_cont = modFile.read_list('gofish.score')
    scores = [int(s) for s in f_cont[0].split() if s.isdigit()]
    if len(scores) >= 5:
        overall_scores["wins"] = scores[0]
        overall_scores["losses"] = scores[1]
        overall_scores["bluffs"] = scores[2]
        overall_scores["bluffswon"] = scores[3]
        overall_scores["matches"] = scores[4]
    setts = [int(s) for s in f_cont[1].split() if s.isdigit()]
    if len(setts) >= 7:
        control_scheme = (bool(setts[0]) if setts[0] in [0, 1] else True)
        turn = (bool(setts[1]) if setts[1] in [0, 1] else True)
        difficulty = (setts[2] if setts[2] in [0, 1, 2] else 1)
        human_color = (setts[3] if setts[3] in [0, 1, 2] else 1)
        robot_color = (setts[4] if setts[4] in [0, 1, 2] else 0)
        red_color = (setts[5] if setts[5] in [0, 1, 2, 3] else 0)
        blk_color = (setts[6] if setts[6] in [0, 1, 2, 3] else 3)
except (FileNotFoundError, IndexError):
    f = open('gofish.score', 'w')
    f.write('w 0 l 0 bm 0 bw 0 m 0\n' +
            'inpt 1 turn 1 diff 1 col0 1 col1 0 col2 1 col3 4')
    f.close()


def score_file():
    _f = open('gofish.score', 'w')
    _f.write('w ' + str(overall_scores["wins"]) +
             ' l ' + str(overall_scores["losses"]) +
             ' bm ' + str(overall_scores["bluffs"]) +
             ' bw ' + str(overall_scores["bluffswon"]) +
             ' m ' + str(overall_scores["matches"]) + '\n' +
             'inpt ' + str(int(control_scheme)) +
             ' turn ' + str(int(turn)) +
             ' diff ' + str(difficulty) +
             ' col0 ' + str(human_color) +
             ' col1 ' + str(robot_color) +
             ' col2 ' + str(red_color) +
             ' col3 ' + str(blk_color))
    _f.close()


def menu():
    global turn
    global control_scheme
    global difficulty
    global human_color
    global robot_color
    global red_color
    global blk_color
    menu_finish = True
    menu_index = 0
    menu_select = 0
    menu_prompt = "You are about to exit the game"
    while menu_finish:
        ui_mid = math.floor(ui.height / 2.5)
        ui.clean()
        score_file()

        settings = {
            "input_type": ["", "Typing", "Arrow Keys", int(control_scheme)],
            "turn_order": ["", "Robot", "Human", int(turn)],
            "difficulty": ["", "Easy", "Medium", "Hard", difficulty],
            "self_color": ["", "Red", "Green", "Blue", human_color],
            "robo_color": ["", "Red", "Green", "Blue", robot_color],
            "redc_color": ["", "Red", "Green", "Blue", "White", red_color],
            "blkc_color": ["", "Red", "Green", "Blue", "White", blk_color],
        }
    
        for key, setting in settings.items():
            output = ""
            for index, option in enumerate(setting):
                if option in [setting[0], setting[-1]]:
                    continue
                if index-1 == setting[-1]:
                    output += "[" + option + "]"
                else:
                    output += " " + option + " "
            setting[0] = output
    
        menus = [{
            "items": ["Go Fish!",  # Title
                      "-- Start            --",
                      "-- Settings         --",
                      "-- Stats            --",
                      "-- Quit             --"
                      ],
            "select": [1, 2, 3, 4],
            "back": None,
            "hints": ["Starts a game",
                      "Options for gameplay",
                      "Statistics and scores",
                      "Exits the program"]
        }, {
            "items": ["Statistics",
                      "-- Matches won      >> " + str(overall_scores["wins"]),
                      "-- Matches lost     >> " + str(overall_scores["losses"]),
                      "-- Total matches    >> " + str(overall_scores["wins"] + overall_scores["losses"]),
                      "-- Bluffs won       >> " + str(overall_scores["bluffswon"]),
                      "-- Total bluffs     >> " + str(overall_scores["bluffs"]),
                      "-- Total matches    >> " + str(overall_scores["matches"]),
                      "-- Go back to menu  -- ",
                      "-- Reset scores     -- "
                      ],
            "select": [7, 8],
            "back": 7,
            "hints": ["Return to the main menu", "Reset ALL scores to ZERO"]
        }, {
            "items": ["Settings",
                      "-- Resize Screen    >> " + str(ui.width) + "x" + str(ui.height),
                      "-- Input type       >> " + settings["input_type"][0],
                      "-- Turn order       >> " + settings["turn_order"][0],
                      "-- Difficulty       >> " + settings["difficulty"][0],
                      "-- Human color      >> " + settings["self_color"][0],
                      "-- Robot color      >> " + settings["robo_color"][0],
                      "-- Red card color   >> " + settings["redc_color"][0],
                      "-- Black card color >> " + settings["blkc_color"][0],
                      "-- Go back to menu  -- ",
                      "-- Reset settings   -- "
                      ],
            "select": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "back": 9,
            "hints": ["Changes the resolution, use when you resize your window",
                      "Type in your awnsers, or select with the arrow keys",
                      "Select who goes first",
                      "Difficulty changes bluff chances and punishments",
                      "The color of your name in the game chat",
                      "The color of robots in the game chat",
                      "The color of red cards in your hand",
                      "The color of black cards in your hand",
                      "Return to the main menu",
                      "Reset ALL settings to defaults"]
        }, {
            "items": ["Title",
                      "Are you sure you want to do that?",
                      "-- Yes, I'm sure.   -- ",
                      "-- No, I'm not.     -- "
                      ],
            "select": [2, 3],
            "back": 3,
            "hints": ["", ""]
        }]
        
        if menu_select > len(menus[menu_index]["select"])-1:
            menu_select = 0
        elif menu_select < 0:
            menu_select = ((len(menus[menu_index]["select"]))-1)
    
        for index, item in enumerate(menus[menu_index]["items"]):
            if menu_index == 3 and index == 0:
                item = menu_prompt
            if index == menus[menu_index]["select"][menu_select]:
                item = modUI.colors["LIGHTGREEN"] + item[:22] + modUI.colors["LIGHTBLUE"]\
                       + item[22:] + modUI.colors["RESET"]
                item = item.replace('--', '[[', 1)
                item = item.replace('--', ']]')
            elif index in [0, menus[menu_index]["back"]]:
                item = modUI.colors["LIGHTRED"] + item + modUI.colors["RESET"]
            else:
                item.replace('[[', '--')
                item.replace(']]', '--')
            for num in range(0, (math.floor(ui.width / 2) - 24)):
                item = " " + item
            ui.line(ui_mid, "insert", item)
        if menus[menu_index]["hints"][menu_select] != "":
            item = menus[menu_index]["hints"][menu_select]
            for num in range(0, (math.floor(ui.width / 2) - 24)):
                item = " " + item
            ui.line(ui_mid-2, "change", item)
        ui.print()
        key_press = None
        while key_press not in ["up", "down", "left", "right", "select"]:
            key_press = modGetch.get_arrow()
        if key_press == 'up':
            menu_select -= 1
        elif key_press == 'down':
            menu_select += 1
        elif key_press == 'left':
            if menu_index == 2:
                if menu_select == 1:
                    control_scheme = not control_scheme
                if menu_select == 2:
                    turn = not turn
                if menu_select == 3:
                    if difficulty == 0:
                        difficulty = 2
                    else:
                        difficulty -= 1
                if menu_select == 4:
                    if human_color == 0:
                        human_color = 2
                    else:
                        human_color -= 1
                    human_player.color = ck[human_color]
                if menu_select == 5:
                    if robot_color == 0:
                        robot_color = 2
                    else:
                        robot_color -= 1
                    robot_player.color = ck[robot_color]
                if menu_select == 6:
                    if red_color == 0:
                        red_color = 3
                    else:
                        red_color -= 1
                if menu_select == 7:
                    if blk_color == 0:
                        blk_color = 3
                    else:
                        blk_color -= 1
        elif key_press in ['right', 'select']:
            if menus[menu_index]["select"][menu_select] == menus[menu_index]["back"]:
                menu_index = 0
                continue
            elif menu_index == 0:
                if menu_select == 0:
                    menu_finish = not menu_finish
                elif menu_select == 1:
                    menu_index = 2
                elif menu_select == 2:
                    menu_index = 1
                elif menu_select == 3:
                    menu_index = 3
                    menu_prompt = "You are about to exit the game!"
            elif menu_index == 1:
                if menu_select == 1:
                    menu_index = 3
                    menu_prompt = "You are about to erase your scores!"
            elif menu_index == 2:
                if menu_select == 0:
                    ui.width, ui.height = ui.auto_size()
                if menu_select == 1:
                    control_scheme = not control_scheme
                if menu_select == 2:
                    turn = not turn
                if menu_select == 3:
                    if difficulty == 2:
                        difficulty = 0
                    else:
                        difficulty += 1
                if menu_select == 4:
                    if human_color == 2:
                        human_color = 0
                    else:
                        human_color += 1
                    human_player.color = ck[human_color]
                if menu_select == 5:
                    if robot_color == 2:
                        robot_color = 0
                    else:
                        robot_color += 1
                    robot_player.color = ck[robot_color]
                if menu_select == 6:
                    if red_color == 3:
                        red_color = 0
                    else:
                        red_color += 1
                if menu_select == 7:
                    if blk_color == 3:
                        blk_color = 0
                    else:
                        blk_color += 1
                if menu_select == 9:
                    menu_index = 3
                    menu_prompt = "You are about to reset your settings!"
            elif menu_index == 3:
                if menu_select == 0:
                    if "exit" in menu_prompt:
                        sys.exit()
                    elif "erase" in menu_prompt:
                        reset_scores()
                        menu_index = 1
                    elif "reset" in menu_prompt:
                        reset_settings()
                        menu_index = 2


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
        messages.append(modUI.colors[usr.color] + "<" + usr.name + "> " + modUI.colors["RESET"] + msg)
        if len(messages) > 20:
            del messages[0]
        for a in range(chat_height, ui.height):
            ui.line(a, "clear")
    ui.line(chat_height, "clear")
    ui.line(chat_height-5, "clear")
    for msg in messages:
        ui.line(chat_height, "insert", msg)
    ui.print()


def printhand(selected: [list, int] = None, controls: str = "..."):
    global curr_height
    global chat_height
    global max_cards
    if len(human_player.hands['hand']) <= 0:
        return False
    # -- UI Variables --
    # The amount of cards that can fit on one row
    max_cards = math.floor(ui.width / 14)
    # The amount of rows needed to display all of the player's cards
    rows_needed = math.ceil(len(human_player.hands['hand']) / max_cards)
    # The height that the cards will start printing at.
    curr_height = math.ceil(rows_needed * 12)-1
    # Exactly 6 rows above the cards (Where chat is printed)
    chat_height = math.ceil(rows_needed * 12) + 6

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
                    if colorcheck(human_player.hands['hand'][y]) == "red":
                        curr_line += modUI.colors[ck[red_color]]
                    else:
                        curr_line += modUI.colors[ck[blk_color]]
                    curr_line += z[y] + modUI.colors["RESET"]
            ui.line(curr_height, "change", curr_line)
            curr_height -= 1
            curr_line = ""
        startrow += max_cards
    ui.line(0, "insert", controls)
    update_scores()
    send(None, None)


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
    global overall_scores
    if human_match_count == robot_match_count:
        send(system, "There was a tie!")
    elif human_match_count > robot_match_count:
        send(system, "You won! Congratulations!")
        overall_scores["wins"] += 1
    elif robot_match_count > human_match_count:
        send(system, "You lost! Try again!")
        overall_scores["losses"] += 1
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
    turn = True
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
    menu()

    while len(available) > 44:
        if turn:
            human_player.hands['hand'].append(deck[dealcard()])
        else:
            robot_player.hands['hand'].append(deck[dealcard()])
        turn = not turn

    human_match_count = 0
    robot_match_count = 0
    send(system, ("You go first, pick a card to play." if turn else "Robot's up first, wait for your turn."))
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
                    printhand(select, "left/right to move / enter to select / m to match / q to quit game")
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
                            match_selects = [select, -1]
                            curr_select = 0
                            while not finish:
                                printhand(match_selects, "left/right to move / enter to select / m to stop matching")
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
                                        match_selects[1] = 1 if match_selects[0] == 0 else 0
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
                                            overall_scores["matches"] += 1
                                            match_selects = [0, -1]
                                            curr_select = 0
                                        else:
                                            send(system, "That's not a match!")
                                if keyp_2 == 'match':
                                    select = match_selects[curr_select]
                                    break

            elif not control_scheme:
                select = "None, but not None"
                while True:
                    printhand(None, "enter number to select / m to match / q to quit")
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
                            printhand(None, "enter number to select / m to stop matching")
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
                                        overall_scores["matches"] += 1
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
                    overall_scores["matches"] += 1
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
            select = prev_query
            max_rolls = 0
            while select == prev_query or max_rolls < 10:
                select = random.randrange(0, len(robot_player.hands['hand']))
                max_rolls += 1
            prev_query = select
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
                    overall_scores["bluffs"] += 1
                    send(human_player, get_msg("nothave"))
                    send(robot_player, "Hmm..")
                    time.sleep(3)
                    bluff_chance = (9*difficulty) if difficulty > 0 else 3
                    if random.randrange(0, bluff_chance) > 2 if difficulty > 0 else 1:
                        send(robot_player, "You're bluffing!")
                        time.sleep(1)
                        if difficulty > 0 and len(human_player.hands['matches']) >= 2*difficulty:
                            human_player.hands['matches'] = \
                                human_player.hands['matches'][:len(human_player.hands['matches'])-(2*difficulty)]
                            send(system, "You got caught! You lost " + "a match!" if difficulty == 1 else "2 matches!")
                        elif difficulty == 2 and len(human_player.hands['matches']) >= 2:
                            human_player.hands['matches'] = \
                                human_player.hands['matches'][:len(human_player.hands['matches']) - 2]
                            send(system, "You got caught! You lost a match!")
                        elif difficulty == 0:
                            send(system, "You got caught! :(")
                        else:
                            send(system, "You got caught, but you have no matches!")
                    else:
                        time.sleep(2)
                        overall_scores["bluffswon"] += 1
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
