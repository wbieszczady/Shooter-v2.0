import pygame, sys
from settings import *
from level import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Shooter v3')

        pygame.mouse.set_visible(SHOW_CURSOR)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.settings = DynamicSettings()

        self.level = Level()
        self.mainMenu = MainMenu(self.settings)

    def select_state(self):
        if self.settings.get_MAIN_MENU():
            self.mainMenu.run()
        else:
            self.level.run()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')

            self.select_state()

            pygame.display.update()
            #print(self.clock.get_fps())

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()