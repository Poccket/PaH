# list_manip.py
# functions for manipulating and creating lists.
from typing import List


def merge_alternate(listlist: list, endchar: str = None) -> List[str]:
    """
    Merges lists into one list.

    Creates a single list from a set of lists by alternating through the lists.
    For example, Item from A, Item from B, Item from C, Item from A and so on.

    :param listlist: A list of the lists to merge.
    :param endchar: Character to put at the end of each iteration
    :return: The merged lists as a single list
    """
    if type(listlist) != list:
        raise TypeError("item 'listList' must be a list")
    output = []
    length = len(max(listlist, key=len))

    if endchar != "list":
        for vItem in range(0, length):
            for vList in listlist:
                if vItem <= len(vList)-1:
                    output.append(vList[vItem])
            if endchar is not None:
                output.append(endchar)
    else:
        for vItem in range(0, length):
            output.append([])
            for vList in listlist:
                if vItem <= len(vList)-1:
                    output[vItem].append(vList[vItem])

    return output
