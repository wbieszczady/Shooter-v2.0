import pygame
from utilities import center_position, NavigationButton
from animation import Animation
from settings import *
from tile import Border, Box
from player import Player
from gui import Gui, Debug
from network import Client
from threading import Thread
from levels.menu import Lobby
from server import Server
from client import Client

class Multiplayer:
    def __init__(self, game):

        #common
        self.game = game
        self.lobby = Lobby(self)
        self.inGame = False


    def run(self):

        if self.inGame:
            self.gameMP.run()
        else:
            self.lobby.run()

    def createServer(self):
        self.killServer()
        self.game.server = Server()

    def killServer(self):
        if self.game.server != None:
            self.game.server.shutServer()
            self.game.server = None

    def clientConnect(self):
        if self.game.client == None:
            self.game.client = Client()
            try:
                index = self.game.client.connect()
                self.gameMP = MultiplayerGame(self, index[0], index[1])
                self.inGame = True
            except:
                print('No connection')
                self.game.client = None

    def killClient(self):
        if self.game.client != None:
            self.game.client.disconnect()
            self.game.client = None


class MultiplayerGame:
    def __init__(self, multiplayer, player_index, player_count):

        #common
        self.player_index = player_index
        self.player_count = player_count
        self.multiplayer = multiplayer

        self.multiplayer.game.client.run()

        # get the display surface
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load('assets/obstacles/map.png').convert_alpha()

        # create sprite groups
        self.group_objects = pygame.sprite.Group()
        self.group_players = pygame.sprite.Group()
        self.group_projectiles = pygame.sprite.Group()

        self.animation_player = Animation()

        # create map
        self.create_map()

        self.gui = Gui()
        self.debug = Debug(self.group_players)

    def create_map(self):

        count = 0

        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                if column == 'x':
                    Box((x, y), self.group_objects)
                if column == 'p':

                    player = Player((x, y), [self.group_players, self.group_projectiles], self.animation_player)
                    if int(count) != int(self.player_index):
                        player.canMove = False
                    count += 1

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

    def packageParser(self):
        player = self.group_players.sprites()[self.player_index]

        infoToSend = {'rect': player.rect,
                      'rectHead': player.rectHead,
                      'angle': player.angleBody,
                      'angleHead': player.angleHead,
                      'frame': player.frame_index
                      }

        self.multiplayer.game.client.send(infoToSend)

    def responseParser(self):
        response = self.multiplayer.game.client.response

        if response == None:
            pass
        else:
            player = self.group_players.sprites()[response[0]]
            package = response[1]

            player.rect = package['rect']
            player.rectHead = package['rectHead']
            player.angleBody = package['angle']
            player.angleHead = package['angleHead']
            player.frame_index = package['frame']

    def run(self):

        #network


        self.responseParser()
        self.packageParser()


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

        #drawing gui


        self.gui.gameMenu()
        self.gui.showMouse()


