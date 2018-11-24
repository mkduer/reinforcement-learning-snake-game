"""
Source of original game is a tutorial for building snake with pygame:
  https://pythonspot.com/snake-with-pygame/

Modifications:
  - different visual components
  - code cleaned to reduce unnecessary if statements, change variable names
  - separate classes into different files
  - add functionality for wall collisions
  -	add count score, frames count, speed
  - Q learning algorithm to turn it into a reinforcement learning project
"""

import pygame
import argparse
import time
from random import randint

from mouse import Mouse
from snake import Snake
from game import Game
from q_learning import QLearning


class App:

    def __init__(self):
        self.tile = 44
        self.row_tiles = 3
        self.height_tiles = 3
        self.window_width = self.tile * self.row_tiles
        self.window_height = self.tile * self.height_tiles

        self._running = True
        self._display = None
        self._snake = None
        self._mouse = None

        self.game = Game()
        self.snake = Snake(self.tile)
        self.mouse = Mouse(0, 4, self.tile)  # TODO: Randomize these coordinates to fit within grid ranges
        self.score = 0
        self.frames = 0

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)

        pygame.display.set_caption('SNAKE')
        self._running = True
        self._snake = pygame.image.load("img/snake_body_mini.png").convert()
        # source for mouse: http://pixelartmaker.com/art/3d272b1bf180b60.png
        self._mouse = pygame.image.load("img/mouse_mini.png").convert()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_collision(self, i: int):
        print("\nCollision. You lose!")
        print("Score: " + str(self.score))
        print("Total Frames: " + str(self.frames))

    def on_loop(self):
        self.snake.update()

        # if snake eats mouse
        for i in range(0, self.snake.length):
            if self.game.is_collision(self.mouse.x, self.mouse.y, self.snake.x[i], self.snake.y[i], self.tile):
                self.mouse.x = randint(2, 9) * self.tile
                self.mouse.y = randint(2, 9) * self.tile
                self.snake.length = self.snake.length + 1
                self.score += 1

        # if snake collides with itself
        for i in range(2, self.snake.length):
            if self.game.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], 40):
                self.on_collision(i) 
                exit(0)

        # if snake collides with walls
        if self.game.is_wall_collision(0, self.window_width, 0, self.window_height, self.snake.x[0], self.snake.y[0]):
            self.on_collision(i)
            exit(0)

    def on_render(self):
        self._display.fill((0, 0, 0))
        self.snake.draw(self._display, self._snake)
        self.mouse.draw(self._display, self._mouse)
        pygame.display.flip()

    def human_play(self, delay: int):
        """
        Executes the game play, snake movements, and loops until the game ends.
        Keys can be used to play the game.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        """

        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.snake.move_right()
            elif keys[pygame.K_LEFT]:
                self.snake.move_left()
            elif keys[pygame.K_UP]:
                self.snake.move_up()
            elif keys[pygame.K_DOWN]:
                self.snake.move_down()
            elif keys[pygame.K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(float(delay) / 1000.0)
            self.frames += 1

    def ai_play(self, delay: int):
        """
        Executes the game play, snake movements, and loops until the game ends.
        Movements are implemented by the AI rather than by a human pressing keys.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        """
        q = QLearning()

        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()

            head_loc = self.snake.head_coordinates()
            mouse_loc = self.mouse.relative_coordinates(head_loc) # TODO: implement
            """
            tail_loc = self.snake.tail_coordinates(head_loc)  # TODO: implement
            """
            tail_loc = (0,0)
            state = q.define_state(tail_loc, mouse_loc)
            q.update(state)

            if q.move_east():
                self.snake.move_right()
            elif q.move_west():
                self.snake.move_left()
            elif q.move_north():
                self.snake.move_up()
            elif q.move_south():
                self.snake.move_down()

            self.on_loop()
            self.on_render()

            time.sleep(float(delay) / 1000.0)
            self.frames += 1


def parse_args():
    """ purpose: parse command line arguments if they are available
        return: values associated with flag(s)"""

    # define arguments and types
    parser = argparse.ArgumentParser(description='A Snake game (created for training an AI), '
                                        'but also available for manual play')
    parser.add_argument('-d', metavar='delay', type=int, nargs='?', help='delays speed of snake (e.g. lower values '
                                        'result in faster snake, higher values result in slower snake', default=40)
    parser.add_argument('-ai', metavar='player_type', type=str, nargs='?', help='y/n where "y" activates AI play, '
                                        '"n" allows for manual play', default='n')

    # parse arguments
    args = parser.parse_args()
    delay = vars(args)['d']
    ai_play = vars(args)['ai']

    return delay, ai_play


if __name__ == "__main__":
    snake_app = App()

    # Parse command line
    delay, ai_play = parse_args()

    # Select game play
    if ai_play == 'y':
        snake_app.ai_play(delay)
    else:
        snake_app.human_play(delay)

    pygame.quit()
