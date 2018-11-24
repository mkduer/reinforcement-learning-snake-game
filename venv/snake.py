class Snake:


    def __init__(self, tile: int):
        self.tile = tile
        self.update_count_max = 2
        self.update_count = 0

        self.length = 1
        self.direction = 0

        self.x = [0]
        self.y = [0]
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        self.tail = self.x[0], self.y[0]

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):
        self.update_count = self.update_count + 1
        if self.update_count > self.update_count_max:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]
                if i == self.length - 1:
                    self.tail = self.x[i], self.y[i]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.tile
            if self.direction == 1:
                self.x[0] = self.x[0] - self.tile
            if self.direction == 2:
                self.y[0] = self.y[0] - self.tile
            if self.direction == 3:
                self.y[0] = self.y[0] + self.tile

            self.update_count = 0

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

    def head_coordinates(self):
        return self.x[0], self.y[0]

    def tail_coordinates(self, head: (int, int)):
        """
        print(f'head coord: {head}')
        print(f'tail coord: {self.tail}')
        """
        return self.tail  # TODO subtract tail from head

