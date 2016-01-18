import sys
import pygame
import utils
from utils import consts
from pygame.locals import QUIT

class PygameScreen:
    def __init__(self):
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((consts.WINDOWWIDTH,
                                                    consts.WINDOWHEIGHT))
        self.FPSCLOCK = pygame.time.Clock()

        self.compute_specs()
        font_size = min([consts.WINDOWWIDTH // 30, 18])
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', font_size)
        pygame.display.set_caption('Tic-Tac-Toe')

        self.mark_history = []
        self.draw()

    def reset(self):
        self.mark_history = []
        self.draw()

    def _make_rect(self, i, j):

        x = self.CELLSIZE[0]*i + self.OFFSET[0]
        y = self.CELLSIZE[1]*j + self.OFFSET[1]
        w = self.CELLSIZE[0] - 2 * self.OFFSET[0]
        h = self.CELLSIZE[1] - 2 * self.OFFSET[1]

        return pygame.Rect(x, y, w, h)

    def compute_specs(self):
        self.CELLSIZE = (consts.WINDOWWIDTH//3, consts.WINDOWHEIGHT//3)
        self.OFFSET = (self.CELLSIZE[0]//10, self.CELLSIZE[1]//10)
        self.RECTS = [[self._make_rect(col_i, row_j) for col_i in range(3)] for row_j in range(3)]

    def draw(self, move=None, player=None):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()

        self.DISPLAYSURF.fill(consts.BGCOLOR)
        self.draw_grid()
        if player and move:
            new_mark = {"coords":move, "player":str(player)}
            self.mark_history.append(new_mark)
        for mark in self.mark_history:
            self.draw_mark(mark)
        pygame.display.update()
        self.FPSCLOCK.tick(consts.FPS)

    def draw_grid(self):
        xthird = consts.WINDOWWIDTH // 3
        ythird = consts.WINDOWHEIGHT // 3
        for i in range(1,3):
            # vert
            pygame.draw.line(self.DISPLAYSURF, consts.DARKGRAY,
                             (xthird*i, 0), (xthird*i, consts.WINDOWHEIGHT),3)
            #horiz
            pygame.draw.line(self.DISPLAYSURF, consts.DARKGRAY,
                             (0, ythird*i), (consts.WINDOWWIDTH, ythird*i), 3)

    def draw_mark(self, mark):
        if mark['player'] == consts.X:
            self._draw_x(mark['coords'])
        else:
            self._draw_o(mark['coords'])

    def _draw_x(self, mark_coords):
        i, j = mark_coords
        rect = self.RECTS[i][j]
        pygame.draw.line(self.DISPLAYSURF, consts.RED,
                         rect.topleft, rect.bottomright, 5)
        pygame.draw.line(self.DISPLAYSURF, consts.RED,
                         rect.bottomleft, rect.topright, 5)

    def _draw_o(self, mark_coords):
        i, j = mark_coords
        rect = self.RECTS[i][j]
        center = rect.center
        radius = rect.width // 2
        radius -= radius//3
        pygame.draw.circle(self.DISPLAYSURF, consts.BLUE, center, radius, radius//3)

    def terminate(self):
        pygame.quit()
        sys.exit()
