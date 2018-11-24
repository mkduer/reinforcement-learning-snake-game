

class Q_Learning:

    def __init__(self):

        # State
        self.actions = {'north': 0, 'east': 0, 'south': 0, 'west': 0}  # "clock-wise" directions
        self.table = {}  # Q-table values

        # Hyperparameters
        self.learning_rate = 1
        self.discount_factor = 0.9


    def update(self):
        print(f'update')


def main():
    q = Q_Learning()
    q.update()


if __name__ == "__main__":
    main()
