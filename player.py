import pygame, math
from time import time
import time
from pygame import Vector2
from projectile import Rocket
from settings import *
from threading import Thread
import multiprocessing

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

        self.posx, self.posy = self.rect.centerx, self.rect.centery

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
        self.animation_speed = 0.1
        self.frames = self.animation.animation_player_move(index)

        #player projectiles
        self.rocketCooldown = 0.1 # [seconds]

        #listeners

        moveListener = Thread(target=self.move, daemon=True)
        moveListener.start()

        rotateListener = Thread(target=self.rotateBody, daemon=True)
        rotateListener.start()

        shootListener = Thread(target=self.shoot, daemon=True)
        shootListener.start()

        bulletHandler = Thread(target=self.handler, daemon=True)
        bulletHandler.start()

    def handler(self):

        while self.alive():

            for bullet in self.group_projectiles:
                try:
                    bullet.update()
                except:
                    pass

            time.sleep(0.01)

    def rotateHead(self):

        self.posHead = Vector2(self.rect.center)

        offs = (self.game.offset[0], self.game.offset[1])

        self.directionHead = pygame.mouse.get_pos() - self.posHead - offs
        self.radiusHead, self.angleHead = self.directionHead.as_polar()
        self.angleHead = round(self.angleHead, 0)

        # pre calculating rotation

        self.pr = self.preRotation[self.angleHead]
        self.rectHead = self.pr.get_rect(center=(self.rect.centerx, self.rect.centery))

    def rotateBody(self):

        while self.alive():

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.directionBody.rotate_ip(-1)
                time.sleep(0.005)
            elif keys[pygame.K_d]:
                self.directionBody.rotate_ip(1)
                time.sleep(0.005)
            else:
                time.sleep(0.01)


            if keys[pygame.K_d] or keys[pygame.K_a]:
                self.isRotating = True
            else:
                self.isRotating = False

            self.angleBody = round(self.directionBody.angle_to((6, 0)), 2)

    def updateBody(self):
        self.image = pygame.transform.rotate(self.orig_image, self.angleBody)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        while self.alive():
            keys = pygame.key.get_pressed()

            heading = round(self.directionBody[0], 4), round(self.directionBody[1], 4)

            if keys[pygame.K_w]:

                self.posx += heading[0]
                self.posy += heading[1]

                self.rect.centerx = self.posx
                self.rect.centery = self.posy

                self.game.offset[0] -= heading[0]
                self.game.offset[1] -= heading[1]
                # self.animate()
                time.sleep(0.0025)

            if keys[pygame.K_s]:

                self.posx -= heading[0]
                self.posy -= heading[1]

                self.rect.centerx = self.posx
                self.rect.centery = self.posy

                self.game.offset[0] += heading[0]
                self.game.offset[1] += heading[1]
                # self.animate()
                time.sleep(0.0025)


            if keys[pygame.K_w]:
                self.isMoving = True
                self.isMovingForward = True
            elif keys[pygame.K_s]:
                self.isMoving = True
                self.isMovingForward = False
            else:
                self.isMoving = False
                self.isMovingForward = None



            for tile in self.game.group_objects:
                try:
                    if pygame.sprite.collide_mask(tile, self):
                        self.bounce()
                        break
                except:
                    print(tile, self)

            time.sleep(0.010)

    def bounce(self):
        if self.isMovingForward:

            heading = round(-self.directionBody[0], 4), round(-self.directionBody[1], 4)

            self.posx += heading[0]
            self.posy += heading[1]

            self.game.offset[0] -= heading[0]
            self.game.offset[1] -= heading[1]

        elif self.isMovingForward == False:

            heading =  round(self.directionBody[0], 4),  round(self.directionBody[1], 4)

            self.posx += heading[0]
            self.posy += heading[1]

            self.game.offset[0] -= heading[0]
            self.game.offset[1] -= heading[1]

    def shoot(self):
        while self.alive():
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.createRocket()
                time.sleep(self.rocketCooldown)
            else:
                time.sleep(0.010)

    def createRocket(self):
        Rocket(self, 20)

    def animate(self):
        if self.isMoving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            else:
                self.orig_image = self.frames[int(self.frame_index)]

    def outline(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 3, border_radius=1)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rectHead, 3, border_radius=1)

    def customDraw(self):
        offset = self.game.offset

        self.screen.blit(self.image, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))
        self.screen.blit(self.pr, (self.rectHead.x + offset[0], self.rectHead.y + offset[1]))

    def update(self):
        self.updateBody()
        self.rotateHead()
        self.customDraw()