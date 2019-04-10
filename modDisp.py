"""Contains functions for creating display art."""
# TODO: Update to fit guideline.
from typing import List


block = {
    'horiz': {'light': '─', 'heavy': '━', 'double': '═', 'arc': '─', 'block': '█'},
    'vert':  {'light': '│', 'heavy': '┃', 'double': '║', 'arc': '│', 'block': '█'},
    's-e':   {'light': '┌', 'heavy': '┏', 'double': '╔', 'arc': '╭', 'block': '█'},
    's-w':   {'light': '┐', 'heavy': '┓', 'double': '╗', 'arc': '╮', 'block': '█'},
    'n-e':   {'light': '└', 'heavy': '┗', 'double': '╚', 'arc': '╰', 'block': '█'},
    'n-w':   {'light': '┘', 'heavy': '┛', 'double': '╝', 'arc': '╯', 'block': '█'}
}


def as_block(text: str = "", width: int = 10, height: int = 10, blockset: str = "light", compensate: bool = True,
             aslist: bool = False) -> [str, List[str]]:
    """Creates a block. containing text, of Unicode characters.

    You have a few options of the block characters to use, examples below.

    ┌──────┮━━━━━━━┓
    │light!│ heavy ┣━━━╾──╖
    └──────┾━━━━━━━┛      ║
    ╔══════╪══════███████═╝
    ║double│╭────╮█block█
    ╚══════╪╡arc!│███████
           └┴────╯

    :param text: The text inside the block
    :param width: The width of the block
    :param height: The height of the block
    :param blockset: Which block set to use
    :param compensate: When set to True, the height/weight are actually the size of the space within the block
    :param aslist: Whether to return as a list of lines, or as a string with newlines
    :return: A string or a list, depending on aslist
    """
    if blockset not in ['light', 'heavy', 'double', 'arc', 'block']:
        blockset = 'light'
    if compensate:
        width += 2
        height += 2
    output = [] if aslist else ""
    # Here we just make the first few variables,
    # First we check if blockset is a valid set, and if not, we just reset it.
    # Then if compensate is True we add 2 to each size variable, to compensate
    # for the extra size added by the block pieces
    # and we start the output, with just a south-east corner.

    for line in range(0, height):
        currline = ("" if aslist or line == 0 else "\n")
        if line in [0, height-1]:
            currline += block['n-e'][blockset] if line == height-1 else block['s-e'][blockset]
            for x in range(0, width-2):
                currline += block['horiz'][blockset]
            currline += block['n-w'][blockset] if line == height-1 else block['s-w'][blockset]
        else:
            currline += block['vert'][blockset]
            for char in range(0, width-2):
                if text == "":
                    currline += " "
                else:
                    currline += text[:1]
                    text = text[1:]
            currline += block['vert'][blockset]
        output += ([currline] if aslist else currline)
    return output
