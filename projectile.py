import math, time, pygame
from cooldown import Decay
from animation import Animation

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, angle, animation):
        super().__init__(group)
        self.screen = pygame.display.get_surface()

        self.decay = Decay()
        self.decayTime = 100

        self.radians = math.radians(angle)
        self.heading = [math.cos(self.radians), math.sin(self.radians)]

        # projectile animation
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = animation.animation_player_bullet()

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -angle)
        self.rect = self.image.get_rect(center = (pos[0] + self.heading[0] * 70, pos[1] + self.heading[1] * 70))

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def update(self):
        self.decay.bulletDecay(self)
        self.rect.x += round(self.heading[0] * 20)
        self.rect.y += round(self.heading[1] * 20)