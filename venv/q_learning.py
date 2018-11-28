from random import choice
import constant


class QLearning:

    def __init__(self):
        # Q-table
        self.table = {}
        self.all_actions = ['north', 'east', 'south', 'west']

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.5
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
