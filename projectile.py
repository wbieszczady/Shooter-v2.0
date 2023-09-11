import math, time, pygame, random
from animation import Animation
from threading import Thread

class Rocket(pygame.sprite.Sprite):
    def __init__(self, player, speed):

        super().__init__(player.group_projectiles)

        self.screen = pygame.display.get_surface()

        self.player = player

        self.radians = math.radians(player.angleHead)
        self.heading = [math.cos(self.radians), math.sin(self.radians)]

        self.speed = speed

        # projectile animation
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = player.animation.animation_player_rocket()

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -player.angleHead)

        # adjusting bullet pos to barrel pos

        adx, ady = self.heading[0] * 70, self.heading[1] * 70

        self.rect = self.image.get_rect(center = (player.rect.centerx + adx, player.rect.centery + ady))

        # float pos setup
        self.posx, self.posy = self.rect.x, self.rect.y

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def customDraw(self):
        offs = (self.player.game.offset[0], self.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))

    def update(self):
        vecx, vecy = self.heading[0] * self.speed, self.heading[1] * self.speed

        self.posx += round(vecx, 4)
        self.posy += round(vecy, 4)

        self.rect.x = self.posx
        self.rect.y = self.posy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, speed):

        super().__init__(player.group_projectiles)

        self.screen = pygame.display.get_surface()

        self.player = player

        self.spread = 0.4

        self.radians = math.radians(player.angleHead)
        self.heading = [math.cos(self.radians) + random.uniform(-self.spread, self.spread), math.sin(self.radians) + random.uniform(-self.spread, self.spread)]

        self.speed = speed

        #projectile animation
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = player.animation.animation_player_bullet()

        #spread

        vector = pygame.Vector2(self.heading[0], self.heading[1])

        _, angle = vector.as_polar()

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -angle)

        # adj
        self.adx, self.ady = math.cos(self.radians) * 70, math.sin(self.radians) * 70

        self.rect = self.image.get_rect(center=(player.rect.centerx + self.adx, player.rect.centery + self.ady))

        self.outline_pos = self.rect.x, self.rect.y

        # float pos setup
        self.posx, self.posy = self.rect.x, self.rect.y

    def outline(self):
        offs = (self.player.game.offset[0], self.player.game.offset[1])

        pygame.draw.line(self.screen, (255, 255, 255), (self.outline_pos[0] + offs[0], self.outline_pos[1] + offs[1]), (self.posx + offs[0], self.posy + offs[1]))

    def customDraw(self):
        offs = (self.player.game.offset[0], self.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))

        self.outline()

    def update(self):

        vecx, vecy = self.heading[0] * self.speed, self.heading[1] * self.speed

        self.posx += round(vecx, 4)
        self.posy += round(vecy, 4)

        self.rect.x = self.posx
        self.rect.y = self.posy