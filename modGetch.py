import os


class _Arrow:
    def __init__(self):
        if os.name == 'nt':
            self.impl = _arrownt
        else:
            self.impl = _arrowunix

    def __call__(self): return self.impl()


def _arrowunix():
    a, b, c = None, None, None
    keys = {'A': 'up', 'B': 'down', 'C': 'right', 'D': 'left', 'R': 'select', 'q': 'escape'}
    while c not in ['A', 'B', 'C', 'D']:
        while a not in ['\x1b', '\r', 'q']:
            a = getch()
        if a == '\r':
            c = 'R'
            break
        if a == 'q':
            c = 'q'
            break
        getch()
        c = getch()
    return keys[c]


def _arrownt():
    a, b = None, None
    keys = {b'H': 'up', b'P': 'down', b'M': 'right', b'K': 'left', 'R': 'select', 'q': 'escape'}
    while b not in [b'H', b'P', b'M', b'K']:
        while a not in [b'\xe0', b'\r', b'q']:
            a = getch()
        if a == b'\r':
            b = 'R'
            break
        if a == b'q':
            b = 'q'
            break
        b = getch()
    return keys[b]


#class _ArrowNT:
#    def __init__(self):
#        pass
#
#    def __call__(self):
#        a, b = None, None
#        keys = {'H': 'up', 'P': 'down', 'M': 'right', 'K': 'left', 'R': 'select', 'q': 'escape'}
#        while b not in [b'H', b'P', b'M', b'K']:
#            while a not in [b'\xe0', b'\r', b'q']:
#                a = getch()
#            if a == b'\r':
#                b = 'R'
#                break
#            if a == b'q':
#                b = 'q'
#                break
#            b = getch()
#        return keys[b]


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
get_arrow = _Arrow()
