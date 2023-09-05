import pygame, math
from time import time
import time
from pygame import Vector2
from projectile import Bullet
from settings import *
from threading import Thread

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, index=0):
        super().__init__(game.group_players)

        #common attributes

        self.screen = pygame.display.get_surface()
        self.group_projectiles = game.group_projectiles

        self.isMoving = False
        self.isRotating = False
        self.isMovingForward = False

        self.game = game

        self.index = index

        #player body

        self.image = pygame.image.load(f'assets/player/player{index}.png').convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.directionBody = Vector2(0, -6)
        self.angleBody = 0

        #player head

        self.imageHead = pygame.image.load(f'assets/player/playerHead{index}.png').convert_alpha()
        self.orig_imageHead = self.imageHead
        self.rectHead = self.imageHead.get_rect(topleft = pos)
        self.angleHead = 0

        #precalculating rotation

        self.preRotation = {}
        for angle in range(-181, 181):
            self.imageHead = pygame.transform.rotate(self.orig_imageHead, -angle)
            self.preRotation.update({angle: self.imageHead})

        #player animations

        self.animation = game.animation_player
        self.frame_index = 0
        self.animation_speed = 0.45
        self.frames = self.animation.animation_player_move(index)

        #player projectiles
        self.bulletCooldown = 10 # [ms]

        #listener
        moveListener = Thread(target=self.move, daemon=True)
        moveListener.start()

        rotateListener = Thread(target=self.rotateBody, daemon=True)
        rotateListener.start()

        shootListener = Thread(target=self.shoot, daemon=True)
        shootListener.start()


    def rotateHead(self):

        self.posHead = Vector2(self.rect.center)

        self.directionHead = pygame.mouse.get_pos() - self.posHead
        self.radiusHead, self.angleHead = self.directionHead.as_polar()
        self.angleHead = round(self.angleHead, 0)

        # pre calculating rotation

        preRotation = self.preRotation[self.angleHead]
        self.rectHead = preRotation.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.screen.blit(preRotation, self.rectHead)


    def rotateBody(self):
        while True:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.directionBody.rotate_ip(-1)
                time.sleep(0.0025)
            if keys[pygame.K_d]:
                self.directionBody.rotate_ip(1)
                time.sleep(0.0025)

            if keys[pygame.K_d] or keys[pygame.K_a]:
                self.isRotating = True
            else:
                self.isRotating = False

            self.angleBody = round(self.directionBody.angle_to((6, 0)), 2)

            time.sleep(0.017)

    def drawBody(self):
        self.image = pygame.transform.rotate(self.orig_image, self.angleBody)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        while True:
            keys = pygame.key.get_pressed()

            heading = int(self.directionBody[0]), int(self.directionBody[1])

            if keys[pygame.K_w]:
                self.rect.x += heading[0]
                self.rect.y += heading[1]
                self.animate()
                time.sleep(0.005)

            if keys[pygame.K_s]:
                self.rect.x -= heading[0]
                self.rect.y -= heading[1]
                self.animate()
                time.sleep(0.005)

            if keys[pygame.K_w]:
                self.isMoving = True
                self.isMovingForward = True
            elif keys[pygame.K_s]:
                self.isMoving = True
                self.isMovingForward = False
            else:
                self.isMoving = False
                self.isMovingForward = None

            time.sleep(0.010)

    def bounce(self):
        if self.isMovingForward:

            heading = int(-self.directionBody[0]), int(-self.directionBody[1])
            self.rect.x += heading[0]
            self.rect.y += heading[1]
        elif self.isMovingForward == False:
            heading = int(self.directionBody[0]), int(self.directionBody[1])
            self.rect.x += heading[0]
            self.rect.y += heading[1]

    def shoot(self):
        while True:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.createBullet()
                time.sleep(0.1)

            time.sleep(0.010)

    def createBullet(self):
        Bullet((self.rect.centerx, self.rect.centery), self.group_projectiles, self.angleHead, self.animation)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.orig_image = self.frames[int(self.frame_index)]

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)

    def update(self):
        self.drawBody()
        self.rotateHead()