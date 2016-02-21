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

    def bad_move(self, x,y):
        if len(self.body_parts) > 1:
            neck_x, neck_y = self.body_parts[1]['x'], self.body_parts[1]['y']
            new_head_x, new_head_y = self.head['x']+x, self.head['y']+y
            return new_head_x == neck_x and new_head_y == neck_y
        else:
            return False

class RandomWormBot(GenericWormBot):
    def think(self, game, bots):
        x,y = random.choice(list(consts.MOVES.values()))
        while self.bad_move(x, y):
            x,y = random.choice(list(consts.MOVES.values()))
        return (x,y)

