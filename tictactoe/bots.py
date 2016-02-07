import random
import utils
from copy import deepcopy
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
        random.shuffle(move_list)
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

class MiniMaxBot(GenericT3Bot):
    def think(self, game):
        """implement the minimax algorithm

            1. pick the max of your moves.
            2. the value of each of your moves is the min of your opponent's moves
               if you make that move

            Use this algorithm to implement a recursive algorithm.
            Base case: the game is decided. then it is worth a value.
                       recursive case: the min or max move.


            Each time we have to copy the board new so it's not contaminated
                (i.e. so no two recursive calls are editing the same data)
            so, algorithm:
                for each move:
                    hypothetically apply the move
                    recurse to hypothetically apply other move
        """
        moves = {}
        #print(self.open_moves(game))
        #for move in self.open_moves(game):
        #    print('looking at', move)
        #    new_game = game.hypothetical(move, self.symbol)
        #    other_player = utils.other_player(self.symbol)
        #    val, _ = self.ab_recursion_solver(new_game, other_player)
        #    moves[move] = val
        #sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)

        #for move, val in sorted_moves:
        #    print("Move {} has value {}".format(move, val))
        #move = sorted_moves[0][0]
        #if not move:
        #    return random.choice(self.open_moves(game))
        #return sorted_moves[0][0]
        val, move = self.ab_recursion_solver(game, self.symbol)
        if not move:
            return random.choice(self.open_moves(game))
        return move

    def recursion_solver(self, game, player):
        if game.no_winner():
            if player == self:
                best_score = -10**10
            else:
                best_score = 10**10
            best_move = None
            for move in self.open_moves(game):
                new_game = game.hypothetical(move, player)
                other_player = utils.other_player(player)
                valueofmove, _ = self.recursion_solver(new_game, other_player)
                me_condition = player == self and valueofmove > best_score
                them_condition = player != self and valueofmove < best_score
                if me_condition or them_condition:
                    best_score = valueofmove
                    best_move = move
            return best_score, best_move
        else:
            if game.draw():
                return 0, None
            elif game.winner == self:
                return 1, None
            else:
                return -1, None

    def ab_recursion_solver(self, game, player, alpha=-10**10, beta=10**10):
        if game.no_winner():
            best_move = None
            if len(self.open_moves(game)) == 0:
                return 0, None
            for move in self.open_moves(game):
                new_game = game.hypothetical(move, player)
                other_player = utils.other_player(player)
                valueofmove, _ = self.ab_recursion_solver(new_game, other_player, alpha, beta)
                me_condition = player == self and valueofmove > alpha
                them_condition = player != self and valueofmove < beta
                if me_condition:
                    alpha = valueofmove
                    best_move = move
                    if alpha >= beta:
                        return alpha, best_move
                elif them_condition:
                    best_move = move
                    beta = valueofmove
                    if beta <= alpha:
                        return beta, best_move
            if player == self:
                return alpha, best_move
            else:
                return beta, best_move
        else:
            if game.draw():
                return 0, None
            elif game.winner == self:
                return 1, None
            else:
                return -1, None

"""
alpha-beta pruning

beta is my best max option so far
if asking a min child to give me an option and they see anything less than beta
then i know i can skip the rest of their biz

and vice versa

if alpha is the worst option so far and i'm a min node and i'm asking for
a max node to give me a value and i've already seen a pretty low value from another
child, and the max node sees a value that' shigher, then it shouldn't be further explored
"""
