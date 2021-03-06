"""Functions for manipulating or creating lists"""
from typing import List


def merge_alternate(inp: list, mode: str, endchar: str = None) -> List[str]:
    """Merges lists into one list using an alternating pattern.

    There are two modes able to be used in this function, detailed below.
    To select a mode, set 'mode' to the first letter of the mode you wish to use.

    m(ulti)
        Creates a list of lists, from a set of lists.

        For example:
        List 0: Item 0 from A, Item 0 from B, Item 0 from C, endchar (if set)
        List 1: Item 1 from A, Item 1 from B, and so on.

    s(ingle)
        Creates a single list, using every item from the lists.

        For example:
        Item 0 from A, Item 0 from B, Item 0 from C, endchar (if set), Item 1 from A, and so on.

    :param inp: A list of the lists to merge.
    :param mode: The mode you want to use.
    :param endchar: Character to put at the end of each iteration, if set
    :return: The merged lists as a single list
    """
    output = []
    length = len(max(inp, key=len))
    # Here we just make two variables to use later,
    # output is just an empty list to add any output to
    # length is the length, of the longest list in 'inp'

    if not isinstance(mode, str):
        raise TypeError("argument 'mode' must be str")
    mode = mode.lower()
    if mode not in ["s", "m"]:
        raise ValueError("invalid mode: '" + mode + "'")
    # Right here we first check if 'mode' is a string, if not we throw a TypeError
    # Then we set mode to a lowercase version of itself, ie. 'M' becomes 'm'
    # Then we check if it's one of the valid modes, and if not, we throw a ValueError.

    if mode == 's':
        for vItem in range(0, length):
            for vList in inp:
                if vItem < len(vList):
                    output.append(vList[vItem])
            if endchar is not None:
                output.append(endchar)
    # This is the 'single' mode, first we start a for loop, which goes through every number between 0 and 'length'.
    # Then we start another for loop, which goes through every list in the input.
    # We check if vItem is larger than the list, because if it is we'd get an IndexError
    # and if it isn't, we append the item at vList's index vItem to the output.
    # Once we've gone through each list, we check if 'endchar' is set, and append it if it is.

    elif mode == 'm':
        for vItem in range(0, length):
            output.append([])
            for vList in inp:
                if vItem <= len(vList)-1:
                    output[vItem].append(vList[vItem])
            if endchar is not None:
                output[vItem].append(endchar)
    # This is the 'multi' mode, We start the same loop as previously,
    # But this time we append an empty list to the output.
    # Then we start going through the lists again,
    # We check if vItem is larger,
    # and if it isn't, append the item to the new list in the output.
    # If endchar is set, we add it to that list as well.
    # This creates a new list for every number between 0 and 'length'.

    return output
