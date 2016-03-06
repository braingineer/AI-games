from agent import *
import math

class Robot(Player):
    def __init__(self, controller, color, k_right, k_backward, k_left,
                       k_forward, k_weapon1, k_weapon2, x, y, rotation = 0):
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


    def update(self):
        """ 90 down, 0 left, 270 up, 180 right """
        #self.direction = "Forward"
        #self.speed = self.max_speed * 0.75
        self.weapon2(None)
        super(Robot, self).update()

        #self.keypress_right()



        for agent in self.controller.agents:
            if agent.name == self.name:
                continue

            #print(agent.x, agent.y)
            #print(agent.rotation)
            dy, dx = (agent.y - self.y), (agent.x - self.x)
            #print(math.atan(M))
            #print(math.atan(M)*360)

            angle_rad = math.atan2(dy,dx)
            angle_deg = angle_rad*180.0/math.pi
            adj_deg = angle_deg if angle_deg > 0 else angle_deg + 360
            adj_deg += 180
            adj_deg %= 360
            print("PREADJUSTED DEGREE: {}".format(angle_deg))
            print("ADJUSTED DEGREE: {}".format(adj_deg))
            print("MY CURRENT DEGREE: {}".format(self.rotation))
            if self.rotation - adj_deg < 10:
                self.keypress_right()
            elif self.rotation - adj_deg > 10:
                self.keypress_left()
            #print(angle_rad)
            #print(angle_deg)
            #print(dx)
            #print(dy)

