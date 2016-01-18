import random
import utils
from utils import consts

class GenericT3Bot:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def open_moves(self, game):
        move_list = []
        for i in range(3):
            for j in range(3):
                if game.spaces[i][j] == consts.EMPTY:
                    move_list.append((i,j))
        return move_list

    def move(self, game):
        if game.draw():
            return
        next_move = self.think(game)
        consts.LOGGER.debug("{} has chosen {}".format(self.symbol, next_move))
        game.update(next_move, self)

    def think(self, game):
        raise NotImplementedError


class RandomBot(GenericT3Bot):
    def think(self, game):
        return random.choice(self.open_moves(game))
