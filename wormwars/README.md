# Worm Wars

## Description

An implementation of Snake with multiple snakes battling over the food.  Meant for an Intro to AI course.  

Note: turn on PyGame with `USE_PYGAME` variable in consts.py  make pygame window 
stats only with `STATS_ONLY` variable in consts.py.  Not having stats only means seeing each frame of every game. 

## Files
  1. main.py 
    - main game runner
    - does the game loop logic
  2. visualizers.py
    - implemented a pygame visualizing interface
      + Adapted from [Al Sweigart](https://inventwithpython.com/)'s implementation
  3. consts.py
    - all parameters set here
    - turns on PyGame, sets framerate, board size, etc.
  4. bots.py
    - bots get defined here
  5. boards.py
    - handles food placement, visualizer frame updates, etc.
    
