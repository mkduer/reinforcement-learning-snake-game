from random import randint
import constant


class Mouse:

    def __init__(self, width, height, snake_body: ([int], [int])):
        self.grid_width = width
        self.grid_height = height
        self.x = -1
        self.y = -1
        self.generate_mouse(snake_body)

    def draw(self, surface, image):
        """
        Draw the mouse on the board
        :param surface: the pygame board
        :param image: the mouse image
        """
        surface.blit(image, (self.x, self.y))

    def generate_mouse(self, snake_body: ([int], [int])):
        """
        Generates a mouse within the grid dimensions so it does not populate inside the snake
        :param snake_body: snake body's coordinates
        """
        unique = False
        length = len(snake_body[0])

        while not unique:
            x = randint(0, self.grid_width - 1) * constant.TILE
            y = randint(0, self.grid_height - 1) * constant.TILE
            for i in range(0, length):
                if x == snake_body[0][i] and y == snake_body[1][i]:
                    break
            unique = True

        self.x = x
        self.y = y

    def relative_coordinates(self, snake_head: (int, int)) -> (int, int):
        """
        Calculates the relative position of the mouse relative to the snake's origin head
        :param snake_head: the snake head's coordinates
        :return the relative coordinates
        """
        new_x = self.x - snake_head[0]
        new_y = self.y - snake_head[1]
        return new_x, new_y
