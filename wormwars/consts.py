from boards import GameBoard, TronGameBoard, InfiniteGameBoard
import logging

"""
LOGGING STUFF
=============
"""
LOGGER = logging.getLogger("wormwars")
LOGGER.setLevel(logging.WARNING)


"""
SYNTACTIC SUGAR
===============
"""
HEAD = 0 # syntactic sugar: index of the worm's head
#             R    G    B
WHITE            = (255, 255, 255)
BLACK            = (  0,   0,   0)
RED              = (255,   0,   0)
GREEN            = (  0, 255,   0)
DARKGREEN        = (  0, 155,   0)
BLUE             = (  0,   0, 255)
DARKBLUE         = (  0,   0, 155)
PURPLE           = (200,   0, 200)
DARKPURPLE       = (115,   0, 115)
DARKGRAY         = ( 40,  40,  40)
BGCOLOR = BLACK
COLOR_LIST = {"Green": (GREEN, DARKGREEN), "Blue":(BLUE, DARKBLUE),
              "Purple": (PURPLE, DARKPURPLE)}
MOVES = {"left": (-1, 0), "right": (1,0),
         "down": (0, 1), "up": (0, -1)}
MOVE_LOOKUP = {v:k for k,v in MOVES.items()}

GAME_BOARDS = {"original": GameBoard,
               "tron": TronGameBoard,
               "infinite": InfiniteGameBoard}
PAUSE_AFTER_DEATH = True

"""
PYGAME SETTINGS
===============
"""

USE_PYGAME = True
STATS_ONLY = False
FPS = 300
WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
CELLSIZE = 10
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

