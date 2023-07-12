import sys
import pygame
import threading
from levels.singleplayer import Singleplayer
from levels.multiplayer import Multiplayer
from levels.menu import MainMenu
from animation import Animation
from settings import *
from gui import Gui
from utilities import *

class Game:
    def __init__(self):

        # initialize pygame

        pygame.init()
        pygame.display.set_caption('Shooter v2')
        pygame.mouse.set_visible(SHOW_CURSOR)
        self.clock = pygame.time.Clock()

        # configure display window

        info = pygame.display.Info()

        # SCREEN['WIDTH'] = info.current_w
        # SCREEN['HEIGHT'] = info.current_h

        SCREEN['WIDTH'] = 1000
        SCREEN['HEIGHT'] = 1000

        self.screen = pygame.display.set_mode((SCREEN['WIDTH'], SCREEN['HEIGHT']))

        # network

        self.server = None
        self.client = None

        # resources

        self.animation = Animation()

    def initialize(self):
        self.mainMenu = MainMenu()
        self.singleplayer = Singleplayer(self)
        self.multiplayer = Multiplayer(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                if self.client != None:
                    self.multiplayer.killClient()

                if self.server != None:
                    self.multiplayer.killServer()

                pygame.quit()
                sys.exit()

            if event.type == backToMenu:
                del self.singleplayer
                del self.multiplayer
                self.singleplayer = Singleplayer(self)
                self.multiplayer = Multiplayer(self)

            if event.type == clientDisconnect and self.client != None:
                self.multiplayer.killClient()

            if event.type == killServer and self.server != None:
                self.multiplayer.killServer()


    def run(self):
        while True:

            self.handle_events()

            # main loop

            self.screen.fill('black')

            if LEVELS['mainMenu']:
                self.mainMenu.run()

            if LEVELS['singleplayer']:
                self.singleplayer.run()

            if LEVELS['multiplayer']:
                self.multiplayer.run()

            pygame.display.update()

            #TODO create functional delta time

            print(self.clock.get_fps())

            self.clock.tick()


if __name__ == '__main__':
    game = Game()
    game.initialize()
    game.run()