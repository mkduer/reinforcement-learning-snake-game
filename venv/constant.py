from os import getcwd

# command line default values
EPISODES = 5
DELAY = 0
SAVE_EPISODE = 1

# external files
DELETE_JSON = False
RESUME = True
RESUME_EPISODE = 50000
JSON_DIR = str(getcwd()) + '/json/'
DATA_DIR = str(getcwd()) + '/measurements/'

# grid and display measurements
TILE = 44
WIDTH = 8
HEIGHT = 8
SNAKE_LENGTH = 1
SNAKE_X, SNAKE_Y = 1 * 44, 1 * 44

# directions
EAST = (1, 0)
WEST = (-1, 0)
NORTH = (0, -1)
SOUTH = (0, 1)

# rewards
MOUSE = 200
WALL = -100
SNAKE = -100
EMPTY = -10
