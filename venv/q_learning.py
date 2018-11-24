

class Q_Learning:

    def __init__(self):

        # State
        self.actions = {'north': 0, 'east': 0, 'south': 0, 'west': 0}  # "clock-wise" directions
        self.table = {}  # Q-table values
        self.current_action = 'east'

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9

    def move_north(self):
        if self.current_action == 'north':
            return True
        return False

    def move_east(self):
        if self.current_action == 'east':
            return True
        return False

    def move_south(self):
        if self.current_action == 'south':
            return True
        return False

    def move_west(self):
        if self.current_action == 'west':
            return True
        return False

    def next_action(self):
        self.current_action = 'south'


    def update(self):
        # TODO: add q algorithm here
        print(f'update')




def main():
    q = Q_Learning()
    q.update()


if __name__ == "__main__":
    main()
