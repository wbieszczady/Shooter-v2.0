import pygame
import random

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

        # rect

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -projectile.angle)
        self.rect = self.image.get_rect(center=(projectile.player.rect.centerx + projectile.adx * 2, projectile.player.rect.centery + projectile.ady * 2))

        # scale



    def customDraw(self):
        offs = (self.projectile.player.game.offset[0], self.projectile.player.game.offset[1])



        self.screen.blit(self.image, (self.rect.x + offs[0], self.rect.y + offs[1]))

        self.screen.blit(self.image, (self.rect.x + offs[0] + self.projectile.heading[0] * 50, self.rect.y + offs[1] + self.projectile.heading[1] * 50))


