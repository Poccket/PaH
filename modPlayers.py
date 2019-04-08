"""Holds a class for players"""
players = 0
# This is just a count for amount of players.


class Player:
    """A player with minimal functionality"""
    def __init__(self, name: str = "", hands: dict = None, groups: list = None):
        """
        Initializes a player.

        :param name: The username for the player
        :param hands: A dictionary containing the players hands
        :param groups: The groups that the player is part of
        """
        global players
        players += 1
        # Add one to the player count
        self.hands = hands
        if groups is None:
            self.groups = ['default']
        else:
            self.groups = groups
        # If there's no groups, we just give them a default group
        if name is not "":
            self.name = name
        else:
            self.name = "Player" + str(players)
        # And here's a fallback name, if one isn't defined
