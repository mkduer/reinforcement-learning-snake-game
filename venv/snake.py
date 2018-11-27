import constant


class Snake:

    def __init__(self):
        self.length = constant.SNAKE_LENGTH
        self.direction = constant.START_DIRECTION
        self.x, self.y = [], []
        self.head = (0, 0)
        self.tail = (0, 0)
        self.initialize_positions()

    def initialize_positions(self):
        """
        Initializes the position of the snake
        """
        self.length = constant.SNAKE_LENGTH
        self.x = []
        self.y = []

        # Initial position changes based on initial direction
        if self.direction == 0:    # East
            for i in range(self.length, 0, -1):
                self.x.append(i * constant.TILE)
                self.y.append(0)
        elif self.direction == 1:  # West
            for i in range(0, self.length):
                self.x.append(i * constant.TILE)
                self.y.append(0)
        elif self.direction == 2:  # North
            for i in range(0, self.length):
                self.y.append(i * constant.TILE)
                self.x.append(0)
        else:                      # South
            for i in range(self.length, 0, -1):
                self.y.append(i * constant.TILE)
                self.x.append(0)

        self.tail = self.x[-1], self.y[-1]
        self.head = self.x[0], self.y[0]
        self.length = constant.SNAKE_LENGTH

    def update(self):
        """
        Updates snake body based on new movements
        """
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        self.tail = self.x[-1], self.y[-1]

        # update head
        if self.direction == 0:
            self.x[0] += constant.TILE
        if self.direction == 1:
            self.x[0] -= constant.TILE
        if self.direction == 2:
            self.y[0] -= constant.TILE
        if self.direction == 3:
            self.y[0] += constant.TILE
        self.head = self.x[0], self.y[0]

    def eats_mouse(self, mouse_x: int, mouse_y: int) -> bool:
        """
        If the snake eats the mouse, update its body positions
        :param mouse_x: mouse's x coordinate
        :param mouse_y: mouse's y coordinate
        :return: True if mouse was eaten, False otherwise
        """
        for i in range(0, self.length):
            if mouse_x == self.x[i] and mouse_y == self.y[i]:

                # update tail
                self.x.append(self.x[-1])
                self.y.append(self.y[-1])
                self.tail = self.x[-1], self.y[-1]
                self.length += 1

                # update the rest of body
                for j in range(self.length - 2, 0, -1):
                    self.x[j] = self.x[j - 1]
                    self.y[j] = self.y[j - 1]

                # update head
                if self.direction == 0:
                    self.x[0] += constant.TILE
                if self.direction == 1:
                    self.x[0] -= constant.TILE
                if self.direction == 2:
                    self.y[0] -= constant.TILE
                if self.direction == 3:
                    self.y[0] += constant.TILE
                self.head = self.x[0], self.y[0]

                return True
        return False

    def body_collision(self) -> bool:
        """
        Check if the snake has collided with itself
        :return: True if collision occurred, False otherwise
        """
        for i in range(1, self.length):
            if self.head[0] == self.x[i] and self.head[1] == self.y[i]:
                return True
        return False

    def wall_collision(self, x_base, x_max, y_base, y_max):
        """
        Check if the snake collided with the wall
        :return: True if collision occurred, False otherwise
        """
        if self.head[0] < x_base or self.head[0] > x_max:
            return True
        if self.head[1] < y_base or self.head[1] > y_max:
            return True
        return False

    def move_east(self):
        """
        Snake moves East
        """
        self.direction = 0

    def move_west(self):
        """
        Snake moves West
        """
        self.direction = 1

    def move_north(self):
        """
        Snake moves North
        """
        self.direction = 2

    def move_south(self):
        """
        Snake moves South
        """
        self.direction = 3

    def draw(self, surface, image):
        """
        Draw the snake on the board
        :param surface: the pygame board
        :param image: the pixelated snake body image
        """
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

    def body_position(self) -> ([int], [int]):
        """
        :return: returns snake body's coordinates
        """
        return self.x, self.y

    def head_coordinates(self):
        """
        :return: returns the snake's head coordinates
        """
        return self.x[0], self.y[0]

    def tail_coordinates(self):
        """
        Calculates the relative position of the tail relative to the snake's origin head
        :return the relative coordinates
        """
        new_x = self.tail[0] - self.head[0]
        new_y = self.tail[1] - self.head[1]
        return new_x, new_y
