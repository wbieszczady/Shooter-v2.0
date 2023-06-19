import pygame, math
from time import time
from pygame import Vector2
from projectile import Bullet
from cooldown import Cooldown
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, animation):
        super().__init__(group)

        #common attributes

        self.screen = pygame.display.get_surface()
        self.group = group

        self.isMoving = False
        self.isRotating = False
        self.isMovingForward = False

        #player body

        self.image = pygame.image.load('assets/player/player.png').convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.directionBody = Vector2(0, -6)

        #player head

        self.imageHead = pygame.image.load('assets/player/playerHead.png').convert_alpha()
        self.orig_imageHead = self.imageHead
        self.rectHead = self.imageHead.get_rect(topleft = pos)

        #player animations

        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = animation.animation_player_move()
        self.animation = animation

        #player projectiles
        self.bulletCooldownCheck = Cooldown()
        self.bulletCooldown = 45 # [ms]

        self.group_bullet = pygame.sprite.Group()

    def rotateHead(self):

        self.posHead = Vector2(self.rect.center)

        self.directionHead = pygame.mouse.get_pos() - self.posHead
        self.radiusHead, self.angleHead = self.directionHead.as_polar()
        self.angleHead = round(self.angleHead, 0)

        self.imageHead = pygame.transform.rotate(self.orig_imageHead, -self.angleHead)
        self.rectHead = self.imageHead.get_rect(center=(self.rect.centerx, self.rect.centery))

    def rotateBody(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.directionBody.rotate_ip(-2)
        if keys[pygame.K_d]:
            self.directionBody.rotate_ip(2)

        if keys[pygame.K_d] or keys[pygame.K_a]:
            self.isRotating = True
        else:
            self.isRotating = False

        self.angleBody = round(self.directionBody.angle_to((6, 0)), 2)

        self.image = pygame.transform.rotate(self.orig_image, self.angleBody)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        keys = pygame.key.get_pressed()

        heading = int(self.directionBody[0]), int(self.directionBody[1])

        if keys[pygame.K_w]:
            self.rect.x += heading[0]
            self.rect.y += heading[1]

        if keys[pygame.K_s]:
            self.rect.x -= heading[0]
            self.rect.y -= heading[1]


        if keys[pygame.K_w]:
            self.isMoving = True
            self.isMovingForward = True
        elif keys[pygame.K_s]:
            self.isMoving = True
            self.isMovingForward = False
        else:
            self.isMoving = False
            self.isMovingForward = None

    def bounce(self):
        if self.isMovingForward:
            heading = int(-self.directionBody[0]), int(-self.directionBody[1])
            self.rect.x += heading[0]
            self.rect.y += heading[1]
        elif self.isMovingForward == False:
            heading = int(self.directionBody[0]), int(self.directionBody[1])
            self.rect.x += heading[0]
            self.rect.y += heading[1]

    def drawHead(self):
        self.screen.blit(self.imageHead, self.rectHead)

    def shoot(self):
        keys = pygame.key.get_pressed()

        checkForCooldown = self.bulletCooldownCheck.calculate(self.bulletCooldown, time())

        if checkForCooldown:
            if keys[pygame.K_SPACE]:
                Bullet((self.rect.centerx, self.rect.centery), self.group_bullet, self.angleHead, self.animation)
                self.bulletCooldownCheck.reset()


    def animate(self):
        if self.isMoving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            else:
                self.orig_image = self.frames[int(self.frame_index)]

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def update(self):
        self.rotateBody()
        self.rotateHead()
        self.move()
        self.drawHead()
        self.shoot()
        print(self.isMovingForward)

        self.outline()

        self.animate()
