import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.group_objects)
        self.game = game

        self.pos = pos
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/obstacles/box.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.health = 10

    def destroy(self):
        self.health -= 1

        if self.health == 0:
            self.kill()

    def update(self):
        offset = self.game.offset

        self.screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


class Border(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.group_objects)
        self.game = game

        self.pos = pos
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load('assets/obstacles/border.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        pass

    def update(self):
        offset = self.game.offset

        self.screen.blit(self.image, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


