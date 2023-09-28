import pygame
import random
import math

class Trail(pygame.sprite.Sprite):

    def __init__(self, projectile):

        super().__init__(projectile.player.group_particles)

        # general
        self.screen = pygame.display.get_surface()
        self.projectile = projectile

        # animation

        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = projectile.player.animation.animation_particle_trail()

        self.opacity = 254

        # rect

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -self.projectile.angle)
        self.rect = self.image.get_rect(center=(projectile.rect.centerx, projectile.rect.centery))

    def decay(self):
        if self.opacity > 0:
            self.opacity -= 2
            self.image.set_alpha(self.opacity)
        else:
            self.kill()

    def update(self):
        self.decay()

    def customDraw(self):

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])
        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))



class RocketTrail(pygame.sprite.Sprite):

    def __init__(self, projectile):
        super().__init__(projectile.player.group_particles)

        # general
        self.screen = pygame.display.get_surface()
        self.projectile = projectile

        # animation
        self.frame_index = 0
        self.animation_speed = 0.05
        self.frames = projectile.player.animation.animation_particle_rocket_trail()

        # rect
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(projectile.rect.centerx + -self.projectile.heading[0] * 20,
                                                projectile.rect.centery + -self.projectile.heading[1] * 20))

        # base pos
        self.posX = self.rect.centerx
        self.posY = self.rect.centery

        self.dirX, self.dirY = -self.projectile.heading[0] + random.uniform(-1.5, 1.5), \
                               -self.projectile.heading[1] + random.uniform(-1.5, 1.5)

        # opacity

        self.opacity = 255

    def decay(self):
        if self.opacity > 0:
            self.opacity -= 2
            self.image.set_alpha(self.opacity)
        else:
            self.kill()

    def update(self):
        self.decay()

        self.posX += self.dirX
        self.posY += self.dirY

        self.rect.centerx = self.posX
        self.rect.centery = self.posY


    def customDraw(self):

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])
        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))


class BulletImpact(pygame.sprite.Sprite):

    def __init__(self, projectile):
        super().__init__(projectile.player.group_particles)

        # general
        self.screen = pygame.display.get_surface()
        self.projectile = projectile

        # animation

        self.frame_index = 0
        self.animation_speed = 0.05
        self.frames = projectile.player.animation.animation_particle_bullet_impact()

        # rect

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(projectile.rect.centerx, projectile.rect.centery))

    def animate(self):

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

    def customDraw(self):

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))
class RocketImpact(pygame.sprite.Sprite):

    def __init__(self, projectile):
        super().__init__(projectile.player.group_particles)

        # general
        self.screen = pygame.display.get_surface()
        self.projectile = projectile

        # animation

        self.frame_index = 0
        self.animation_speed = 0.05
        self.frames = projectile.player.animation.animation_particle_rocket_impact()

        # rect

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(projectile.rect.centerx, projectile.rect.centery))

        # random vectors
        self.velX = random.uniform(-8.0, 8.0)
        self.velY = random.uniform(-8.0, 8.0)

        self.scale = 32

    def destroy(self):

        self.kill()

    def update(self):

        self.rect.x += self.velX
        self.rect.y += self.velY

        if self.scale < 0:
            self.destroy()

        self.scale -= 0.2

        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))


    def customDraw(self):

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))