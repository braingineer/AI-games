import sys
import os
sys.path.append(os.path.dirname(__file__))

import main
import bots
from main import WormWars
from bots import CarefulBot

default_2bots = [CarefulBot, CarefulBot]
default_3bots = [CarefulBot, CarefulBot, CarefulBot]

def demo():
    war = WormWars(default_3bots)
    for i in range(2000):
        try:
            war.run()
            war.initialize()
        except KeyboardInterrupt as e:
            print("Okay. Stopping now")
            break

if __name__ == "__main__":
    demo()
