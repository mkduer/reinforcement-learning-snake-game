class QLearning:

    def __init__(self):
        self.table = {}  # Q-table
        self.current_action = 'east'

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9

    def move_north(self):
        """
        Makes snake move North
        """
        if self.current_action == 'north':
            return True
        return False

    def move_east(self):
        """
        Makes snake move East
        """
        if self.current_action == 'east':
            return True
        return False

    def move_south(self):
        """
        Makes snake move South
        """
        if self.current_action == 'south':
            return True
        return False

    def move_west(self):
        """
        Makes snake move West
        """
        if self.current_action == 'west':
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
        return self.table[hashkey]

    def update(self, state: str):
        # TODO: add q algorithm here and return

        # TODO: current_action is currently hardcoded to south, this needs to be updated and returned after the algorithm
        #print(f'update')
        return 1


def main():
    # local, class testing
    q = QLearning()


if __name__ == "__main__":
    main()
