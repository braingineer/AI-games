import logging
from controller import Controller, S_GAME

DEBUG = False

if DEBUG:
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
else:
    logging.basicConfig(filename='example.log', level=logging.INFO)


if __name__ == "__main__":
    logging.info('Starting...')
    c = Controller(debug=DEBUG)
    c.start_game("grass")
    c.all_player_names.append("Robot Alpha")
    c.all_player_names.append("Robot Beta")
    c.agents[0].name = "Robot Alpha"
    c.agents[1].name = "Robot Beta"
    c.run()