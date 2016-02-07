import logging

class consts:
    """
    SYNTACTIC SUGAR
    ===============
    """

    EMPTY = "-"
    X = "X"
    O = "O"
    LOGGER = logging.getLogger("tictactoe")
    #                    R    G    B
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
    BGCOLOR = WHITE

    """
    PYGAME SETTINGS
    ===============
    """

    USE_PYGAME = False
    WINDOWWIDTH = 500
    WINDOWHEIGHT = 300
    FPS = 40

    """
    GAME SETTINGS
    =============
    """

    # this will randomize the order, so that X doesn't always start first
    MAKE_IT_FAIR = False

def pretty_board(spaces):
    return "\n".join("|".join(row) for row in spaces)

def debug(use_console=True, filename=None):
    if use_console:
        ch = logging.StreamHandler()
    else:
        assert filename is not None
        ch = logging.FileHandler(filename)

    ch.setLevel(logging.DEBUG)
    consts.LOGGER.addHandler(ch)
    consts.LOGGER.setLevel(logging.DEBUG)

def other_player(player):
    return consts.X if player == consts.O else consts.O

def all_same(vec):
    return vec[0] == vec[1] == vec[2] != consts.EMPTY
