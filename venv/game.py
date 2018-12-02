import pygame
import argparse
from time import sleep
import os
import csv

from mouse import Mouse
from snake import Snake
from q_learning import QLearning
import constant


class Game:

    def __init__(self, total_episodes: int):
        self.window_width = constant.WIDTH * constant.TILE
        self.window_height = constant.HEIGHT * constant.TILE

        self._running = True
        self._display = None
        self._snake = None
        self._mouse = None

        self.episode = 1
        self.total_episodes = total_episodes
        self.score = 0
        self.max_score = 0
        self.frames = 0
        self.game_stats = []
        self.specs = []
        self.test_run = False

        self.snake = Snake()
        self.mouse = Mouse(constant.WIDTH, constant.HEIGHT, self.snake.body_position())
        self.q = QLearning()

    def initialize_pygame(self):
        """
        Initialize pygame along with display and image settings
        """
        pygame.init()
        self._display = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('SNAKE ' + 'Episode ' + str(self.episode))
        self._snake = pygame.image.load("img/snake_body_mini.png").convert()
        # source for mouse: http://pixelartmaker.com/art/3d272b1bf180b60.png
        self._mouse = pygame.image.load("img/mouse_mini.png").convert()

    def game_over(self, collision_type: str):
        """
        Print game results and exit the game
        """
        collision_value = -1  # represents body collision
        if collision_type == 'the wall':
            collision_value = 1

        self.snake.update_tail()
        self._running = False

        if self.score > self.max_score:
            self.max_score = self.score
        self.game_stats.append([self.frames, self.score, collision_value])
        self.display(collision_type)
        self.next_episode()

    def display(self, collision_type: str):
        """
        Displays game over status and scores, and can call display/save data functions
        :param collision_type: what type of collision ended the game
        """
        if self.episode % constant.SAVE_EPISODE == 0:
            #self.q.display_table()  # optional TODO: delete at the end of the project
            self.q.save_table(self.episode, clear_dir=constant.DELETE_JSON)
        print(f'GAME OVER! Snake collided with {collision_type}')
        print(f'SCORE: {self.score}')

    def move_snake(self, ai_play: bool):
        """
        Check whether the snake has eaten the mouse or encountered a collision
        :param ai_play: True if ai play, False otherwise
        """
        self.snake.update_head()

        # if snake eats mouse
        if self.snake.eats_mouse(self.mouse.x, self.mouse.y):
            self.mouse.generate_mouse(self.snake.body_position())
            self.score += 1
            if ai_play:
                self.q.update_reward('mouse')

        # if snake collides with itself
        elif self.snake.body_collision():
            if ai_play:
                self.q.update_reward('snake')
            self.game_over('itself')

        # if snake collides with walls
        elif self.snake.wall_collision(0, self.window_width, 0, self.window_height):
            if ai_play:
                self.q.update_reward('wall')
            self.game_over('the wall')

        else:
            if ai_play:
                self.q.update_reward('empty')
            self.snake.update_tail()

    def abs_coordinates(self):
        snake_head = self.snake.head_coordinates()
        mouse_loc = self.mouse.relative_coordinates(snake_head)
        tail_loc = self.snake.tail_coordinates()
        return tail_loc, mouse_loc

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
                self.snake.set_east()
            elif keys[pygame.K_LEFT]:
                self.snake.set_west()
            elif keys[pygame.K_UP]:
                self.snake.set_north()
            elif keys[pygame.K_DOWN]:
                self.snake.set_south()
            elif keys[pygame.K_ESCAPE]:
                self._running = False

            self.move_snake(False)
            self.render()
            sleep(float(delay) / 1000)
            self.frames += 1

    def set_direction(self, direction: str):
        """
        Sets the direction for the snake to take
        :param direction: specified direction
        """
        if direction == 'east':
            self.snake.set_east()
        elif direction == 'west':
            self.snake.set_west()
        elif direction == 'north':
            self.snake.set_north()
        else:        # south
            self.snake.set_south()

    def ai_train(self, delay: int, resume_state: bool):
        """
        Executes the AI training, looping until the snake is trained the total number of episodes.
        Movements are implemented by the AI rather than by a human pressing keys.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        :param resume_state: if True, start training from externally saved table's next episode, if False,
        initial episode is 1
        """

        # If resuming from a saved state, start from the loaded state's next episode
        if resume_state:
            self.resume_game(self.total_episodes)

        while self._running:
            pygame.event.pump()

            tail_loc, mouse_loc = self.abs_coordinates()
            snake_direction = self.snake.current_direction()
            state = self.q.define_state(tail_loc, mouse_loc, snake_direction)
            action = self.q.select_action(state)

            self.set_direction(action)
            self.move_snake(True)

            tail_loc, mouse_loc = self.abs_coordinates()
            snake_direction = self.snake.current_direction()
            next_state = self.q.define_state(tail_loc, mouse_loc, snake_direction)
            self.q.update(state, next_state, action)
            self.q.reset_reward()

            self.render()

            sleep(float(delay) / 1000)
            self.frames += 1

    def ai_test(self, delay: int, resume_state: bool):
        """
        Tests the AI on previous training data
        :param delay: defines the frame delay
        :param resume_state: if True, start training from externally saved table's next episode, if False,
        initial episode is 1
        """
        self.test_run = True
        self.episode = 1

        # If resuming from a saved state, start from the loaded state's next episode
        if resume_state:
            self.resume_game(constant.TOTAL_TESTS)

        if constant.PARAM_TEST:
            self.total_episodes = constant.TOTAL_TESTS

        # Run the total number of tests specified
        while self.episode <= self.total_episodes:
            caption = 'SNAKE ' + 'FINAL TEST RUN: EPISODE ' + str(self.episode)
            self.reset_game(caption)
            self.game_stats = []
            self.specs = []

            while self._running:
                pygame.event.pump()

                tail_loc, mouse_loc = self.abs_coordinates()
                snake_direction = self.snake.current_direction()
                state = self.q.define_state(tail_loc, mouse_loc, snake_direction)
                action = self.q.select_action(state)

                self.set_direction(action)
                self.move_snake(True)
                self.render()

                sleep(float(delay) / 1000)
                self.frames += 1
            print(f'(TEST RUN EPISODE {str(self.episode)}) FINAL SCORE: {self.score}, FINAL MAX SCORE: {self.max_score}\n')
            self.episode += 1

        print(f'EXITING FUNCTION')
        return

    def resume_game(self, total_tests):
        filename = 'episode' + str(constant.RESUME_EPISODE) + '.json'
        self.episode = self.q.load_table(filename)
        if self.episode < 1:
            print(f'Table failed to load')
        self.total_episodes = self.episode + total_tests - 1

    def reset_game(self, caption: str):
        pygame.display.set_caption(caption)
        self.score = 0
        self.frames = 0
        self._running = True
        self.snake.initialize_positions(self.mouse.x, self.mouse.y)
        self.mouse.generate_mouse(self.snake.body_position())

    def next_episode(self):
        """
        Sets-up the next episode or completes the final episode
        """
        if self.episode >= self.total_episodes:
            self.prep_data()
            return

        # set new episode
        self.episode += 1
        print(f'\nNEW GAME, EPISODE {self.episode}')
        caption = 'SNAKE ' + 'Episode ' + str(self.episode)
        self.reset_game(caption)

    def prep_data(self):
        """
        Prepares data formatting with headers, specific test names, etc
        """
        print(f'in prep_data()')
        self.specs = []
        filename = ''

        if self.test_run:
            filename = 'testing_' + constant.PARAM + str(constant.PARAM_VAL)

        if constant.PARAM_TEST:
            filename += constant.PARAM + str(constant.PARAM_VAL)

        stats_file = filename + '_data.csv'
        header = ['Steps', 'Scores', 'Collisions']
        self.write_data(stats_file, header, self.game_stats)

        specs_file = filename + '_specs.csv'
        header = ['Parameters', 'Values']
        self.specs.append(['total episodes', self.episode])
        self.specs.append(['height', constant.HEIGHT])
        self.specs.append(['width', constant.WIDTH])
        self.specs.append(['learning rate', constant.ETA])
        self.specs.append(['discount', constant.DISCOUNT])
        self.specs.append(['epsilon', constant.EPSILON])
        self.specs.append(['mouse reward', constant.MOUSE])
        self.specs.append(['wall penalty', constant.WALL])
        self.specs.append(['self-collision penalty', constant.SNAKE])
        self.specs.append(['empty tile penalty', constant.EMPTY])
        self.write_data(specs_file, header, self.specs, True)

    def write_data(self, filename: str, header: [str], data: [], add_specs: bool=False):
        """
        Writes the data from the current session to a file.
        :param filename: filename to write data
        :param header: header names for data
        :param data: data to add to file
        :param add_specs: True if writing specs file, False otherwise
        """
        op = 'w'  # default write to CSV
        path = constant.DATA_DIR
        file = path + filename

        # create directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)

        # append data to existing file
        if constant.RESUME and os.path.isfile(file):
            op = 'a'

        # write specs
        if add_specs:
            op = 'w'

        # write data to csv file(s)
        with open(file, op, newline='') as outfile:
            w = csv.writer(outfile)

            if not constant.RESUME:
                w.writerow(header)

            w.writerows(data)
        outfile.close()


