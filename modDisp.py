"""Contains functions for creating display art."""
# TODO: Update to fit guideline.
# TODO: Improve, this is a wreck.
from typing import List


block = {
    'horiz': {'light': '─', 'heavy': '━', 'double': '═', 'arc': '─', 'block': '█'},
    'vert':  {'light': '│', 'heavy': '┃', 'double': '║', 'arc': '│', 'block': '█'},
    's-e':   {'light': '┌', 'heavy': '┏', 'double': '╔', 'arc': '╭', 'block': '█'},
    's-w':   {'light': '┐', 'heavy': '┓', 'double': '╗', 'arc': '╮', 'block': '█'},
    'n-e':   {'light': '└', 'heavy': '┗', 'double': '╚', 'arc': '╰', 'block': '█'},
    'n-w':   {'light': '┘', 'heavy': '┛', 'double': '╝', 'arc': '╯', 'block': '█'}
}


def as_block(text: str = "", width: int = 10, height: int = 10, blockset: str = "light", docompensate: bool = True,
             aslist: bool = False) -> [str, List[str]]:
    """
    Creates a block. containing text, of Unicode characters.

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
    :param docompensate: When set to True, the height/weight are actually the size of the space within the block
    :param aslist: Whether to return as a list of lines, or as a string with newlines
    :return: A string or a list, depending on aslist
    """
    if blockset not in ['light' 'heavy', 'double', 'arc', 'block']:
        blockset = 'light'

    if docompensate:  # Check to see if docompensate is true, which it is by default
        width += 2  # If it is, we add 2 to the width and height to get a 'true' width and height
        height += 2  # instead of the width/height of the text area
    currheight = 1  # currHeight keeps track of the line we're on, to compare to the height, set to 1 for now
    if aslist:
        output = [block['s-e'][blockset]]
    else:
        output = block['s-e'][blockset]  # And we'll set the output as DOWN-RIGHT, which is always the first character.
    x = width - 2  # Here we set x to the width minus 2, which is the length of the straight upper line
    while x > 0:  # Then, while x is bigger than 0
        if aslist:
            output[currheight - 1] += block['horiz'][blockset]
        else:
            output += block['horiz'][blockset]  # add a HOR to output
        x -= 1  # and remove 1 from x
    # Which leaves up with the upper straight line and the NW corner.
    if aslist:
        output[currheight - 1] += block['s-w'][blockset]
        output.append("")
    else:
        output += block['s-w'][blockset] + '\n'  # Finally we add the DOWN-LEFT, which completes the first line of the block.
    currheight += 1  # Then, since we added a newline, and have moved to line 2, add one to currHeight

    if text:  # Check if text is a valid variable, ie; not empty, null or undefined.
        counter = 0  # Then we set counter to 0, which keeps track of the amount of characters on the line
        limit = (width - 2) * (
                height - 2)  # Set limit to (width minus 2) times (height minus 2), aka the max characters allowed
        text = text[:limit]  # Then, simply cut out any characters that wouldn't fit.

        if currheight < height:  # Check if currHeight is already smaller than height, so we don't exceed it doing this
            if aslist:
                output[currheight - 1] += block['vert'][blockset]
            else:
                output += block['vert'][blockset]  # Add a VER to the output, the first line of the left wall

        for x in text:  # And for every letter in text
            if currheight < height:  # check to make sure currHeight hasn't past height, if it hasn't,
                if counter < width - 2:  # check if the characters on line is smaller than the width allowed, if so
                    if aslist:
                        output[currheight - 1] += x
                    else:
                        output += x  # add the letter to the output
                    counter += 1  # and add 1 to the counter
                else:  # if the characters on the line are more than the width
                    if aslist:
                        output[currheight - 1] += block['vert'][blockset]
                        output.append("")
                        output[currheight] += block['vert'][blockset] + x
                    else:
                        output += block['vert'][blockset] + "\n" + block['vert'][blockset] + x  # add a VER, newline, VER and the letter to the output
                    currheight += 1  # then since we're on a newline we add 1 to currHeight
                    counter = 1  # and set the counter to 1, since it's a newline and we've put a character in

        if currheight < height:  # if the currHeight isn't past height
            while counter < width - 2:  # then while the counter isn't past the width minus 2
                if aslist:
                    output[currheight - 1] += " "
                else:
                    output += " "  # add blank filler space to the output
                counter += 1  # and add one to counter since we're adding a character
            if aslist:
                output[currheight - 1] += block['vert'][blockset]
                output.append("")
            else:
                output += block['vert'][blockset] + '\n'  # after that, add a VER and a newline
            currheight += 1  # then add to currHeight since we made a newline

    while currheight < height:  # then, while currHeight is less than height, so we don't overshoot
        if aslist:
            output[currheight - 1] += block['vert'][blockset]
        else:
            output += block['vert'][blockset]  # add a VER to the output
        counter = 0  # set the counter to 0
        while counter < width - 2:  # and then, while counter is less than width minus 2
            if aslist:
                output[currheight - 1] += " "
            else:
                output += " "  # add a blank space to output
            counter += 1  # and one to the counter
        if aslist:
            output[currheight - 1] += block['vert'][blockset]
            output.append("")
        else:
            output += block['vert'][blockset] + '\n'  # close the line with a VER and a newline added to output
        currheight += 1  # add one to currHeight, because newline

    x = width - 2  # Set x to width minus 2, which is the length of the bottom straight line.
    if aslist:
        output[currheight - 1] += block['n-e'][blockset]
    else:
        output += block['n-e'][blockset]  # add a UP-RIGHT to the output, the third corner.
    while x > 0:  # then, while x is bigger than 0,
        if aslist:
            output[currheight - 1] += block['horiz'][blockset]
        else:
            output += block['horiz'][blockset]  # add a HOR line,
        x -= 1  # and remove 1 from x
    if aslist:
        output[currheight - 1] += block['n-w'][blockset]
    else:
        output += block['n-w'][blockset]  # add the final block, a UP-LEFT, to close the box, and protect it from 3p1c h4x0rz
    return output  # return output to whatever called the function
