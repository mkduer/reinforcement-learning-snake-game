from os import getcwd

# command line default values
EPISODES = 10
DELAY = 10
SAVE_EPISODE = 5

# external files
DELETE_DIR = True
RESUME_FILE = False
RESUME_EPISODE = 10
JSON_DIR = str(getcwd()) + '/json/'
DATA_DIR = str(getcwd()) + '/measurements/'

# grid and display measurements
TILE = 44
WIDTH = 10
HEIGHT = 10
SNAKE_LENGTH = 1
SNAKE_X, SNAKE_Y = 2 * 44, 2 * 44

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
