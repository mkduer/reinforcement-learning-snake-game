import pygame
import argparse
import time

from mouse import Mouse
from snake import Snake
from q_learning import QLearning
import constant


class Game:

    def __init__(self):

        self.window_width = constant.WIDTH * constant.TILE
        self.window_height = constant.HEIGHT * constant.TILE
        self.score = 0
        self.frames = 0

        self._running = True
        self._display = None
        self._snake = None
        self._mouse = None

        self.snake = Snake()
        self.mouse = Mouse(constant.WIDTH, constant.HEIGHT, self.snake.body_position())
        self.q = QLearning()


    def pygame_init(self):
        """
        Initialize pygame along with display and image settings
        """
        pygame.init()
        self._display = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('SNAKE')
        self._snake = pygame.image.load("img/snake_body_mini.png").convert()
        # source for mouse: http://pixelartmaker.com/art/3d272b1bf180b60.png
        self._mouse = pygame.image.load("img/mouse_mini.png").convert()

    def on_collision(self, collision_type: str):
        """
        Print game results and exit the game
        """
        print('\nSnake collided with ' + collision_type + '. You lose!')
        print("Score: " + str(self.score))
        print("Total Frames: " + str(self.frames))  # TODO: needed?
        exit(0)  # TODO: this can be altered to a reset game with a reset function

    def snake_status(self, ai_play: bool):
        """
        Check whether the snake has eaten the mouse or encountered a collision
        """
        self.snake.update()

        # if snake eats mouse
        if self.snake.eats_mouse(self.mouse.x, self.mouse.y):
            self.mouse.x, self.mouse.y = self.mouse.generate_mouse(self.snake.body_position())
            self.score += 1
            if ai_play:
                self.q.update_reward('mouse')

        # if snake collides with itself
        if self.snake.body_collision():
            if ai_play:
                self.q.update_reward('snake')
            self.on_collision('itself')

        # if snake collides with walls
        if self.snake.wall_collision(0, self.window_width, 0, self.window_height):
            if ai_play:
                self.q.update_reward('wall')
            self.on_collision('the wall')

    def render(self):
        """
        Render the visual components of the game
        """
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
        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.snake.move_east()
            elif keys[pygame.K_LEFT]:
                self.snake.move_west()
            elif keys[pygame.K_UP]:
                self.snake.move_north()
            elif keys[pygame.K_DOWN]:
                self.snake.move_south()
            elif keys[pygame.K_ESCAPE]:
                self._running = False

            self.snake_status(ai_play=False)
            self.render()

            time.sleep(float(delay) / 1000.0)
            self.frames += 1

    def ai_play(self, delay: int):
        """
        Executes the game play, snake movements, and loops until the game ends.
        Movements are implemented by the AI rather than by a human pressing keys.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        """

        while self._running:
            pygame.event.pump()

            snake_head = self.snake.head_coordinates()
            mouse_loc = self.mouse.relative_coordinates(snake_head)
            tail_loc = self.snake.tail_coordinates()
            state = self.q.define_state(tail_loc, mouse_loc)
            action = self.q.select_action(state)
            print(f'action: {action}')  # TODO testing print, useful when snake hits walls

            if action == 'east':
                self.snake.move_east()
            elif action == 'west':
                self.snake.move_west()
            elif action == 'north':
                self.snake.move_north()
            else:        # south
                self.snake.move_south()

            snake_head = self.snake.head_coordinates()
            mouse_loc = self.mouse.relative_coordinates(snake_head)
            tail_loc = self.snake.tail_coordinates()
            next_state = self.q.define_state(tail_loc, mouse_loc)

            self.snake_status(True)
            #self.q.update(state, next_state, action)  # TODO implement
            self.q.reset_reward()
            self.render()

            time.sleep(float(delay) / 1000.0)
            self.frames += 1


def parse_args():
    """ purpose: parse command line arguments if they are available
        return: values associated with flag(s)"""

    # define arguments and types
    parser = argparse.ArgumentParser(description='A Snake game (created for training an AI), '
                                        'but also available for manual play')
    parser.add_argument('-d', metavar='delay', type=int, nargs='?', help='delays speed of snake (e.g. lower values '
                                        'result in faster snake, higher values result in slower snake', default=100)
    parser.add_argument('-ai', metavar='player_type', type=str, nargs='?', help='y/n where "y" activates AI play, '
                                        '"n" allows for manual play', default='n')

    # parse arguments
    args = parser.parse_args()
    delay = vars(args)['d']
    ai_play = vars(args)['ai']

    return delay, ai_play


if __name__ == "__main__":
    # parse command line
    delay, ai_play = parse_args()

    # initialize and select game play
    snake_game = Game()
    snake_game.pygame_init()
    if ai_play == 'y':
        snake_game.ai_play(delay)
    else:
        snake_game.human_play(delay)

    pygame.quit()
