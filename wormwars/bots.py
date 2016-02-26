from __future__ import print_function
import random
import consts
import itertools

class GenericWormBot:
    def __init__(self, bot_id, initial_position=(0,0)):
        self.bot_id = bot_id

        x,y = initial_position
        self.body_parts = [{'x':x, 'y':y}]
        self.FAILED = False
        self.FAILURE_REASON = "Hasn't Failed"


    @classmethod
    def new_instance(cls, bot_id, starting_position):
        bot_id = "<{}>.{}".format(cls.__name__, bot_id)
        return cls(bot_id, starting_position)

    def act(self, game, bots):
        move_x, move_y = self.think(game, bots)
        new_head_x = self.body_parts[consts.HEAD]['x'] + move_x
        new_head_y = self.body_parts[consts.HEAD]['y'] + move_y

        self.body_parts.insert(consts.HEAD, {'x':new_head_x, 'y':new_head_y})

    def delete_tail(self):
        cell = self.body_parts[-1]
        del self.body_parts[-1]
        return cell

    def think(self, game, bots):
        raise NotImplementedError

    @property
    def head(self):
        return self.body_parts[consts.HEAD]

    def _single_collision(self, part):
        head = self.head
        return head['x'] == part['x'] and head['y'] == part['y']

    def _collision_helper(self, body):
        return any([self._single_collision(part) for part in body])

    def self_collision(self):
        return self._collision_helper(self.body_parts[1:])

    def other_collision(self, bots):
        for bot in bots:
            if bot.bot_id == self.bot_id:
                continue
            if self._collision_helper(bot.body_parts):
                return True
        return False

    def failed(self, reason):
        self.FAILED = True
        self.FAILURE_REASON = reason

  def bad_move(self, new_coords):
        if len(self.body_parts) > 1:
            for part in self.body_parts[1:]:
                if part['x'] == new_coords[0] and part['y'] == new_coords[1]:
                    return True

        return False

class PriorityQueue:
    def __init__(self):
        self.items = []
        self.graveyard = set()

    def push(self, item):
        heapq.heappush(self.items, item)

    def push_many(self, items):
        for item in items:
            if item[1] not in self.graveyard:
                self.push(item)
                self.graveyard.add(item[1])

    def pop(self):
        return heapq.heappop(self.items)

    def not_empty(self):
        return len(self.items) > 0


class AwesomeBot(GenericWormBot):
    def calc_dist(self, coord1, coord2):
        ## coord1 = (x1,y1)
        ## coord2 = (x2,y2)
        xsq = (coord1[0]-coord2[0])**2
        ysq = (coord1[1]-coord2[1])**2
        return (xsq + ysq)**0.5

    def apply_move(self, move, xy):
        ## move = (-1,0)
        ## xy = (curx, cury)
        new_coord = (move[0]+xy[0], move[1]+xy[1])
        return new_coord


    def apply_moves(self, xy, foodxy):
        all_moves = []
        for move_name, move_value in consts.MOVES.items():
            new_coord = self.apply_move(move_value, xy)
            move_dist = self.calc_dist(new_coord, foodxy)
            if not self.bad_move(new_coord):
                all_moves.append((move_dist, new_coord, move_value))
        return all_moves

    def think(self, game, bots):

        foodxy = (game.food['x'], game.food['y'])
        head = self.body_parts[consts.HEAD]
        curxy = (head['x'], head['y'])

        frontier = PriorityQueue()
        frontier.push((0,curxy, None))
        came_from = dict()

        while frontier.not_empty():
            move_dist, next_move, move_value = frontier.pop()
            if next_move == foodxy:
                best_move = (move_dist, next_move, move_value)
                break
            moves = self.apply_moves(next_move, foodxy)
            for move in moves:
                came_from[move] = (move_dist, next_move, move_value)
            frontier.push_many(moves)

        justincase = 0
        while came_from[best_move][0] > 0 and justincase < 10**4:
            best_move = came_from[best_move]
            justincase += 1

        move_dist, next_move, move_value = best_move
        return move_value


