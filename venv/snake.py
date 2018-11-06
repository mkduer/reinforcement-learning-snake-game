"""
Source of original game is a tutorial for building snake with pygame:
  https://pythonspot.com/snake-with-pygame/

Modifications:
  - different visual components
  - code cleaned to reduce unnecessary if statements, change variable names
  - separate classes into different files
  - add functionality for wall collisions
"""

from pygame.locals import *
from random import randint
import pygame
import time
from mouse import Mouse
from player import Player
from game import Game


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0
    mouse = 0

    def __init__(self):
        self._running = True
        self._display = None
        self._snake = None
        self._mouse = None
        self.game = Game()
        self.player = Player(1)
        self.mouse = Mouse(5, 5)

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('SNAKE: Modified from original source pythonspot.com')
        self._running = True
        self._snake = pygame.image.load("img/snake_body_mini.png").convert()
        # source for mouse: http://pixelartmaker.com/art/3d272b1bf180b60.png
        self._mouse = pygame.image.load("img/mouse_mini.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat mouse?
        for i in range(0, self.player.length):
            if self.game.isCollision(self.mouse.x, self.mouse.y, self.player.x[i], self.player.y[i], 44):
                self.mouse.x = randint(2, 9) * 44
                self.mouse.y = randint(2, 9) * 44
                self.player.length = self.player.length + 1

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)

        # does snake collide with walls?
        if self.game.isWallCollision(0, self.windowWidth, 0, self.windowHeight, self.player.x[0], self.player.y[0]):
            print("You lose! Collision: ")
            print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
            exit(0)

    def on_render(self):
        self._display.fill((0, 0, 0))
        self.player.draw(self._display, self._snake)
        self.mouse.draw(self._display, self._mouse)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()
            elif (keys[K_LEFT]):
                self.player.moveLeft()
            elif (keys[K_UP]):
                self.player.moveUp()
            elif (keys[K_DOWN]):
                self.player.moveDown()
            elif (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()