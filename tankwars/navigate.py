"""
authors: AI class (the best AI class)
Winter 2016
"""

class Vec(object):
    def __init__(self, x, y, rotation):
        pass

class Grid(object):
    def __init__(self, num_cells, window_size):
        self.cell_x
        self.cell_y

    def transform(self, x, y, rotation):
        """
        :param x:
        :param y:
        :param rotation:
        :return: a :Vec: object
        """
        x // self.cell_x
        y // self.cell_y

    def apply_move(self, vec, dx, dy, drotation):
        """
        return a new vec given a current vec + a move

        :param vec:
        :param dx:
        :param dy:
        :param drotation:
        :return:
        """
        pass