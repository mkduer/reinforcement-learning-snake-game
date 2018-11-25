from random import randint
import constant


class QLearning:

    def __init__(self):
        self.table = {}  # Q-table
        self.all_actions = ['north', 'east', 'south', 'west']

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9
        self.reward = 0


    def define_state(self, tail_loc: (int, int), mouse_loc: (int, int)):
        """
        Creates state based on the snake's origin head relative to its tail and relative to the mouse
        :param tail_loc: tail coordinates
        :param mouse_loc: mouse coordinates
        :return: the hashed state
        """
        hashkey = str(tail_loc) + str(mouse_loc)

        # if Q value does not exist
        if hashkey not in self.table:
            self.table[hashkey] = {'north': 0, 'east': 0, 'south': 0, 'west': 0}
        return hashkey

    def select_action(self, state: str):
        """
        Given the state details, choose the optimal action i.e. the maximal choice or, if there is
        no obvious maximum, a randomized action
        :param state: the state's relevant actions
        :return: the selected action
        """
        actions = self.table[state]
        action = self.all_actions[randint(0, 3)]
        max_choice = actions[action]

        for a in actions:
            if actions[a] > max_choice:
                action = a

        return action

    def update_reward(self, reward_type: str):
        if reward_type == 'mouse':
            self.reward + constant.MOUSE
        elif reward_type == 'wall':
            self.reward + constant.WALL
        elif reward_type == 'snake':
            self.reward + constant.SNAKE

    def reset_reward(self):
        self.reward = 0

    def update(self, state: str, next_state: str, reward: int, action: str):
        # TODO: function stub, add q algorithm here and return
        return 1



def main():
    # local, class testing
    q = QLearning()


if __name__ == "__main__":
    main()
