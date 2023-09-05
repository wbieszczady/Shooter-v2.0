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
import pygame_gui

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
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))

        # resources

        self.animation = Animation()

        # controls

        self.level = 'mainMenu'
        self.mainMenu = MainMenu(self)

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # going back to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    self.loadLevel('mainMenu')

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.mainMenu.b1:

                    self.loadLevel('singleplayer')

                if event.ui_element == self.mainMenu.b2:

                    self.loadLevel('multiplayer')


            self.manager.process_events(event)

        self.manager.update(1)
        self.manager.draw_ui(self.screen)


    def loadLevel(self, lvl):

        match lvl:

            case 'mainMenu':
                try:
                    del self.singleplayer
                except:
                    pass

                try:
                    del self.multiplayer
                except:
                    pass

            case 'singleplayer':

                self.singleplayer = Singleplayer(self)

            case 'multiplayer':

                self.multiplayer = Multiplayer(self)

        self.level = lvl
        print(f'Level loaded: {lvl}')


    def run(self):

        while True:

            # main loop

            self.screen.fill('black')

            self.handle_events()


            match self.level:

                case 'mainMenu':
                    pass

                case 'singleplayer':
                    self.singleplayer.run()

                case 'multiplayer':
                    self.multiplayer.run()

            self.gui.show()

            pygame.display.update()

            print(self.clock.get_fps())

            print(threading.active_count())

            self.clock.tick()


if __name__ == '__main__':
    game = Game()
    game.run()