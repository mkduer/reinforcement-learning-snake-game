from os import getcwd

# command line default values
EPISODES = 5000
DELAY = 0

# resume/save game settings
RESUME = False
RESUME_EPISODE = 1200000
SAVE_EPISODE = 1000000

# delete file settings
DELETE_JSON = True
DELETE_GRAPHS = True

# external directories
JSON_DIR = str(getcwd()) + '/json/'
DATA_DIR = str(getcwd()) + '/measurements/'
GRAPH_DIR = str(getcwd()) + '/graphs/'

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
MOUSE = 100
WALL = -100
SNAKE = -100
EMPTY = -10
