import pygame, math
from time import time
import time
from pygame import Vector2
from projectile import Rocket, Bullet
from settings import *
from threading import Thread
from utilities import Cooldown
import multiprocessing
import ctypes
import keyboard

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, index=3):
        super().__init__(game.group_players)

        #common attributes

        self.screen = pygame.display.get_surface()

        self.group_projectiles = game.group_projectiles
        self.group_particles = game.group_particles

        self.isColliding = False
        self.isMovingForward = False

        self.game = game

        self.index = index

        #player body

        self.image = pygame.image.load(f'assets/player/player{index}.png').convert_alpha()
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.directionBody = Vector2(0, -6)
        self.angleBody = 90

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
        self.animation_speed = 0.3
        self.frames = self.animation.animation_player_move(index)

        #listeners

        self.input = Input()

    def rotateHead(self):

        self.posHead = Vector2(self.rect.center)

        offs = (self.game.offset[0], self.game.offset[1])

        self.directionHead = pygame.mouse.get_pos() - self.posHead - offs
        self.radiusHead, self.angleHead = self.directionHead.as_polar()
        self.angleHead = round(self.angleHead, 0)

        # pre calculating rotation

        self.pr = self.preRotation[self.angleHead]
        self.rectHead = self.pr.get_rect(center=(self.rect.centerx, self.rect.centery))

    def rotateBody(self, direction):

        if not self.isColliding:

            if direction == 'left':
                self.directionBody.rotate_ip(-2)

            if direction == 'right':
                self.directionBody.rotate_ip(2)

            self.angleBody = round(self.directionBody.angle_to((6, 0)), 2)

    def moveForward(self):

        self.canMove()

        self.isMovingForward = True

        heading = round(self.directionBody[0], 4), round(self.directionBody[1], 4)

        self.posx += heading[0]
        self.posy += heading[1]

        self.rect.centerx = self.posx
        self.rect.centery = self.posy

        self.game.offset[0] -= heading[0]
        self.game.offset[1] -= heading[1]

        self.animate()


    def moveBackward(self):

        self.canMove()

        self.isMovingForward = False

        heading = round(self.directionBody[0], 4), round(self.directionBody[1], 4)

        self.posx -= heading[0]
        self.posy -= heading[1]

        self.rect.centerx = self.posx
        self.rect.centery = self.posy

        self.game.offset[0] += heading[0]
        self.game.offset[1] += heading[1]

        self.animate()

    def canMove(self):

        for tile in self.game.group_objects:
            try:
                if pygame.sprite.collide_mask(tile, self):
                    self.isColliding = True
                    self.bounce()
                    break
                else:
                    self.isColliding = False
            except:
                print(tile, self)


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

    def shootBullet(self):
        Bullet(self, 30)

    def shootRocket(self):
        Rocket(self, 10)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.orig_image = self.frames[int(self.frame_index)]

    def customDraw(self):

        self.image = pygame.transform.rotate(self.orig_image, self.angleBody)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        offset = self.game.offset

        self.screen.blit(self.image, (self.rect.topleft[0] + offset[0], self.rect.topleft[1] + offset[1]))
        self.screen.blit(self.pr, (self.rectHead.x + offset[0], self.rectHead.y + offset[1]))

    def inputMovement(self):

        if self.input.forward.value:
            for _ in range(self.input.forward.value):
                self.moveForward()
            self.input.forward.value = 0

        if self.input.backward.value:
            for _ in range(self.input.backward.value):
                self.moveBackward()
            self.input.backward.value = 0

    def inputRotate(self):
        if self.input.rotateLeft.value:
            for _ in range(self.input.rotateLeft.value):
                self.rotateBody('left')
            self.input.rotateLeft.value = 0

        if self.input.rotateRight.value:
            for _ in range(self.input.rotateRight.value):
                self.rotateBody('right')
            self.input.rotateRight.value = 0

    def inputShoot(self):
        if self.input.shootE.value:

            for _ in range(self.input.shootE.value):
                self.shootBullet()
            self.input.shootE.value = 0

        if self.input.shootSPACE.value:

            for _ in range(self.input.shootSPACE.value):
                self.shootRocket()
            self.input.shootSPACE.value = 0



    def inputHandler(self):
        self.inputMovement()
        self.inputRotate()
        self.inputShoot()

        # objects update handler

        if not self.input.update.value == 0:

            for _ in range(self.input.update.value):
                self.objectHandler()
            self.input.update.value = 0

    def objectHandler(self):
        self.game.update()

    def update(self):
        self.inputHandler()
        self.rotateHead()
        self.customDraw()


class Input:

    def __init__(self):

        self.alive = multiprocessing.Value('i', 1)

        self.forward = multiprocessing.Value('i', 0)
        self.backward = multiprocessing.Value('i', 0)

        self.rotateLeft = multiprocessing.Value('i', 0)
        self.rotateRight = multiprocessing.Value('i', 0)

        self.shootE = multiprocessing.Value('i', 0)
        self.shootSPACE = multiprocessing.Value('i', 0)

        self.update = multiprocessing.Value('i', 0)

        self.movementProcess = multiprocessing.Process(target=self.general, args=(self.alive, self.forward, self.backward, self.rotateLeft, self.rotateRight, self.shootE, self.shootSPACE, self.update))
        self.movementProcess.start()

    def general(self, alive, forward, backward, rotateL, rotateR, shootE, shootSPACE, update):

        self.cooldown1 = Cooldown()
        self.cooldown2 = Cooldown()

        self.cd1 = 2
        self.cd2 = 0.1

        while alive.value == 1:

            self.bTime = time.time()

            self.cooldown1.update()
            self.cooldown2.update()

            if keyboard.is_pressed('w'):
                forward.value += 1

            if keyboard.is_pressed('s'):
                backward.value += 1

            if keyboard.is_pressed('a'):
                rotateL.value += 1

            if keyboard.is_pressed('d'):
                rotateR.value += 1

            if keyboard.is_pressed('e') and self.cooldown2.get() > self.cd2:
                shootE.value += 1
                self.cooldown2.clear()

            if keyboard.is_pressed('space') and self.cooldown1.get() > self.cd1:
                shootSPACE.value += 1
                self.cooldown1.clear()

            update.value += 1

            time.sleep(0.01)