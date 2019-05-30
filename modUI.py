"""This module contains functions for a very basic text-based output"""
from typing import Union
import shutil
import os

colors = {
    "RED":          "\033[31m",
    "LIGHTRED":     "\033[1;31m",
    "GREEN":        "\033[32m",
    "LIGHTGREEN":   "\033[1;32m",
    "YELLOW":       "\033[33m",
    "LIGHTYELLOW":  "\033[1;33m",
    "BLUE":         "\033[34m",
    "LIGHTBLUE":    "\033[1;34m",
    "MAGENTA":      "\033[35m",
    "LIGHTMAGENTA": "\033[1;35m",
    "CYAN":         "\033[36m",
    "LIGHTCYAN":    "\033[1;36m",
    "WHITE":        "\033[97m",
    "LIGHTWHITE":   "\033[1;97m",
    "RESET":        "\033[0;0m",
}


class Screen:
    def __init__(self, width: int = 0, height: int = 0, ui: list = None, clamp: bool = True, clear: bool = True,
                 fill: bool = True, reverse: bool = False):
        """Initializes the class 'Screen'

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
        # If the width and height aren't set, automatically set them.
        if self.fill:
            self.clean()
        # If fill is set to true, run clean()

    @staticmethod
    def auto_size() -> os.terminal_size:
        """Automatically gets the size of the Screen

        This method is called on startup, but is set here to allow calling outside of startup.

        :return: Width and height of terminal.
        """
        return shutil.get_terminal_size((70, 100))
        # Returns the size of the terminal, but this actually isn't always accurate.
        # However it's accurate enough for us. We give the backup 70 and 100 here.

    @staticmethod
    def emptyscreen() -> int:
        """Runs OS clear command.

        This method is called if self.clear is set when printing, but is set here to allow calling outside of that.

        :return: 0 if successful
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        return 0
        # Literally just runs the system clear command.

    def line(self, index: int, mode: str = "", inp: str = "", andprint: bool = False) -> Union[str, None]:
        """Modifies an index depending on the mode specified

        insert
            Inserts an index, creating a new index at the index specified.

        change
            Overwrites at the index specified, if no index is here, it creates one.

        delete
            Deletes the index at the index specified if it exists.

        clear
            Clears an index

        Will always return the index specified, even if there is no mode set.

        :param index: Line to modify
        :param mode: insert, change, delete, clear
        :param inp: Text for insert or change modes
        :param andprint: Whether or not to print when calling
        :return: Returns index
        """
        if not isinstance(mode, str):
            raise TypeError("argument 'mode' must be str")
        mode = mode.lower()
        if mode not in ["insert", "change", "delete", "clear"]:
            raise ValueError("invalid mode: '" + mode + "'")
        # Right here we first check if 'mode' is a string, if not we throw a TypeError
        # Then we set mode to a lowercase version of itself, ie. 'M' becomes 'm'
        # Then we check if it's one of the valid modes, and if not, we throw a ValueError.

        if mode.lower() == 'insert':
            self.ui.insert(index, inp)
        # If the mode is 'insert', we just insert the line at the given index.

        if mode.lower() == 'change':
            if index < len(self.ui):
                self.ui[index] = inp
            else:
                self.ui.insert(index, inp)
        # If the mode is 'change', we check if the index exists, and if so, change it.
        # if it doesn't exist, we insert it.

        if mode.lower() == 'delete':
            if index < len(self.ui):
                del self.ui[index]
        # If the mode is 'delete', we check if the index exists.
        # If it does, we delete it.

        if mode.lower() == 'clear':
            if index < len(self.ui):
                self.ui[index] = " "
            else:
                self.ui.insert(index, " ")
        # If the mode is 'clear', we check if the index exists.
        # If it does we set it to a single space.
        # If not, we insert it, just to be nice.

        if andprint:
            self.print()
        # if 'andprint' is set, we print it as well.

        if index < len(self.ui):
            return self.ui[index]
        else:
            return None
        # If the index still exists, we return it, if not we return None

    def clamplines(self) -> int:
        """Clamps the self.ui to only be as long as the height of the terminal

        This method removes all items that exceed this length.

        :return: 0 if successful
        """
        for i, x in reversed(list(enumerate(self.ui))):
            if i > self.height:
                del self.ui[i]
        # First start a for loop, we use a reversed list of the enumerated list of ui.
        # Then we check if i is bigger than the height, if it is, we rid of it!
        return 0
        # Then we just return 0.

    def clean(self, andprint: bool = False) -> int:
        """This method empties the self.ui array.

        This method is included for ease, and to allow printing in the same line.

        :param andprint: Whether or not to print when calling
        :return: 0 if successful
        """
        self.ui = []
        # First we just absolutely clean the ui list.
        for i in range(0, self.height):
            self.ui.append("")
        # Then, for every number between 0 and the height, we add an empty string to the ui list!

        if andprint:
            self.print()
        # If they want us to print, then so be it!
        return 0
        # oh, and return 0.

    def print(self) -> int:
        """
        Prints the self.ui array, with 0 as the bottom unless 'reverse' is set.

        :return: 0 if successful
        """
        if self.clamp:
            self.clamplines()
        # If clamp is set, then clamp!
        if self.clear:
            self.emptyscreen()
        # If clear is set, then clear!

        """
        if self.reverse:
            for x in self.ui:
                print(x)
        # And if reverse it set, then print the ui list in reverse, where 0 is the bottom of the screen!
        else:
            for x in reversed(self.ui):
                print(x)
        # If it's not, then print the ui list where 0 is the top!
        """  # Old code, just in case.

        if self.reverse:  # If reverse is set
            print('\n'.join(self.ui))  # Print list joined into a string, with each item seperated by newlines
        else:  # If it's not
            print('\n'.join(self.ui[::-1]))  # Do that same thing with a reversed list.
        return 0
        # Finally we return 0!
