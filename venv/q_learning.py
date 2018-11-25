from random import randint


class QLearning:

    def __init__(self):
        self.table = {}  # Q-table
        self.action = 'east'
        self.all_actions = ['north', 'east', 'south', 'west']

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9

    def move_north(self):
        """
        Makes snake move North
        """
        if self.action == 'north':
            return True
        return False

    def move_east(self):
        """
        Makes snake move East
        """
        if self.action == 'east':
            return True
        return False

    def move_south(self):
        """
        Makes snake move South
        """
        if self.action == 'south':
            return True
        return False

    def move_west(self):
        """
        Makes snake move West
        """
        if self.action == 'west':
            return True
        return False

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
        self.action = self.all_actions[randint(0, 3)]

        max_choice = actions[self.action]
        for a in actions:
            if actions[a] > max_choice:
                self.action = a

        return self.action

    def update(self, state: str):
        # TODO: function stub, add q algorithm here and return
        return 1



def main():
    # local, class testing
    q = QLearning()


if __name__ == "__main__":
    main()
