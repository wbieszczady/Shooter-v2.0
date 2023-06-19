import threading

import pygame, time
from settings import *
from tile import *
from player import Player
from gui import Gui, Debug
from threading import Thread
from animation import Animation
import cProfile


class MainMenu:
    def __init__(self, settings):

        self.screen = pygame.display.get_surface()
        self.imageNormal = pygame.image.load('assets/menu/playButton.png').convert_alpha()
        self.imageHover = pygame.image.load('assets/menu/playButton_hover.png').convert_alpha()
        self.rect = self.imageNormal.get_rect()

        self.settings = settings

        self.rect.x = 500
        self.rect.y = 500

        self.isClicked = False

        self.gui = Gui()

    def run(self):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.image = self.imageHover
            if pygame.mouse.get_pressed()[0] == 1 and self.isClicked == False:
                self.isClicked = True
                self.settings.set_MAIN_MENU(False)
            else:
                self.isClicked = False
        else:
            self.image = self.imageNormal

        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        self.gui.showMouse()



class Level:
    def __init__(self):

        # get the display surface
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load('assets/obstacles/map.png').convert_alpha()

        # create sprite groups
        self.group_objects = pygame.sprite.Group()
        self.group_players = pygame.sprite.GroupSingle()

        self.animation_player = Animation()

        #create map
        self.create_map()
        self.gui = Gui()
        self.debug = Debug()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                if column == 'x':
                    Box((x, y), self.group_objects)
                if column == 'p':
                    Player((x, y), self.group_players, self.animation_player)
                if column == 'b':
                    Border((x, y), self.group_objects)


    def run(self):

        #drawing background

        self.screen.blit(self.background, (0, 0))

        #drawing sprites

        self.group_objects.draw(self.screen)
        self.group_objects.update()

        self.group_players.sprite.group_bullet.draw(self.screen)
        self.group_players.sprite.group_bullet.update()

        self.group_players.draw(self.screen)
        self.group_players.update()

        #check for collisions

        if self.group_players.sprite.group_bullet:
            for bullet in self.group_players.sprite.group_bullet:
                for object in self.group_objects:
                    if pygame.sprite.collide_rect(bullet, object):
                        object.destroy()
                        bullet.kill()

        for player in self.group_players:
            for object in self.group_objects:
                if pygame.sprite.collide_mask(object, player):
                    player.bounce()
                    object.outline()
                    break

        #drawing gui

        self.gui.showMouse()

        if DEBUG:
            self.debug.debugMode()
            for player in self.group_players:
                player.outline()
            for bullet in self.group_players.sprite.group_bullet:
                bullet.outline()
