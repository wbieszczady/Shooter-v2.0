import pygame, time
from settings import *
from tile import *
from player import Player
from threading import Thread
from animation import Animation
import multiprocessing

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

        self.offset = [0, 0]

        # create map
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                if column == 'x':
                    Box(self, (x, y))
                if column == 'p':
                    Player(self, (x, y))
                if column == 'b':
                    Border(self, (x, y))

    def clear(self):
        for player in self.group_players:
            player.kill()

    def run(self):

        # drawing background

        self.screen.blit(self.background, self.offset)

        # drawing sprites

        try:
            for projectile in self.group_projectiles:
                projectile.customDraw()
        except:
            pass

        self.group_players.update()
        self.group_objects.update()

        # collisions

        self.collision()

    def collision(self):

        #TODO something with this collisions is not right

        for bullet in self.group_projectiles:
            for object in self.group_objects:
                try:
                    if pygame.sprite.collide_rect(bullet, object):
                        bullet.kill()
                        object.destroy()
                        break
                        break

                except Exception as ex:
                    print(ex, bullet, object)
