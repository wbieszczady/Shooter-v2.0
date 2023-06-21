import pygame, sys
from settings import *
from singleplayer import MainMenu, Singleplayer
from utilities import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Shooter v2')

        pygame.mouse.set_visible(SHOW_CURSOR)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def initialize(self):
        self.mainMenu = MainMenu()
        self.singleplayer = Singleplayer()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == backToMenu:
                    del self.singleplayer
                    self.singleplayer = Singleplayer()

            # main loop

            self.screen.fill('black')

            if LEVELS['mainMenu']:
                self.mainMenu.run()

            if LEVELS['singleplayer']:
                self.singleplayer.run()


            pygame.display.update()
            #print(self.clock.get_fps())

            self.clock.tick(FPS)




if __name__ == '__main__':
    game = Game()
    game.initialize()
    game.run()