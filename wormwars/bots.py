from __future__ import print_function
import random
import consts
import itertools
import heapq
from collections import defaultdict

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
        t = self.think(game, bots)
        #print("{1}: is moving {0[0]} x and {0[1]} y".format(t, self.bot_id))
        move_x, move_y = t
        new_head_x = self.body_parts[consts.HEAD]['x'] + move_x
        new_head_y = self.body_parts[consts.HEAD]['y'] + move_y
        #print("{1}: is moving {0[0]} x and {0[1]} y".format(t, self.bot_id), end="; ")
        #print("New X: {0}; New Y: {1}".format(new_head_x, new_head_y))

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

    def _single_collision(self, part, head=None):
        head = head or self.head
        return head['x'] == part['x'] and head['y'] == part['y']

    def _collision_helper(self, body, head):
        return any([self._single_collision(part, head) for part in body])

    def self_collision(self):
        return self._collision_helper(self.body_parts[1:], self.body_parts[0])

    def other_collision(self, bots, new_coords=None):
        head_coord = new_coords or self.head
        for bot in bots:
            if bot.bot_id == self.bot_id:
                continue
            if self._collision_helper(bot.body_parts, head_coord):
                return True
        return False

    def failed(self, reason):
        self.FAILED = True
        self.FAILURE_REASON = reason

    def bad_move(self, new_coords, game=None, bots=None):
        if game:
            if new_coords[0] < 0 or new_coords[1] < 0:
                return True
            if new_coords[0] > game.right_edge or new_coords[1] > game.bottom_edge:
                return True
        if len(self.body_parts) > 1:
            for part in self.body_parts[1:]:
                if part['x'] == new_coords[0] and part['y'] == new_coords[1]:
                    return True
        if bots:
            #print("HERE")
            if self.other_collision(bots, {'x':new_coords[0], 'y':new_coords[1]}):
                return True

class LearningBot(GenericWormBot):
    def think(self, game, bots):
        """
        arguments:
            game:  the game state.
                   gives access to food location
            bots: other bots.
                  gives access to where other bots are located
        """

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

class PriorityQueue:
    def __init__(self, make_max=False):
        self.make_max = make_max
        self.items = []

    def _reverse(self, item):
        return tuple([item[0] * -1] + list(item[1:]))

    def push(self, item):
        if self.make_max:
            item = self._reverse(item)
        heapq.heappush(self.items, item)

    def push_many(self, items):
        for item in items:
            self.push(item)

    def pop(self):
        item = heapq.heappop(self.items)
        if self.make_max:
            item = self._reverse(item)
        return item

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

    def calc_closest_body(self, coord):
        dists = 0.
        for part in self.body_parts[:10]:
            x,y =  part['x'], part['y']
            dists += self.calc_dist(coord, (x,y))
        return dists #/ len(self.body_parts)

    def calc_manhattan(self, coord1, coord2):
        return abs(coord1[0]-coord2[0]), abs(coord1[1]-coord2[1])

    def apply_moves(self, xy, foodxy, game, bots):
        all_moves = []
        for move_name, move_action in consts.MOVES.items():
            new_coord = self.apply_move(move_action, xy)
            dist_to_food = self.calc_dist(new_coord, foodxy)
            #ave_body = self.calc_closest_body(new_coord)
            ave_body = 0
            if not self.bad_move(new_coord, game, bots):
                all_moves.append((dist_to_food, ave_body, new_coord, move_action))
        return all_moves

    def apply_manhattan_moves(self, xy, foodxy, game, bots):
        all_moves = []
        for move_name, move_action in consts.MOVES.items():
            new_coord = self.apply_move(move_action, xy)
            dist_to_food = self.calc_manhattan(new_coord, foodxy)
            if not self.bad_move(new_coord, game, bots):
                all_moves.append((dist_to_food, new_coord, move_action))
        return all_moves



    def apply_moves_bare(self, xy, game, bots):
        all_moves = []
        for move_name, move_action in consts.MOVES.items():
            new_coord = self.apply_move(move_action, xy)
            if not self.bad_move(new_coord, game, bots):
                all_moves.append((new_coord, move_action))
        return all_moves

    def think(self, game, bots):
        n = len(self.last_history)
        # this version makes it crazy
        #if n > 0 and n % 20 != 0:
        #if n == 0 or (n+1) % 20 == 0:
        astar(game, self, bots)
        try:
            return self.last_history.pop()
        except IndexError:
            print("crap. we're dead")
            return (0,1)


