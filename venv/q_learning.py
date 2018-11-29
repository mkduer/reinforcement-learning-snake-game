from random import choice
import os
from shutil import rmtree
from json import dump, load
import constant


class QLearning:

    def __init__(self):
        # Q-table
        self.table = {}
        self.all_actions = ['north', 'east', 'south', 'west']

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9
        self.reward = 0

    def define_state(self, tail_loc: (int, int), mouse_loc: (int, int)) -> {str: float}:
        """
        Creates state based on the snake's origin head relative to its tail and relative to the mouse
        :param tail_loc: tail coordinates
        :param mouse_loc: mouse coordinates
        :return: the state key
        """
        tail_loc = int(tail_loc[0]/44), int(tail_loc[1]/44)
        mouse_loc = int(mouse_loc[0]/44), int(mouse_loc[1]/44)
        key = str(tail_loc) + str(mouse_loc)

        # if Q value does not exist
        if key not in self.table:
            self.table[key] = {'north': 0, 'east': 0, 'south': 0, 'west': 0}
        return self.table[key]

    def select_action(self, state: {str: float}):
        """
        Given the state details, choose the optimal action i.e. the maximal choice or, if there is
        no obvious maximum, a randomized action
        :param state: the state and actions
        :return: the selected action
        """
        action = choice(self.all_actions)
        max_val = state[action]

        for a in state:
            if state[a] > max_val:
                action = a
                max_val = state[a]

        return action

    def update_reward(self, reward_type: str):
        """
        Update reward depending on reward/penalty values
        :param reward_type: a string representing what the snake encountered
        """
        if reward_type == 'mouse':
            self.reward += constant.MOUSE
        elif reward_type == 'wall':
            self.reward += constant.WALL
        elif reward_type == 'snake':
            self.reward += constant.SNAKE
        elif reward_type == 'empty':
            self.reward += constant.EMPTY

    def reset_reward(self):
        """
        Resets the reward
        """
        self.reward = 0

    def update(self, q_current: {str: float}, q_next: {str: float}, action: str):
        """
        Implements the Q learning algorithm with temporal difference and set hyperparameters
        :param q_current: the current state
        :param q_next: the next state
        :param action: the action that was chosen
        """
        prediction = self.select_action(q_next)
        max_action = q_next[prediction]
        q_current[action] = q_current[action] + self.learning_rate * (self.reward + self.discount_factor * (max_action - q_current[action]))

    def display_table(self):
        """
        Displays the Q table
        """
        for state in self.table:
            print(f'{state}: {self.table[state]}')
        print('\n')

    def save_table(self, episode: int, clear_dir: bool):
        """
        Saves table to specified directory. If specified, the directory is cleared in order to remove previous
        episodes that may not otherwise be replaced due to a changed episode save (modulo value change).
        If the directory doesn't exist, it is created.
        :param episode: episode number
        :param clear_dir: if True, the directory and its contents will be removed, if False, nothing is explicitly removed
        """
        path = constant.JSON_DIR

        # clear directory if specified by function call
        if clear_dir and episode == 1 and os.path.exists(path):
            rmtree(path)

        # create directory if it doesn't exist
        if not os.path.exists(path):
            os.mkpath(path)

        # save tables to external files
        outfile = path + 'episode' + str(episode) + '.json'
        with open(outfile, 'w') as f:
            dump(self.table, f, indent=2)
            f.close()

    def load_table(self, filename) -> int:
        """
        Loads existing file as the current table state and returns the proceeding episode number
        :param filename: the filename to load data from
        :return: the next episode following this table's state or -1 if the file does not exist
        """
        path = constant.JSON_DIR + filename
        if os.path.exists(path):
            with open(path) as f:
                self.table = load(f)
                print(f'LOADED table: \n{self.table}')
                f.close()
                return constant.RESUME_EPISODE + 1
        return -1
