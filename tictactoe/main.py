
import sys
import bots
import visualizers
import utils
from copy import deepcopy
from utils import consts

try:
    from tqdm import tqdm
except:
    print("no tqdm")
    class tqdm(list):
        pass


class TicTacToe:
    def __init__(self, p1, p2):
        self.game = None
        self.p1 = p1
        self.p2 = p2

    def run(self, num_games=100):
        #### set everything up
        stats = {'draws': 0, 'total_games': num_games}
        stats[self.p1] = {'wins': 0, 'losses': 0}
        stats[self.p2] = {'wins': 0, 'losses': 0}
        consts.LOGGER.debug("Game initialized to run {} times".format(num_games))


        self.game = GameBoard.NewBoard()
        self.game.turn_on_screen()

        for game_index in tqdm(range(num_games)):
            consts.LOGGER.debug("New game beginning")


            first = self.p1
            other = self.p2

            if consts.MAKE_IT_FAIR:
                if game_index % 2 == 1:
                    first = self.p2
                    other = self.p1

            import pdb
            #pdb.set_trace()

            #### this the actual game loop
            while self.game.no_winner():
                first.move(self.game)
                first, other = other, first
            #### game has ended
            if not self.game.draw():
                consts.LOGGER.debug("{} has won".format(self.game.winner))
                stats[self.game.winner]['wins'] += 1
                stats[self.game.loser]['losses'] += 1
            else:
                consts.LOGGER.debug("Game is a graw")
                stats['draws']+=1

            #### start new game
            self.game = GameBoard.NewBoard(screen=self.game.screen)

            if game_index % 10 == 0 and consts.USE_PYGAME:
                print(self.pretty_stats(stats))

            if game_index % 100 == 0 and not consts.USE_PYGAME:
                print(self.pretty_stats(stats))

        #### done running simulations
        print(self.pretty_stats(stats))


    def pretty_stats(self, stats):
        pretty_string = """
                After {} games, the results are:
                    {} draws
                    {} has won {} times
                    {} has won {} times
                """.format(stats['total_games'], stats['draws'],
                           consts.X, stats[consts.X]['wins'],
                           consts.O, stats[consts.O]['wins'])
        return pretty_string

class GameBoard:
    def __init__(self, spaces):
        self.spaces = spaces
        self.screen = None
        self.winner = None
        self.loser = None

    def turn_on_screen(self):
        if consts.USE_PYGAME:
            self.screen = visualizers.PygameScreen()

    @classmethod
    def NewBoard(cls, spaces = None, screen=None):
        """ reset the board.

        This uses row-major indexing.
        In other words, the first index is row, the second is column.
        """

        spaces = spaces or [[consts.EMPTY for _ in range(3)] for _ in range(3)]
        board = cls(spaces)
        if screen:
            board.screen = screen
            screen.reset()
        return board



    def update(self, move, player):
        i, j = move
        if isinstance(player, str):
            self.spaces[i][j] = player
        else:
            self.spaces[i][j] = player.symbol
            if self.screen:
                self.screen.draw(move, player)



    def draw(self):
        game_over = all([cell!=consts.EMPTY for row in self.spaces for cell in row])
        no_winner = self.winner is None
        return game_over and no_winner

    def set_winner(self, winner):
        self.winner = winner
        self.loser = utils.other_player(self.winner)

    def vert_winner(self):
        spaces_by_col = [[self.spaces[i][j] for i in range(3)] for j  in range(3)]
        for col in spaces_by_col:
            if utils.all_same(col):
                self.set_winner(col[0])
                return True
        return False

    def row_winner(self):
        for row in self.spaces:
            if utils.all_same(row):
                self.set_winner(row[0])
                return True
        return False

    def diag_winner(self):
        diag1 = [(0,0), (1,1), (2,2)]
        diag2 = [(0,2), (1,1), (2,0)]
        diags = [diag1, diag2]
        for diag in diags:
            if utils.all_same([self.spaces[i][j] for i,j in diag]):
                self.set_winner(self.spaces[1][1])
                return True
        return False

    def no_winner(self):
        if self.vert_winner() or self.row_winner() or self.diag_winner():
            consts.LOGGER.debug("Found a winner")
            consts.LOGGER.debug(utils.pretty_board(self.spaces))
            return False
        elif self.draw():
            consts.LOGGER.debug("Draw game")
            return False
        consts.LOGGER.debug("No winner yet")
        consts.LOGGER.debug(utils.pretty_board(self.spaces))
        return True

    def hypothetical(self, move, player):
        new_spaces = deepcopy(self.spaces)
        newgame = GameBoard.NewBoard(new_spaces)
        newgame.update(move, player)
        return newgame


def test():
    p1 = bots.MiniMaxBot(consts.X)
    #p1 = bots.RandomBot(consts.X)
    p2 = bots.MiniMaxBot(consts.O)
    #p2 = bots.RandomBot(consts.O)
    game = TicTacToe(p1,p2)
    game.run(10000)

if __name__ == "__main__":
    #utils.debug()
    if len(sys.argv) > 1:
        consts.FPS = int(sys.argv[1])
    test()
