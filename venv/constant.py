from os import getcwd

# command line default values
EPISODES = 1000000
DELAY = 0
TOTAL_TESTS = 1

# hyperparameters
ETA = 0.005
DISCOUNT = 0.9
EPSILON = 0.1

# rewards
MOUSE = 100
WALL = -100
SNAKE = -100
EMPTY = -10

# specific test
PARAM_TEST = True
PARAM = 'learning_rate'
PARAM_VAL = 0.5

# resume/save game settings
RESUME = False
RESUME_EPISODE = 1000000
SAVE_EPISODE = 100000

# delete file settings
DELETE_JSON = True
DELETE_GRAPHS = False

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
