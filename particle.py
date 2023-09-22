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
        print('impact')

        # animation

        self.frame_index = 0
        self.animation_speed = 0.45
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
            self.image = pygame.transform.scale(self.image, (64, 64))
