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
        #print("Initial x: ", x)
        #print("Initial y: ", y)


    @classmethod
    def new_instance(cls, bot_id, starting_position):
        bot_id = "<{}>.{}".format(cls.__name__, bot_id)
        return cls(bot_id, starting_position)

    def act(self, game, bots):
        move_x, move_y = self.think(game, bots)
        #move_x *= consts.CELLSIZE
        #move_y *= consts.CELLSIZE

        new_head_x = self.body_parts[consts.HEAD]['x'] + move_x
        new_head_y = self.body_parts[consts.HEAD]['y'] + move_y

        """
        try:
            assert new_head_x % consts.CELLSIZE == 0
            assert new_head_y % consts.CELLSIZE == 0
        except AssertionError as e:
            x = self.body_parts[consts.HEAD]['x']
            y = self.body_parts[consts.HEAD]['y']
            print("x: ", x)
            print("x modulo cell size: ", x % consts.CELLSIZE)
            print("y: ", y)
            print("y modulo cell size: ", y % consts.CELLSIZE)
            print("move_x: ", move_x)
            print("move_y: ", move_y)
            raise e
        """

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
        #if len(self.body_parts) > 1:
        #    neck_x, neck_y = self.body_parts[1]['x'], self.body_parts[1]['y']
        #    new_head_x, new_head_y = self.head['x']+x, self.head['y']+y
        #    while new_head_x == neck_x and new_head_y == neck_y:
        #        x,y = random.choice(list(consts.MOVES.values()))
        #        neck_x, neck_y = self.body_parts[1]['x'], self.body_parts[1]['y']
        #        new_head_x, new_head_y = self.head['x']+x, self.head['y']+y
        return (x,y)


class DirectBot(GenericWormBot):
    def line_dist(self, pos1, pos2):
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5

    def apply_moves(self, moves):
        head_x, head_y = self.head['x'], self.head['y']
        head_positions = [(head_x+x, head_y+y) for x,y in moves]
        return {head_pos:move for head_pos, move in zip(head_positions, moves)
                              if not self.bad_move(move[0], move[1])}

    def min_key(self, move_pair):
        head_pos, move = move_pair
        x,y = head_pos
        self.line_dist()

    def think(self, game, bots):
        food = (game.food['x'], game.food['y'])
        moves = list(consts.MOVES.values())
        moves_dict = self.apply_moves(moves)
        if len(moves_dict) == 0:
            consts.LOGGER.warning("About to collide!")
            return moves[0]
        #print("{} moves went in, {} moves came out".format(len(moves), len(moves_dict)))
        min_key = lambda x: self.line_dist(x[0], food)
        head_pos, min_move = min(moves_dict.items(), key=min_key)
        #move_x, move_y = min(moves, key=lambda x: self.line_dist(x, food))
        #print("Inside {}'s head".format(self.bot_id))
        #for head_pos, move in moves_dict.items():
        #    dist = self.line_dist(head_pos, food)
        #    move_name = consts.MOVE_LOOKUP[move]
        #    print("Doing {} results in {} distance".format(move_name, dist))
        #print("So, {} is doing {}".format(self.bot_id, consts.MOVE_LOOKUP[min_move]))
        #input()
        return min_move


class CarefulBot(DirectBot):
    def bad_move(self, x,y, bot=None):
        # this lets us pass in another bot
        bot = bot or self

        # if we passed in ourselves, take off our head
        if bot.bot_id == self.bot_id:
            parts_to_check = bot.body_parts[1:]
        # if we passed in another bot, we will check the whole body
        else:
            parts_to_check = bot.body_parts

        # new head position
        new_head_x, new_head_y = self.head['x']+x, self.head['y']+y
        # if the list is empty, this skips
        for part in parts_to_check:
            if new_head_x == part['x'] and new_head_y == part['y']:
                return True

        # if for loops passes without the if triggering, this is returned
        return False

    def think(self, game, bots):
        food = (game.food['x'], game.food['y'])
        moves = list(consts.MOVES.values())
        moves_dict = self.apply_moves(moves)
        if len(moves_dict) == 0:
            return moves[0]

        move_filter = lambda x: any([self.bad_move(x[1][0], x[1][1], bot)
                                     for bot in bots])
        move_pairs = list(itertools.filterfalse(move_filter, moves_dict.items()))
        if len(move_pairs) == 0:
            return moves[0]

        min_key = lambda x: self.line_dist(x[0], food)

        head_pos, min_move = min(move_pairs, key=min_key)
        return min_move
