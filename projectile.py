import math, time, pygame
from animation import Animation
from threading import Thread

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, pos, group, angle, animation):

        #TODO get all this class arguments opt

        super().__init__(group)

        self.player = player
        self.screen = pygame.display.get_surface()

        self.radians = math.radians(angle)
        self.heading = [math.cos(self.radians), math.sin(self.radians)]

        # projectile animation
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = animation.animation_player_bullet()
        #print(round(self.heading[0], 3) * 10, round(self.heading[1], 3) * 10)

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -angle)

        # adjusting bullet pos to barrel pos

        adx, ady = self.heading[0] * 70, self.heading[1] * 70

        self.rect = self.image.get_rect(center = (pos[0] + adx, pos[1] + ady))

        # float pos setup
        self.posx, self.posy = self.rect.x, self.rect.y

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def update(self):
        vecx, vecy = self.heading[0] * 5, self.heading[1] * 5

        self.posx += round(vecx, 4)
        self.posy += round(vecy, 4)

        self.rect.x = self.posx
        self.rect.y = self.posy