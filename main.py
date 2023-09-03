import sys
import pygame
import threading

import pygame_widgets

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

        self.WIDTH = info.current_w/2
        self.HEIGHT = info.current_h/2
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.gui = Gui()

        # resources

        self.animation = Animation()


        # controls

        self.level = 'mainMenu'

    def initialize(self):
        self.mainMenu = MainMenu(self)
        self.singleplayer = Singleplayer(self)

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == backToMenu:
                self.singleplayer = Singleplayer(self)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    match self.level:
                        case 'mainMenu':
                            pass
                        case 'singleplayer':
                            self.level = 'mainMenu'
                        case 'multiplayer':
                            self.level = 'mainMenu'



        pygame_widgets.update(events)


    def run(self):
        while True:

            # main loop

            self.screen.fill('black')

            self.handle_events()

            match self.level:
                case 'mainMenu':
                    self.mainMenu.run()
                case 'singleplayer':
                    self.singleplayer.run()
                case 'multiplayer':
                    pass

            self.gui.show()

            pygame.display.update()

            #TODO create functional delta time
            print(self.clock.get_fps())
            self.clock.tick()


if __name__ == '__main__':
    game = Game()
    game.initialize()
    game.run()