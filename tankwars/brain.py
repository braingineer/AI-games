import math
from constants import SCREEN_SIZE
class Brain(object):
    def __init__(self, body):
        self.me = body
        self.last = (None, None)

    def distance_to(self, other_agent):
        pass

    def angle_to(self, other_agent):
        xdiff = (other_agent.x - self.me.x) / SCREEN_SIZE[0]
        ydiff = (other_agent.y - self.me.y) / SCREEN_SIZE[1]
        angle = math.degrees(math.atan2(-1*ydiff, xdiff))
        converted = angle + 180
        return converted
        return math.degrees(math.atan(float(ydiff)/xdiff)) % 360

    def angle_decision(self, other_agent):
        if (other_agent.x, other_agent.y) == self.last:
            return
        self.last = (other_agent.x, other_agent.y)
        angle_to = self.angle_to(other_agent)
        angle_between = self.me.rotation - angle_to
        xdiff = (other_agent.x - self.me.x) / SCREEN_SIZE[0]
        ydiff = (other_agent.y - self.me.y) / SCREEN_SIZE[1]
        print("==================")
        print("angle_between = {} | ydiff = {} | xdiff = {}".format(angle_between, ydiff, xdiff))
        print("\tratio: {} | my rotation: {}".format(float(ydiff)/xdiff, self.me.rotation))
        print("\tangle to: {}".format(angle_to))
        if abs(angle_between) < 10:
            return
        right = other_agent.x > self.me.x
        above = other_agent.y < self.me.y
        #print(right, above)
        #print(self.me.rotation)
        self.rotation=True
        if not right and above:
            self.me.rotation -= self.me.rotation_speed
        elif right and above:
            self.me.rotation += self.me.rotation_speed
        elif not right and not above:
            self.me.rotation += self.me.rotation_speed
        elif right and not above:
            self.me.rotation -= self.me.rotation_speed
        else:
            self.rotation=False

        self.me.rotation %= 360

