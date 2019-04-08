"""Helper functions"""


def is_int(inp) -> bool:
    """Checks if an object is an integer

    :param inp: Input object
    :return: boolean
    """
    try:
        int(inp)
        return True
    except ValueError:
        return False
    # Simply a helper function that checks if 'inp' can be run through 'int().'

    # Imagine we have a, which is "1", making it a string. This means 'int(a)' would work, however, if we did something
    # like 'return type(a) is int' wouldn't, despite the fact that it could work as an int.
    # An example use case of this would be checking the value of a variable set with 'input()', since in Python 3 the
    # output of 'input()' is always a string. So you could use this to break a while loop only when the variable is a
    # something that works as an integer.
