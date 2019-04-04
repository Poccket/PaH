import os
import shutil

"""
This module contains functions for a very basic text-based output
"""


class Screen:
	def __init__(self, width=0, height=0, ui=[], clamp=True, clear=True, fill=True, reverse=False):
		"""
		Initializes the class 'Screen'

		:param width: The width of the class, if left alone will auto-detect
		:param height: The height of the class, if left alone will auto-detect
		:param ui: The array that contains all of the text to be displayed
		:param clamp: Whether or not to clamp the array to the size of the screen
		:param clear: Whether or not to clear the screen when printing
		:param fill: Whether or not to fill the array on __init__
		:param reverse: If set, 0 is the top of the screen.
		"""
		self.width = width
		self.height = height
		self.ui = ui
		self.clamp = clamp
		self.clear = clear
		self.reverse = reverse
		self.fill = fill
		if self.width == 0 and self.height == 0:
			self.width, self.height = self.auto_size()
		if self.fill:
			self.clean()

	@staticmethod
	def auto_size():
		"""
		Automatically gets the size of the Screen

		This method is called on startup, but is set here to allow calling outside of startup.

		:return: Width and height of terminal.
		"""
		return shutil.get_terminal_size((70, 100))

	@staticmethod
	def emptyscreen():
		"""
		Runs OS clear command.

		This method is called if self.clear is set when printing, but is set here to allow calling outside of that.

		:return: None
		"""
		os.system('cls' if os.name == 'nt' else 'clear')

	def line(self, line, method="", text="", andprint=False):
		"""
		Modifies a line depending on the method specified

		insert
			Inserts a line, creating a new line at the index specified.

		change
			Overwrites the line at the index specified, if no line is here, it creates one.

		delete
			Deletes the line at the index specified if it exists.

		clear
			Clears a line

		Will always return the line specified, even if there is no method set.

		:param line: Line to modify
		:param method: insert, change, delete, clear
		:param text: Text for insert or change methods
		:param andprint: Whether or not to print when calling
		:return: Returns line
		"""
		if method.lower() == 'insert':
			self.ui.insert(line, text)
		if method.lower() == 'change':
			if line < len(self.ui):
				self.ui[line] = text
			else:
				self.ui.insert(line, text)
		if method.lower() == 'delete':
			if self.ui[line]:
				del self.ui[line]
		if method.lower() == 'clear':
			if self.ui[line]:
				self.ui[line] = ""
			else:
				self.ui.insert(line, "")
		if andprint:
			self.print()
		return self.ui[line]

	def clamplines(self):
		"""
		Clamps the self.ui to only be as long as the height of the terminal

		This method removes all items that exceed this length.

		:return: None
		"""
		for i, x in reversed(list(enumerate(self.ui))):
			if i > self.height-2:
				del self.ui[i]

	def clean(self, andprint=False):
		"""
		This method empties the self.ui array.

		This method is included for ease, and to allow printing in the same line.

		:param andprint: Whether or not to print when calling
		:return: None
		"""
		self.ui = []
		if andprint:
			self.print()
		if self.fill:
			for i in range(0, self.height):
				self.ui.append("")

	def print(self):
		"""
		Prints the self.ui array, with 0 as the bottom unless 'reverse' is set.

		:return: None
		"""
		if self.clamp:
			self.clamplines()
		if self.clear:
			self.emptyscreen()
		if self.reverse:
			for x in self.ui:
				print(x)
		else:
			for x in reversed(self.ui):
				print(x)
