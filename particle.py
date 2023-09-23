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
    def customDraw(self):
        self.decay()

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))
    def decay(self):
        if self.opacity > 0:
            self.opacity -= 2
            self.image.set_alpha(self.opacity)
        else:
            self.kill()
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

    def customDraw(self):
        self.animate()

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))

    def animate(self):

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
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
        self.velX = random.uniform(-4.0, 4.0)
        self.velY = random.uniform(-4.0, 4.0)

        self.scale = 32

    def update(self):
        self.rect.x += self.velX
        self.rect.y += self.velY

        if self.scale < 0:
            self.kill()

        self.scale -= 0.2

        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))


    def customDraw(self):

        self.update()

        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])

        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))



    # def animate(self):
    #
    #     self.frame_index += self.animation_speed
    #     if self.frame_index >= len(self.frames):
    #         self.kill()
    #     else:
    #         self.image = self.frames[int(self.frame_index)]