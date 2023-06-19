import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/obstacles/box.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        self.kill()

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)



class Border(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/obstacles/border.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def destroy(self):
        pass

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

