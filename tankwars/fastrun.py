import logging
from controller import Controller

DEBUG = False

if DEBUG:
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
else:
    logging.basicConfig(filename='example.log', level=logging.INFO)


if __name__ == "__main__":
    logging.info('Starting...')
    c = Controller(debug=DEBUG)
    c.start_game("grass")
    c.all_player_names.extend(['human', 'bot'])
    c.agents[0].name = 'human'
    c.agents[1].name = 'bot'
    c.run()
