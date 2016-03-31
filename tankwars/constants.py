'''
This file contains all the constant variables
When adding variables, make sure to place them in an alphabetical order
'''
CAPTION = "Achtung Panzer"
SCREEN_SIZE = (1000, 700)
FPS = 60
ANIMATION_SPEED = 2

"""Agents and Ammo"""
EXPLOSION_SIZE = 65
EXPLOSION_SPEED = 8
HEALTHBAR_SIZE = (0.5, 5)
TANK_SPEED = 3
TANK_SPEED_BACK = 1.5
TANK_ACCELERATION = 0.125
TANK_ROTATION_SPEED = 2
TANK_HEIGHT = 50
TANK_WIDTH = 50

"""Sound"""
MUSIC_CHANNELS = 1
MUSIC_DEFAULT_VOLUME = 0.40
GAMEFX_CHANNELS = (2, 3)
GAMEFX_DEFAULT_VOLUME = 0.40
MISCFX_CHANNELS = (4, 5)
MISCFX_DEFAULT_VOLUME = 0.40

"""Game World and WorldObjects"""
SOLID_OBJ_PUSHBACK = 0.02
MAP_BORDER_PUSHBACK = 0.05
DEAD_BUSH_SIZE = 80
STONE_MAX_SIZE = 180
DESERT_STONE_MAX_SIZE = 90
DRAW_OBSTACLES = False


STEPSIZE = 3  

""" LOGGING STUFF """
import logging
LOGLEVEL = logging.INFO

def duallog(loggername, shell_level="info", file_loc=".", disable=False):
    levels = {"debug": logging.DEBUG, "warning":logging.WARNING,
              "info": logging.INFO, "error":logging.ERROR,
              "critical":logging.CRITICAL}
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers and not disable:
        fh = logging.FileHandler("{}/{}.debug.log".format(file_loc, loggername))
        fh.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(levels[shell_level])
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger

def brain_log():
    return duallog("brain")