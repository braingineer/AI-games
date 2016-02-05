"""
Rewriting the game loop for the tank game

1. Poll for input
2. Update Physics
3. Handle Physics Events
4. Check Conditions & Loop
"""



def run(tanks, game):
    while check_conditions(tanks, game):
        for tank in tanks:
            tank.poll() # this allows for human players
            game.update(tank)
        if consts.USE_PYGAME:
            game.tick(tanks)


class Game:
    def __init__(self):
        pass

