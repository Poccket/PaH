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
    if not isinstance(mode, str):
        raise TypeError("argument 'mode' must be str")
    mode = mode.lower()
    if mode not in ["s", "m"]:
        raise ValueError("invalid mode: '" + mode + "'")

    if mode == 's':
        for vItem in range(0, length):
            for vList in inp:
                if vItem < len(vList):
                    output.append(vList[vItem])
            if endchar is not None:
                output.append(endchar)
    elif mode == 'm':
        for vItem in range(0, length):
            output.append([])
            for vList in inp:
                if vItem <= len(vList)-1:
                    output[vItem].append(vList[vItem])
            if endchar is not None:
                output[vItem].append(endchar)
    return output
