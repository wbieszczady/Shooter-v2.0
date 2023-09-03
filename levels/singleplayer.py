import threading

import pygame, time
from settings import *
from tile import *
from player import Player
from gui import Gui
from threading import Thread
from animation import Animation
from utilities import NavigationButton
import cProfile

class Singleplayer:
    def __init__(self, game):

        #TODO create player-centerd camera
        self.online = False

        # get the display surface
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load('assets/obstacles/map.png').convert_alpha()

        # create sprite groups
        self.group_objects = pygame.sprite.Group()
        self.group_players = pygame.sprite.Group()

        self.group_projectiles = pygame.sprite.Group()

        self.animation_player = game.animation

        #create map
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                if column == 'x':
                    Box((x, y), self.group_objects)
                if column == 'p':
                    player = Player(self, (x, y))
                if column == 'b':
                    Border((x, y), self.group_objects)

    def collisions(self):
        if self.group_projectiles:
            for bullet in self.group_projectiles:
                for object in self.group_objects:
                    if pygame.sprite.collide_rect(bullet, object):
                        object.destroy()
                        bullet.kill()

        for player in self.group_players:
            for object in self.group_objects:
                if pygame.sprite.collide_mask(object, player):
                    player.bounce()
                    break

    def run(self):

        #drawing background

        self.screen.blit(self.background, (0, 0))

        #drawing sprites

        self.group_objects.draw(self.screen)
        self.group_objects.update()

        self.group_projectiles.draw(self.screen)
        self.group_projectiles.update()

        self.group_players.draw(self.screen)
        self.group_players.update()

        #check for collisions

        self.collisions()

