def get_arrow():
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
        b = getch()
        c = getch()
    return keys[c]

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
