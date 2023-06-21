import pygame
from settings import *
from utilities import center_position, NavigationButton


class Gui:
    def __init__(self):

        #common
        self.screen = pygame.display.get_surface()


        # menu gui
        self.surface = pygame.surface.Surface((WIDTH, HEIGHT))
        self.surface = self.surface.convert_alpha()
        self.surface.fill((0, 0, 0, 190))

        self.image_bMenu = pygame.image.load('assets/menu/backToMenu.png').convert_alpha()
        self.rect_bMenu = self.image_bMenu.get_rect()
        self.rect_bMenuPos = center_position(self.rect_bMenu, -400, -550)


        # custom cursor
        self.image_cursor = pygame.image.load('assets/player/cursor.png').convert_alpha()

    def showMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.image_cursor, (self.mouse_pos[0] - 32, self.mouse_pos[1] - 32))

    def gameMenu(self):
        self.image_bMenuFinal = NavigationButton(self.rect_bMenu, self.image_bMenu, self.image_bMenu, True)
        self.surface.blit(self.image_bMenuFinal, self.rect_bMenuPos)
        self.screen.blit(self.surface, (0, 0))




class Debug:
    def __init__(self, players):
        self.screen = pygame.display.get_surface()
        self.my_font = pygame.font.SysFont('Verdana', 30)
        self.clock = pygame.time.Clock()
        self.players = players

        # self.head_info = my_font.render(f'Head angle: {self.angleHead}', False, (255, 255, 255))
        # self.body_info = my_font.render(f'Body angle: {self.angleBody}', False, (255, 255, 255))
        # self.body_dir_info = my_font.render(f'Body direction: {self.directionBody}', False, (255, 255, 255))

    def debugMode(self):
        self.clock.tick()
        self.fpsCount = self.clock.get_fps()
        self.fps = self.my_font.render(f'FPS: {round(self.fpsCount, 1)}', False, (255, 255, 255))
        self.screen.blit(self.fps, (0, 0))
        for player in self.players:
            mouse = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, (255, 255, 255), player.rect.center, mouse, 3)


        # pygame.draw.line(self.screen, (255, 255, 255), self.rect.center, self.rect.center + self.directionBody * 7, 5)
        # pygame.draw.line(self.screen, (255, 255, 255), self.rect.center, self.rect.center + -self.directionBody * 7, 5)
        #
        # pygame.draw.rect(self.screen, (128, 128, 128), pygame.Rect(0, 0, 600, 120))
        # self.screen.blit(head_info, (0, 0))
        # self.screen.blit(body_info, (0, 40))
        # self.screen.blit(body_dir_info, (0, 80))

