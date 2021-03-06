import constant


class Snake:

    def __init__(self):
        self.length = constant.SNAKE_LENGTH
        self.direction = constant.EAST
        self.x, self.y = [], []
        self.head = (0, 0)
        self.tail = (0, 0)
        self.initialize_positions(-1, -1)

    def initialize_positions(self, mouse_x, mouse_y):
        """
        Initializes the position of the snake
        """
        self.length = constant.SNAKE_LENGTH

        # avoid collision with existing mouse
        if self.x == mouse_x and self.y == mouse_y:
            self.x, self.y = [constant.SNAKE_X + 1], [constant.SNAKE_Y]
        else:
            self.x, self.y = [constant.SNAKE_X], [constant.SNAKE_Y]

        # Initial position changes based on initial direction
        if self.direction == constant.EAST:    # East
            for i in range(self.length - 1, 0, -1):
                self.x.append(i * constant.TILE)
                self.y.append(constant.SNAKE_Y)
        elif self.direction == constant.WEST:  # West
            for i in range(0, self.length - 1):
                self.x.append(i * constant.TILE)
                self.y.append(constant.SNAKE_Y)
        elif self.direction == constant.NORTH:  # North
            for i in range(0, self.length - 1):
                self.y.append(i * constant.TILE)
                self.x.append(constant.SNAKE_X)
        else:                      # South
            for i in range(self.length - 1, 0, -1):
                self.y.append(i * constant.TILE)
                self.x.append(constant.SNAKE_X)

        self.tail = self.x[-1], self.y[-1]
        self.head = self.x[0], self.y[0]

    def update_head(self):
        """
        Increments snake's head
        """
        x = self.x[0] + self.direction[0] * constant.TILE
        y = self.y[0] + self.direction[1] * constant.TILE
        self.x.insert(0, x)
        self.y.insert(0, y)
        self.head = self.x[0], self.y[0]
        self.length = len(self.x)

    def update_tail(self):
        """
        Increments snake's tail
        """
        self.x.pop(-1)
        self.y.pop(-1)
        self.tail = self.x[-1], self.y[-1]
        self.length = len(self.x)

    def eats_mouse(self, mouse_x: int, mouse_y: int) -> bool:
        """
        Checks if the snake eats the mouse
        :param mouse_x: mouse's x coordinate
        :param mouse_y: mouse's y coordinate
        :return: True if mouse was eaten, False otherwise
        """
        if mouse_x == self.x[0] and mouse_y == self.y[0]:
                self.length = len(self.x)
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

    def set_east(self):
        """
        Snake moves East
        """
        self.direction = constant.EAST

    def set_west(self):
        """
        Snake moves West
        """
        self.direction = constant.WEST

    def set_north(self):
        """
        Snake moves North
        """
        self.direction = constant.NORTH

    def set_south(self):
        """
        Snake moves South
        """
        self.direction = constant.SOUTH

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
        return self.head

    def tail_coordinates(self):
        """
        Calculates the relative position of the tail relative to the snake's origin head
        :return the relative coordinates
        """
        new_x = self.tail[0] - self.head[0]
        new_y = self.tail[1] - self.head[1]
        return new_x, new_y

    def current_direction(self):
        return self.direction
