import threading

import pygame, time
from settings import *
from tile import *
from player import Player
from gui import Gui, Debug
from threading import Thread
from animation import Animation
from utilities import center_position, NavigationButton
import cProfile


class MainMenu:
    def __init__(self, settings):

        #common
        self.screen = pygame.display.get_surface()
        self.settings = settings

        #singleplayer button
        self.image_singlePlayerNormal = pygame.image.load('assets/menu/playButton.png').convert_alpha()
        self.image_singlePlayerHover = pygame.image.load('assets/menu/playButton_hover.png').convert_alpha()
        self.rect_singlePlayer = self.image_singlePlayerNormal.get_rect()
        self.rect_singlePlayerPos = center_position(self.rect_singlePlayer)

        #title
        self.image_title = pygame.image.load('assets/menu/title.png').convert_alpha()
        self.rect_title = self.image_title.get_rect()
        self.rect_titlePos = center_position(self.rect_title, 0, -400)

        #gui (extension)
        self.gui = Gui(settings)

    def run(self):

        self.image_singlePlayerFinal = NavigationButton(self.rect_singlePlayer, self.image_singlePlayerNormal, self.image_singlePlayerHover, self.settings, False)

        self.screen.blit(self.image_singlePlayerFinal, self.rect_singlePlayerPos)
        self.screen.blit(self.image_title, self.rect_titlePos)

        self.gui.showMouse()



class Level:
    def __init__(self, settings):

        self.settings = settings

        # get the display surface
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load('assets/obstacles/map.png').convert_alpha()

        # create sprite groups
        self.group_objects = pygame.sprite.Group()
        self.group_players = pygame.sprite.GroupSingle()

        self.animation_player = Animation()

        #create map
        self.create_map()

        self.gui = Gui(settings)
        self.debug = Debug(self.group_players)

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

        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            self.gui.gameMenu()


        #drawing debug mode

        if DEBUG:
            self.debug.debugMode()
            for player in self.group_players:
                player.outline()
            for bullet in self.group_players.sprite.group_bullet:
                bullet.outline()
