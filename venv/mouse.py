class Mouse:

    def __init__(self, x: int, y: int, tile: int):
        self.step = tile
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def relative_coordinates(self, snake_head: (int, int)):
        new_x, new_y = (0, 0)

        if snake_head[0] > self.x:
            new_x = snake_head[0] - self.x
        if snake_head[0] < self.x:
            new_x = self.x - snake_head[0]
        if snake_head[1] > self.y:
            new_y = snake_head[1] - self.y
        if snake_head[1] < self.y:
            new_y = self.y - snake_head[1]

        return new_x, new_y
