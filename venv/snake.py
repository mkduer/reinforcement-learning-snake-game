class Snake:

    def __init__(self, tile: int):
        self.tile = tile
        self.update_count_max = 2
        self.update_count = 0

        self.length = 6
        self.direction = 3

        self.x = []
        self.y = []

        # initial positions
        for i in range(0, self.length):
            self.x.append(i * self.tile)
            self.y.append(0)

        self.tail = self.x[-1], self.y[-1]
        self.head = self.x[0], self.y[0]

    def update(self):
        self.update_count = self.update_count + 1
        if self.update_count > self.update_count_max:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.tile
            if self.direction == 1:
                self.x[0] = self.x[0] - self.tile
            if self.direction == 2:
                self.y[0] = self.y[0] - self.tile
            if self.direction == 3:
                self.y[0] = self.y[0] + self.tile

            self.tail = self.x[self.length - 1], self.y[self.length - 1]
            self.head = self.x[0], self.y[0]
            self.update_count = 0

    def eats_mouse(self, mouse_x: int, mouse_y: int):
        for i in range(0, self.length):
            if mouse_x == self.x[i] and mouse_y == self.y[i]:

                self.x.append(self.x[-1])
                self.y.append(self.y[-1])
                self.length += 1

                for j in range(self.length - 2, 0, -1):
                    self.x[j] = self.x[j - 1]
                    self.y[j] = self.y[j - 1]
                return True
        return False

    def body_collision(self) -> bool:
        for i in range(2, self.length):
            if self.head[0] == self.x[i] and self.head[1] == self.y[i]:
                return True
        return False

    def wall_collision(self, x_base, x_max, y_base, y_max):
        if self.head[0] < x_base or self.head[0] + self.tile > x_max:
            return True

        if self.head[1] < y_base or self.head[1] + self.tile > y_max:
            return True
        return False

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

    def tail_coordinates(self):
        new_x, new_y = (0, 0)
        """
        print(f'head: {self.x[0]}, {self.y[0]}') # TODO: uncomment
        print(f'tail: {self.x[-1]}, {self.y[-1]}') # TODO: uncomment
        """
        if self.x[0] > self.tail[0]:
            new_x = self.x[0] - self.tail[0]
        if self.x[0] < self.tail[0]:
            new_x = self.tail[0] - self.x[0]
        if self.y[0] > self.tail[1]:
            new_y = self.y[0] - self.tail[1]
        if self.y[0] < self.tail[1]:
            new_y = self.tail[1] - y[0]

        #print(f'new x and y: {new_x}, {new_y}\n') # TODO uncomment

        return new_x, new_y
