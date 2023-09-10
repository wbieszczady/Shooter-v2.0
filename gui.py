from settings import *
import pygame

class Gui:
    def __init__(self, game):

        #TODO make buttons go away on level start

        #common
        self.screen = pygame.display.get_surface()
        self.game = game

        # custom cursor
        self.image_cursor = pygame.image.load('assets/player/cursor.png').convert_alpha()

        #fps count
        self.surf = pygame.surface.Surface((300, 100))
        self.surf.set_alpha(130)
        self.surf.fill((0, 0, 0))

        self.font = pygame.font.Font(None, 64)

    def show(self):
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.image_cursor, (pos[0] - 32, pos[1] - 32))
        self.screen.blit(self.surf, (800, 0))

        self.fps = str(int(self.game.clock.get_fps()))
        self.text = self.font.render(f'{self.fps} FPS', 1, (255, 255, 255))

        self.screen.blit(self.text, (850, 50))