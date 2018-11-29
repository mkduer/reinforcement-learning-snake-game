import pygame
import argparse
from time import sleep
import os

from mouse import Mouse
from snake import Snake
from q_learning import QLearning
import constant


class Game:

    def __init__(self):
        self.window_width = constant.WIDTH * constant.TILE
        self.window_height = constant.HEIGHT * constant.TILE

        self._running = True
        self._display = None
        self._snake = None
        self._mouse = None

        self.training_session = 1
        self.episode = 1
        self.score = 0
        self.max_score = 0
        self.frames = 0
        self.game_stats = []

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

    def game_over(self, collision_type: str, total_episodes: int):
        """
        Print game results and exit the game
        """
        self.snake.update_tail()
        self._running = False

        if self.score > self.max_score:
            self.max_score = self.score
        episode_data = [self.frames, self.score, collision_type]
        self.game_stats.append(episode_data)

        self.display(collision_type)
        self.next_episode(total_episodes)

    def display(self, collision_type: str):
        """
        Displays game over status and scores, and can call display/save data functions
        :param collision_type: what type of collision ended the game
        """
        if self.episode % constant.SAVE_EPISODE == 0:
            #self.q.display_table()  # optional TODO: delete at the end of the project
            self.q.save_table(self.episode, clear_dir=constant.DELETE_DIR)
        print(f'GAME OVER! Snake collided with {collision_type}')
        print(f'SCORE: {self.score}')

    def move_snake(self, ai_play: bool, total_episodes: int):
        """
        Check whether the snake has eaten the mouse or encountered a collision
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
            self.game_over('itself', total_episodes)

        # if snake collides with walls
        elif self.snake.wall_collision(0, self.window_width, 0, self.window_height):
            if ai_play:
                self.q.update_reward('wall')
            self.game_over('the wall', total_episodes)

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

    def human_play(self, delay: int, total_episodes: int):
        """
        Executes the game play, snake movements, and loops until the game ends.
        Keys can be used to play the game.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        :param total_episodes: total number of episodes to run the game
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

            self.move_snake(False, total_episodes)
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

    def ai_train(self, delay: int, total_episodes: int, saved_table: bool):
        """
        Executes the AI training, looping until the snake is trained the total number of episodes.
        Movements are implemented by the AI rather than by a human pressing keys.
        :param delay: defines the frame delay with lower values (e.g. 1) resulting in a fast frame, while higher values
        (e.g. 1000) result in very slow frames
        :param total_episodes: total number of episodes to run the game
        :param saved_table: if True, start training from externally saved table's next episode, if False,
        initial episode is 1
        """

        # If resuming from a saved table state, load the state and start from the loaded
        # state's NEXT episode
        if saved_table:
            filename = 'episode' + str(constant.RESUME_EPISODE) + '.json'
            self.episode = self.q.load_table(filename)
            exit(0)  # TODO delete

        while self._running:
            pygame.event.pump()

            tail_loc, mouse_loc = self.abs_coordinates()
            state = self.q.define_state(tail_loc, mouse_loc)
            action = self.q.select_action(state)

            self.set_direction(action)
            self.move_snake(True, total_episodes)

            tail_loc, mouse_loc = self.abs_coordinates()
            next_state = self.q.define_state(tail_loc, mouse_loc)
            self.q.update(state, next_state, action)
            self.q.reset_reward()

            self.render()

            sleep(float(delay) / 1000)
            self.frames += 1

    def ai_test(self, delay: int):
        """
        Tests the AI on previous training data
        :param delay: defines the frame delay
        """
        caption = 'SNAKE ' + 'FINAL TEST RUN'
        self.reset_game(caption)

        while self._running:
            pygame.event.pump()

            tail_loc, mouse_loc = self.abs_coordinates()
            state = self.q.define_state(tail_loc, mouse_loc)
            action = self.q.select_action(state)

            self.set_direction(action)
            self.move_snake(True, 1)
            self.render()

            sleep(float(delay) / 1000)
            self.frames += 1

        print(f'(TEST RUN) FINAL SCORE: {self.score}, FINAL MAX SCORE: {self.max_score}')

    def reset_game(self, caption: str):
        pygame.display.set_caption(caption)
        self.score = 0
        self.frames = 0
        self._running = True
        self.snake.initialize_positions(self.mouse.x, self.mouse.y)
        self.mouse.generate_mouse(self.snake.body_position())

    def next_episode(self, total_episodes: int):
        """
        Sets-up the next episode or completes the final episode
        :param total_episodes: total number of episodes
        """
        if self.episode >= total_episodes:
            self.write_data()
            return

        # set new episode
        self.episode += 1
        print(f'\nNEW GAME, EPISODE {self.episode}')
        caption = 'SNAKE ' + 'Episode ' + str(self.episode)
        self.reset_game(caption)
        
    def write_data(self):
        path = constant.DATA_DIR
        header = 'Episode, Steps, Score, Collision\n'
        filename = path + 'data' + str(self.training_session) + '.csv'

        # create directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)

        # write data to csv file(s)
        with open(filename, 'w') as outfile:
            outfile.write(header)

            for i in range(0, len(self.game_stats)):
                out_str = str(i + 1)
                for j in range(0, len(self.game_stats[i])):
                    out_str = out_str + ',' + str(self.game_stats[i][j])
                outfile.write(out_str + '\n')


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
    game = Game()
    game.initialize_pygame()

    # select game play
    if ai == 'y':
        game.ai_train(delayed, total_episode_number, constant.RESUME_FILE)
        print(f'\nTEST RUN:')
        game.ai_test(delayed)
    else:
        game.human_play(delayed, total_episode_number)

    pygame.quit()
