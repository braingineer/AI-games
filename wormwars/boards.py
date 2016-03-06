import random
import visualizers
import consts

class GameBoard:
    def __init__(self, num_bots):
        self.right_edge = consts.WINDOWWIDTH // consts.CELLSIZE - 1
        self.bottom_edge = consts.WINDOWHEIGHT // consts.CELLSIZE -1
        self.no_food = set()
        self.food = self.new_food()
        self.turn_number = 0
        self.deleted_cells = []
        self.screen = None

        xdist, ydist = self.right_edge//(num_bots+1), self.bottom_edge//(num_bots+1)
        self.starting_positions = [(i*xdist, i*ydist) for i in range(1,1+num_bots)]


    def new_starting_position(self):
        pos = self.starting_positions.pop()
        self.no_food.add(pos)
        return pos

    def outside_bounds(self, bot):
        head = bot.head
        return  (head['x'] < 0 or head['y'] < 0 or
                 head['x'] > self.right_edge or head['y'] > self.bottom_edge)

    def update(self, bot):
        self.turn_number += 1
        head = (bot.head['x'], bot.head['y'])
        self.no_food.add(head)
        if bot._single_collision(self.food):
            self.food = self.new_food()
        else:
            cell = bot.delete_tail()
            cell = (cell['x'], cell['y'])
            if cell not in self.no_food:
                consts.LOGGER.debug("cell ({}) not in no_food ({})".format(cell, self.no_food))
                consts.LOGGER.debug("Worm body: {}".format(bot.body_parts))
                consts.LOGGER.debug("Deleted cells: {}".format(self.deleted_cells[-5:]))
            else:
                self.deleted_cells.append(cell)
                self.no_food.remove(cell)

    def initialize_screen(self):
        if consts.STATS_ONLY:
            self.screen = visualizers.PygameStatsOnly()
        else:
            self.screen = visualizers.PygameScreen()

    def tick(self, bots, stats):
        """ if drawing or reporting, do so here """
        if self.screen:
            self.screen.draw(self.food, bots, stats)

    def _food_helper(self):
        x = random.randint(0, self.right_edge-1)
        #x -= x % consts.CELLSIZE
        y = random.randint(0, self.bottom_edge-1)
        #y -= y % consts.CELLSIZE
        return x,y

    def new_food(self):
        x,y = self._food_helper()
        while (x,y) in self.no_food:
            x,y = self._food_helper()
        return {'x':x,'y':y}


class TronGameBoard(GameBoard):
    def update(self, bot):
        head = (bot.head['x'], bot.head['y'])
        self.no_food.add(head)
        if bot._single_collision(self.food):
            self.food = self.new_food()


class InfiniteGameBoard(GameBoard):
    def __init__(self, *args, **kwargs):
        super(InfiniteGameBoard, self).__init__(*args, **kwargs)
        self.right_edge = 10**10
        self.bottom_edge = 10**10

    def tick(self, bots, stats):
        """ infinite boards would have a hard time rendering without fancy
            camera shifting work"""
        pass
