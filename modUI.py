import os
import shutil


class Screen:
	def __init__(self, width=0, height=0, ui=[], clamp=True, clear=True, fill=True):
		self.width = width
		self.height = height
		self.ui = ui
		self.clamp = clamp
		self.clear = clear
		if self.width == 0 and self.height == 0:
			self.width, self.height = self.auto_size()
		if fill:
			for i in range(0,self.height):
				self.ui.append("")

	@staticmethod
	def auto_size():
		return shutil.get_terminal_size((70, 100))

	@staticmethod
	def emptyscreen():
		os.system('cls' if os.name == 'nt' else 'clear')

	def changeline(self, text, line, andprint=False):
		if line < len(self.ui):
			self.ui[line] = text
		else:
			self.ui.insert(line, text)
		if andprint:
			self.print()

	def insertline(self, text, line, andprint=False):
		self.ui.insert(line, text)
		if andprint:
			self.print()

	def deleteline(self, line, andprint=False):
		del self.ui[line]
		if andprint:
			self.print()

	def emptyline(self, line, andprint=False):
		if self.ui[line]:
			self.ui[line] = ""
		if andprint:
			self.print()

	def clamplines(self):
		for i, x in reversed(list(enumerate(self.ui))):
			if i > self.height:
				del self.ui[i]

	def clean(self, andprint=False):
		self.ui = []
		if andprint:
			self.print()

	def print(self):
		if self.clamp:
			self.clamplines()
		if self.clear:
			self.emptyscreen()
		for x in reversed(self.ui):
			print(x)
