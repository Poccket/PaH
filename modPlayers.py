players = 0


class Player:
	def __init__(self, name: str = "", hands: dict = None, groups: list = None):
		global players
		players += 1
		self.hands = hands
		if groups is None:
			self.groups = ['default']
		else:
			self.groups = groups
		if name is not "":
			self.name = name
		else:
			self.name = "Player" + str(players)
