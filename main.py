import sys
from levels.singleplayer import Singleplayer
from levels.multiplayer import Multiplayer
from levels.menu import MainMenu
from gui import Gui
from utilities import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Shooter v2')

        pygame.mouse.set_visible(SHOW_CURSOR)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.server = None

    def initialize(self):
        self.mainMenu = MainMenu()
        self.singleplayer = Singleplayer()
        self.multiplayer = Multiplayer(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.server != None:
                    self.multiplayer.killServer()
                self.multiplayer.clientDisconnect()

                pygame.quit()
                sys.exit()

            if event.type == backToMenu:
                del self.singleplayer
                del self.multiplayer
                self.singleplayer = Singleplayer()
                self.multiplayer = Multiplayer(self)

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
            #print(self.clock.get_fps())

            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.initialize()
    game.run()