def parse_args():
    """
    Parse command line arguments if they are available
    :return: values associated with flag(s)
    """
    parser = argparse.ArgumentParser(description='A Snake game (created for training an AI), '
                                                 'but also available for manual play')
    parser.add_argument('-d', metavar='delay', type=int, nargs='?',
                        help='delays speed of snake (e.g. lower values result in faster snake, '
                             'higher values result in slower snake', default=constant.DELAY)
    parser.add_argument('-ai', metavar='player type', type=str, nargs='?',
                        help='y/n where "y" activates AI play, "n" allows for manual play', default='n')
    parser.add_argument('-i', metavar='number of episodes', type=int, nargs='?',
                        help='number of q-learning episodes', default=constant.EPISODES)

    # parse arguments
    args = parser.parse_args()
    delay = vars(args)['d']
    ai_play = vars(args)['ai']
    episodes = vars(args)['i']
    return delay, ai_play, episodes


if __name__ == "__main__":

    # parse command line
    delayed, ai, total_episode_number = parse_args()

    # initialize
    game = Game(total_episode_number)
    game.initialize_pygame()

    # AI play
    if ai == 'y':
        if constant.PARAM_TEST:
            print(f'\nTRAINING RUNS:')
            game.ai_train(delayed, constant.RESUME)
            print(f'\nTEST RUN:')
            game.ai_test(delayed, False)
        else:
            print(f'\nTEST RUNS:')
            game.ai_test(delayed, constant.RESUME)
    # human play
    else:
        game.human_play(delayed)

    pygame.quit()
