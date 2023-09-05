from settings import *
from utilities import NavigationButton
import pygame

class Gui:
    def __init__(self):

        #common
        self.screen = pygame.display.get_surface()

        # custom cursor
        self.image_cursor = pygame.image.load('assets/player/cursor.png').convert_alpha()


    def show(self):
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.image_cursor, (pos[0] - 32, pos[1] - 32))
