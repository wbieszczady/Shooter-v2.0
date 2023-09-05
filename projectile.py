import math, time, pygame
from animation import Animation
from threading import Thread

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, angle, animation):
        super().__init__(group)
        self.screen = pygame.display.get_surface()

        self.radians = math.radians(angle)
        self.heading = [math.cos(self.radians), math.sin(self.radians)]

        # projectile animation
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = animation.animation_player_bullet()
        #print(round(self.heading[0], 3) * 10, round(self.heading[1], 3) * 10)

        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], -angle)
        self.rect = self.image.get_rect(center = (pos[0] + self.heading[0] * 70, pos[1] + self.heading[1] * 70))

        self.bulletHandler = Thread(target=self.update, daemon=True)
        self.bulletHandler.start()


    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def update(self):
        while self.alive():
            try:
                self.rect.x += round(self.heading[0] * 10, 3)
                self.rect.y += round(self.heading[1] * 10, 3)
            except:
                pass
            time.sleep(0.010)