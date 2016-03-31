from math import atan2, cos, sin, pi, degrees, radians
import math
import heapq
from constants import *
from time import sleep
from collections import deque
import random
import logging

logger = brain_log()


def fix(angle):
    return degrees(atan2(sin(radians(angle)), cos(radians(angle))))


class GridStep(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def filter(self):
        self.x = 0 if self.x < 0 else self.x
        self.x = min(max(0,self.x), SCREEN_SIZE[0])
        self.y = min(max(0, self.y), SCREEN_SIZE[1])


    @classmethod
    def forward(cls, x, y, rotation, speed):
        new_x = x - math.cos(math.radians(rotation)) * (speed+1) * STEPSIZE
        new_y = y + math.sin(math.radians(rotation)) * (speed+1) * STEPSIZE
        if new_x < 0 or new_x > SCREEN_SIZE[0] or new_y < 0 or new_y > SCREEN_SIZE[1]:
            return cls(x,y)
        else:
            return cls(new_x, new_y)
        return cls(x,y)

    @classmethod
    def backward(cls, x, y, rotation, speed):
        new_x = x + math.cos(math.radians(rotation)) * (speed+1) * STEPSIZE
        new_y = y - math.sin(math.radians(rotation)) * (speed+1) * STEPSIZE
        if 0 < new_x or new_x > SCREEN_SIZE[0] or new_y < 0 or new_y > SCREEN_SIZE[1]:
            return cls(x,y)
        else:
            return cls(new_x, new_y)
        return cls(x,y)


class SearchState(object):
    def __init__(self, bot, location, rotation, move=None):
        self.bot = bot
        self.rotation = rotation
        self.move = move
        self.path_position = 0
        self.location = location
        self.visits = 0

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    @classmethod
    def initial(cls, bot, x, y, rotation):
        return cls(bot, GridStep(x,y), rotation)

    def move_forward(self):
        new_loc = GridStep.forward(self.location.x, self.location.y, 
                                   self.rotation, self.bot.speed)
        return SearchState(self.bot, new_loc, self.rotation, "move_forward")

    def move_backward(self):
        new_loc = GridStep.backward(self.location.x, self.location.y, 
                                   self.rotation, self.bot.speed)
        return SearchState(self.bot, new_loc, self.rotation, "move_backward")

    def turn_left(self):
        rotation = (self.rotation + self.bot.rotation_speed * STEPSIZE * 2)
        rotation %= 360
        return SearchState(self.bot, self.location, rotation, "turn_left")

    def turn_right(self):
        rotation = self.rotation - self.bot.rotation_speed * STEPSIZE * 2
        rotation %= 360
        return SearchState(self.bot, self.location, rotation, "turn_right")

    def turn_left_small(self):
        rotation = self.rotation + self.bot.rotation_speed 
        rotation %= 360
        return SearchState(self.bot, self.location, rotation, "turn_left")

    def turn_right_small(self):
        rotation = self.rotation - self.bot.rotation_speed 
        rotation %= 360
        return SearchState(self.bot, self.location, rotation, "turn_right")

    def left_move(self):
        rotation = (self.rotation + self.bot.rotation_speed * STEPSIZE * 2)
        rotation %= 360
        new_loc = GridStep.forward(self.location.x, self.location.y, 
                                   self.rotation, self.bot.speed)
        return SearchState(self.bot, new_loc, rotation, "left_move")

    def right_move(self):
        rotation = self.rotation - self.bot.rotation_speed * STEPSIZE * 2
        rotation %= 360
        new_loc = GridStep.forward(self.location.x, self.location.y, 
                                    rotation, self.bot.speed)
        return SearchState(self.bot, new_loc, rotation, "right_move")

    def shoot(self):
        pass

    def key(self):
        return (self.x, self.y, self.rotation, self.move)

    def apply(self, action):
        func = getattr(self, action)
        return func()

    def generate_next(self):
        actions = ["move_forward", "move_backward", "turn_left", "turn_right",
                   "turn_left_small", "turn_right_small", "left_move", "right_move"]#, "shoot"]
        next_states = []
        for action in actions:
            new_state = self.apply(action)
            new_state.path_position = self.path_position+1
            next_states.append(new_state)
        return next_states

    def satisfied(self, brain):
        if "turn" in self.move:
            logger.debug((brain.me.rotation, self.rotation))
            threshold = 7 + self.visits // 3
            turn_sat =  abs(brain.me.rotation - self.rotation) < threshold
            if turn_sat:
                logger.debug("Move is satisfied")
            else:
                logger.debug("increasing visit num")
                self.visits += 1
            return turn_sat

        elif "move" in self.move:
            loc_sat = abs(self.location.x - brain.me.x) < 1 and abs(self.location.y - brain.me.y) < 1
            return loc_sat

        else:
            raise Exception

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.rotation == other.rotation
    
    def __lt__(self, other):
        return 0

class SearchSolution(object):
    def __init__(self, brain):
        self.brain = brain
        self.items = deque()
        self.tick = 0
        self.last_move = None

    def add(self, move):
        self.items.append(move)

    def step(self):
        next_move = self.items[0]
        while len(self.items) > 0 and next_move.satisfied(self.brain):
            throwing = self.items.popleft()
            if len(self.items) > 0:
                next_move = self.items[0]
            else:
                next_move = None
        if next_move is not None:
            self.last_move = next_move
        return next_move

    def __len__(self):
        return len(self.items)


class Brain(object):
    def __init__(self, body):
        self.me = body
        self.last = (None, None)
        self.plan = []

    def distance_to(self, other_agent, x=None, y=None):
        x = x or self.me.x
        y = y or self.me.y
        return ((other_agent.x - x)**2 + (other_agent.y - y)**2)**0.5

    def angle_to(self, other_agent, x=None, y=None):
        x = x or self.me.x
        y = y or self.me.y
        xdiff = (other_agent.x - x) 
        ydiff = (other_agent.y - y) 
        angle = math.degrees(math.atan2(-1*ydiff, xdiff)) + 180
        return angle

    def angle_distance(self, other_agent, rotation=None, x=None, y=None):

        angle_to = self.angle_to(other_agent, x, y)
        my_angle = rotation or self.me.rotation

        a_to_v1 = fix(angle_to)
        a_to_v2 = a_to_v1 + (360 if a_to_v1 < 0 else 0)
        a_me_v1 = fix(my_angle)
        a_me_v2 = a_me_v1 + (360 if a_me_v1 < 0 else 0)
        #print("to v1 and v2: {} and {}".format(a_to_v1, a_to_v2))
        #print("me v1 and v2: {} and {}".format(a_me_v1, a_me_v2))
        return min(abs(a_me_v1-a_to_v1), abs(a_me_v2-a_to_v2))


        if angle_to > 180:
            angle_to = fix(angle_to)
        if my_angle > 180:
            old2 = my_angle
            my_angle = fix(my_angle)
        angle_diff = abs(angle_to - my_angle)
        return angle_diff

    def turn_towards(self, other_agent):
        angle_diff = self.angle_distance(other_agent)
        speed = self.me.rotation_speed

        def is_left():
            return angle_diff > 0
        if is_left():
            self.turn_left()
        else:
            self.turn_right()


    def turn_left(self):
        #print('SHOULD BE TURNING left')
        self.me.keypress_left()
        #self.me.rotation += self.me.rotation_speed

    def turn_right(self):
        #ssprint("SHOULD BE TURNING RIGHT")
        self.me.keypress_right()
        #self.me.rotation -= self.me.rotation_speed

    def move_forward(self):
        self.me.keypress_forward()

    def move_backward(self):
        self.me.keypress_backward()

    def left_move(self):
        self.turn_left()
        self.move_forward()

    def right_move(self):
        self.turn_right()
        self.move_forward()

    def exec_action(self, action):

        logger.debug("[{}]. EXECUTING ACTION: {}".format(self.me.name, action))
        logger.debug("==================")
        getattr(self, action)()

    def evaluate_distance(self, state, other_agent):
        return self.distance_to(other_agent, state.x, state.y) 

    def evaluate_angle(self, state, other_agent):
        return self.angle_distance(other_agent, state.rotation, state.x, state.y)

    def run_search(self, other_agent, ranker=None, lookahead=2):
        logger.debug("Starting search against agent {}".format(other_agent.name))
        logger.debug("Stats: X: {}, Y: {}, ROTATION: {}".format(self.me.x, self.me.y, self.me.rotation))
        logger.debug("Turning stepping size: {}".format(self.me.rotation_speed * STEPSIZE))

        force_replan = True
        if len(self.plan) == 0 or force_replan:
            logger.debug("Plan is empty, so replanning")
            self.plan = self.search_k(other_agent, ranker=ranker, lookahead=lookahead)
        else:
            logger.debug("Have existing plan. Running with that!")

        next_move = self.plan.step()
        while next_move is None:
            logger.debug("Plan had some issues. researching.")
            self.plan = self.search_k(other_agent, ranker=ranker, lookahead=lookahead)
            next_move = self.plan.step()
            if next_move is None:
                logger.debug("Plan failure....")
        self.exec_action(next_move.move)

    def decode(self, state, lookup, initial):
        path = SearchSolution(self)
        one_step = lookup[state.x, state.y, state.rotation]
        while one_step != initial:
            path.add(one_step)
            one_step = lookup[one_step.x, one_step.y, one_step.rotation]
        plan_str = "the plan is to: "
        for move in path.items:
            plan_str += "{} to ({:0.2f},{:0.2f}); ".format(move.move, move.x, move.y)
        logger.debug(plan_str)
        #logger.debug("The plan is to: {}".format(", ".join(m.move for m in path.items)))
        return path

    def attack_ranker(self, next_state, other_agent):
        dist_val = self.evaluate_distance(next_state, other_agent)
        ang_val = max(self.evaluate_angle(next_state, other_agent), 3)
        return ang_val+dist_val

    def run_ranker(self, next_state, other_agent):
        wall_penalty = 0
        dist_val = self.evaluate_distance(next_state, other_agent)

        ang_val = self.angle_distance(self.me, other_agent.rotation, other_agent.x, other_agent.y)
        if SCREEN_SIZE[0] - next_state.x  < 50 or next_state.x < 50:
            wall_penalty = 500
        if SCREEN_SIZE[1] - next_state.y + TANK_HEIGHT < 50 or next_state.y < 50:
            wall_penalty += 500 
        return -1 * (ang_val + dist_val) + wall_penalty #+ random.random()


    def search_k(self, other_agent, ranker=None, lookahead=2):
        """ Find the search path to the agent that is lookahead steps """
        ### all the necessary data structures
        #print("wat")
        #print("other.x={}, other.y={}".format(other_agent.x, other_agent.y))
        if ranker is None:
            ranker = self.attack_ranker
        frontier = PriorityQueue()
        solution = []
        graveyard = set()
        lookup = {}
        import pdb
        #pdb.set_trace()
        ### the initial search state.. our current location 
        initial = SearchState.initial(self.me, self.me.x, self.me.y, self.me.rotation)
        ### start the frontier off
        frontier.push((0,0, initial))
        graveyard.add((initial.x, initial.y, initial.rotation))
        ### while our path is less than lookahead or we have no more options
        while frontier.not_empty():
            # note: the _ means we don't care about that variable but we need a placeholder for it
            # it's the number from the for loop below
            # we include it to break ties when two values are the same
            val, _, cur_state = frontier.pop()
            import pdb
            #pdb.set_trace()
            if cur_state.path_position == lookahead:
                return self.decode(cur_state, lookup, initial)
            # iterate through the states that are possible after that
            next_list = cur_state.generate_next()
            for i, next_state in enumerate(next_list):
                if next_state.satisfied(self): continue
                ## evaluate that state. you can do different evaluations by replacing this
                ## the important thing is lower = better
                state_value = ranker(next_state, other_agent)
                logger.debug("MOVE: {} to do ({},{},{}) has value {}".format(next_state.move, 
                                                                             next_state.x,
                                                                             next_state.y,
                                                                             next_state.rotation,
                                                                             state_value))
                #print(dist_val, ang_val)
                #rint("distance val: {}".format(dist_val))
                #print("angle val: {}".format(ang_val))
                #print("me.x={}, me.y={}".format(self.me.x, self.me.y))
                #print("move.x={}, move.y={}".format(next_state.x, next_state.y))
                #print("them.x={}, them.y={}".format(other_agent.x, other_agent.y))
                ## if the state isn't in the graveyard (aka, we haven't see it on this path)
                ## then add it to our frontier
                if (next_state.x, next_state.y, next_state.rotation) not in graveyard:
                    frontier.push((state_value+val, i, next_state))
                    graveyard.add((next_state.x, next_state.y, next_state.rotation))
                    lookup[next_state.x, next_state.y, next_state.rotation] = cur_state
        raise Exception




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

    def __len__(self):
        return len(self.items)