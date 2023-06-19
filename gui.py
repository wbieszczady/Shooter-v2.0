import pygame


class Gui:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        # custom cursor
        self.image = pygame.image.load('assets/player/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()


    def showMouse(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.image, (self.mouse_pos[0] - 32, self.mouse_pos[1] - 32))


class Debug:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.my_font = pygame.font.SysFont('Verdana', 30)
        self.clock = pygame.time.Clock()

        # self.head_info = my_font.render(f'Head angle: {self.angleHead}', False, (255, 255, 255))
        # self.body_info = my_font.render(f'Body angle: {self.angleBody}', False, (255, 255, 255))
        # self.body_dir_info = my_font.render(f'Body direction: {self.directionBody}', False, (255, 255, 255))

    def debugMode(self):
        self.clock.tick()
        self.fpsCount = self.clock.get_fps()
        self.fps = self.my_font.render(f'FPS: {round(self.fpsCount, 1)}', False, (255, 255, 255))
        self.screen.blit(self.fps, (0, 0))

        # pygame.draw.line(self.screen, (255, 255, 255), self.rect.center, self.rect.center + self.directionBody * 7, 5)
        # pygame.draw.line(self.screen, (255, 255, 255), self.rect.center, self.rect.center + -self.directionBody * 7, 5)
        #
        # pygame.draw.rect(self.screen, (128, 128, 128), pygame.Rect(0, 0, 600, 120))
        # self.screen.blit(head_info, (0, 0))
        # self.screen.blit(body_info, (0, 40))
        # self.screen.blit(body_dir_info, (0, 80))

