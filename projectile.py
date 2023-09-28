import math, time, pygame, random
from animation import Animation
from threading import Thread
from particle import Trail, BulletImpact, RocketImpact, RocketTrail

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

    def destroy(self):

        for _ in range(50):
            RocketImpact(self)
        self.kill()

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def customDraw(self):
        RocketTrail(self)


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

        # general variables

        self.screen = pygame.display.get_surface()
        self.player = player
        self.spread = 0.1
        self.speed = speed

        # projectile animation

        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = player.animation.animation_player_bullet()

        # projectile heading vector

        self.radians = math.radians(player.angleHead)
        self.heading = [math.cos(self.radians) + random.uniform(-self.spread, self.spread),
                        math.sin(self.radians) + random.uniform(-self.spread, self.spread)]

        # spread

        vector = pygame.Vector2(self.heading[0], self.heading[1])
        _, self.angle = vector.as_polar()
        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -self.angle)

        # adjust spawn pos to the barrel

        self.adx, self.ady = math.cos(self.radians) * 50, math.sin(self.radians) * 50
        self.rect = self.image.get_rect(center=(player.rect.centerx + self.adx, player.rect.centery + self.ady))

        # calculated bullet pos

        self.posx, self.posy = self.rect.centerx, self.rect.centery

        # calculated bullet spawnpoint

        self.basePosX, self.basePosY = self.rect.centerx, self.rect.centery

    def customDraw(self):

        # draw projectile

        offs = (self.player.game.offset[0], self.player.game.offset[1])
        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))

        # spawn trail particle

        Trail(self)

    def destroy(self):
        #BulletImpact(self)

        self.kill()



    def update(self):

        vecx, vecy = self.heading[0] * self.speed, self.heading[1] * self.speed

        self.posx += round(vecx, 4)
        self.posy += round(vecy, 4)

        self.rect.centerx = self.posx
        self.rect.centery = self.posy