def astar(game, bot, bots):
    foodxy = (game.food['x'], game.food['y'])
    head = bot.body_parts[consts.HEAD]
    curxy = (head['x'], head['y'])
    starting_point = (0, 0,curxy, 0, None)

    frontier = PriorityQueue()
    frontier.push(starting_point)
    came_from = dict()
    graveyard = set()
    best_move = None


    while frontier.not_empty():
        last_move = frontier.pop()
        astarval, dist_to_food, move_xy_coord, number_steps, move_action = last_move
        if move_xy_coord == foodxy:
            best_move = (astarval, dist_to_food, move_xy_coord, number_steps, move_action)
            break
        moves = bot.apply_moves(move_xy_coord, foodxy, game, bots)
        for new_dist_to_food, ave_body, new_xy_coord, new_move_action in moves:
            if new_xy_coord not in graveyard:
                new_number_steps = number_steps+1
                next_astarval = new_dist_to_food+ new_number_steps
                new_move = (next_astarval, new_dist_to_food, new_xy_coord,
                            new_number_steps, new_move_action)
                came_from[new_move] = last_move
                frontier.push(new_move)
                graveyard.add(new_xy_coord)

    if best_move is None:
        astar_dontdie(game, bot, bots)
    else:
        bot.last_version = "normal"
        get_best(bot, best_move, came_from)

def astar_dontdie(game, bot, bots):
    print('in dont die')
    head = bot.body_parts[consts.HEAD]
    curxy = (head['x'], head['y'])
    butt = bot.body_parts[-1]
    buttxy = (butt['x'], butt['y'])
    starting_point = (0, curxy, None)

    frontier = PriorityQueue(True)
    frontier.push(starting_point)
    came_from = dict()
    graveyard = defaultdict(lambda: 0)
    memory = defaultdict(lambda: set())
    best_move = None

    #import pdb
    #pdb.set_trace()
    while frontier.not_empty():
        print(len(frontier.items))
        last_move = frontier.pop()
        number_steps, move_xy_coord, move_action = last_move
        moves = bot.apply_moves_bare(move_xy_coord, game, bots)
        for new_coord, new_action in moves:
            #move = (number_steps-1, move[0], move[1])
            #move_coord = move[1]
            print("here with {} moves".format(len(moves)))
            if number_steps+1 > graveyard[new_coord] and new_coord not in memory[move_xy_coord]:
                print(" and here ")
                new_move = (number_steps+1, new_coord, new_action)
                came_from[new_move] = (number_steps, move_xy_coord, move_action)
                frontier.push(new_move)
                graveyard[new_coord] = number_steps + 1
                memory[new_coord] = memory[move_xy_coord].union(set([move_xy_coord]))
                #graveyard.add(move_coord)
    if best_move == None:
        print("this is none")
        if len(came_from) == 0:
            print('we are screwed and dead')
            return list(consts.MOVES.values())[1]
        # move_pair[0] is the destination, move_pair[1] is the origin
        # move_pari[0][0] is the number_steps
        # getting second item, the [1] means  getting the origin, since we found the best destintation
        # going to pass the first so that in the history, we get the last move too
        best_move = max(came_from.items(), key=lambda move_pair: move_pair[0][0])[0]

    bot.last_version = "dontdie"
    get_best(bot, best_move, came_from)

def get_best(bot, best_move, came_from):
    bot.last_history = []
    justincase = 0
    #print(pos)
    bot.last_history.append(best_move[-1])
    while came_from[best_move][-1] is not None and justincase < 10**4:
        best_move = came_from[best_move]
        justincase += 1
        bot.last_history.append(best_move[-1])
