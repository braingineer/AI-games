from agent import *
from brain import Brain
import math
import time


class Robot(Player):
    def __init__(self, controller, color, k_right, k_backward, k_left,
                       k_forward, k_weapon1, k_weapon2, x, y, rotation = 0,
                       mode="attack"):
        self.controller = controller
        self.screen = self.controller.screen
        self.name = "Agent"
        self.type = 0
        self.x, self.y = x, y
        self.health = 100
        self.max_speed = TANK_SPEED
        self.max_speed_back = TANK_SPEED_BACK
        self.acceleration = TANK_ACCELERATION
        self.rotation_speed = TANK_ROTATION_SPEED
        self.speed = 0
        self.rotation = rotation
        self.direction = None
        self.moving = False
        self.rotating = False
        self.solid = 100
        self.current_collisions = []
        self.dead = False
        self.iter = 0
        self.behaviors = []
        self.logger = brain_log()
        self.mode = mode

        """Gives the player static ammo object, these objects are copied in their fire() function.
        These variables can be seen as weapons, so fiddle with these variables when adding/changing it"""
        self.ammo1, self.ammo2 = NormalShot(self), StickyBomb(self)

        if TANK_WIDTH > TANK_HEIGHT:
            self.radius = int(TANK_WIDTH * 0.55)
        else:
            self.radius = int(TANK_HEIGHT * 0.55)

        #Load and resize tank img with right color
        if color == 'green':
            self.MasterSprites = [pygame.transform.scale(pygame.image.load("images/tankgreen1.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankgreen2.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankgreen3.png"), (TANK_WIDTH, TANK_HEIGHT))]
        else:
            self.MasterSprites = [pygame.transform.scale(pygame.image.load("images/tankpurple1.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankpurple2.png"), (TANK_WIDTH, TANK_HEIGHT)), pygame.transform.scale(pygame.image.load("images/tankpurple3.png"), (TANK_WIDTH, TANK_HEIGHT))]

        self.sprite = self.MasterSprites[0]

        self.animationindex = 0

        self.brain = Brain(self)


    def update(self):
        """ 90 down, 0 left, 270 up, 180 right """
        self.logger.debug("Entering Agent {}'s Update".format(self.name))
        for agent in self.controller.agents:
            if agent.name == self.name:
                continue
            else:
                if self.mode == "attack":
                    ranker = self.brain.attack_ranker
                    lookahead = 2
                elif self.mode == "run":
                    ranker = self.brain.run_ranker
                    lookahead = 10
                self.brain.run_search(agent, ranker, lookahead=lookahead)
                #self.brain.turn_towards(agent)


        self.weapon1(None)
        super(Robot, self).update()

    """
        if len(self.behaviors) > 0:
            behavior_func = self.behaviors[-1]
            print('executed')
            if behavior_func():
                self.behaviors.pop()
        else:
            for agent in self.controller.agents:
                if agent.name == self.name:
                    continue
                if isinstance(agent, Robot):
                    continue
                print('adding')
                self.behaviors.append(self.face_agent(agent))
            print('new turn')
    """
