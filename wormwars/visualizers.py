# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *
import logging
import consts


class PygameScreen:
    def __init__(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((consts.WINDOWWIDTH,
                                                    consts.WINDOWHEIGHT))
        font_size = min([consts.WINDOWWIDTH // 30, 18])
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', font_size)
        pygame.display.set_caption('WormWars')

    def draw(self, food, bots, stats):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
        self.DISPLAYSURF.fill(consts.BGCOLOR)
        self.draw_grid()
        for i, bot in enumerate(bots):
            self.draw_bot(bot.body_parts, i)
        self.draw_food(food)
        self.draw_score(stats)
        pygame.display.update()
        self.FPSCLOCK.tick(consts.FPS)

    def terminate(self):
        pygame.quit()
        #sys.exit()

    def draw_bot(self, body_parts, color_index=0):
        num_colors = len(consts.COLOR_LIST)
        if color_index >= num_colors:
            consts.LOGGER.warning("Repeating a color")
        cname, (part_bg, part_fg) = list(consts.COLOR_LIST.items())[color_index % num_colors]

        for part in body_parts:
            x = part['x'] * consts.CELLSIZE
            y = part['y'] * consts.CELLSIZE
            body_part_rect = pygame.Rect(x, y, consts.CELLSIZE, consts.CELLSIZE)
            pygame.draw.rect(self.DISPLAYSURF, part_bg, body_part_rect)
            inner_rect = pygame.Rect(x + 4, y + 4,
                                     consts.CELLSIZE - 8,
                                     consts.CELLSIZE - 8)
            pygame.draw.rect(self.DISPLAYSURF, part_fg, inner_rect)


    def draw_food(self, food):
        x = food['x'] * consts.CELLSIZE
        y = food['y'] * consts.CELLSIZE
        food_rect = pygame.Rect(x, y, consts.CELLSIZE, consts.CELLSIZE)
        pygame.draw.rect(self.DISPLAYSURF, consts.RED, food_rect)


    def draw_grid(self):
        # vertical lines
        for x in range(0, consts.WINDOWWIDTH, consts.CELLSIZE):
            pygame.draw.line(self.DISPLAYSURF, consts.DARKGRAY,
                            (x, 0), (x, consts.WINDOWHEIGHT))

        # horizontal lines
        for y in range(0, consts.WINDOWHEIGHT, consts.CELLSIZE):
            pygame.draw.line(self.DISPLAYSURF, consts.DARKGRAY,
                             (0, y), (consts.WINDOWWIDTH, y))

    def draw_score(self, stats):
        num_bots = len(stats)
        for i, (bot_id, stats_dict) in enumerate(stats.items(),0):
            score = stats_dict['score']
            color_name, _ = list(consts.COLOR_LIST.items())[i]
            name = "{} [{}]".format(bot_id, color_name)
            surface = self.BASICFONT.render('{} Score: {}'.format(name, score),
                                            True, consts.WHITE)
            rect = surface.get_rect()
            y_sep = consts.WINDOWHEIGHT // (num_bots+5)
            rect.topleft = (20,
                            20+y_sep*i)
            self.DISPLAYSURF.blit(surface, rect)


class PygameStatsOnly(PygameScreen):
    def draw(self, food, bots, stats):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
        self.DISPLAYSURF.fill(consts.BGCOLOR)
        self.draw_score(stats)
        pygame.display.update()
        #self.FPSCLOCK.tick(consts.FPS)
