import pygame
from utilities import center_position, NavigationButton
from utilities import *
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

        #setup
        self.game = game
        self.lobby = Lobby(self)
        self.inGame = False

        self.serverAvailable = True

        self.state = None

    def gameInit(self):

        self.multiplayer = MultiplayerGame(self, self.state[1], self.state[2])
        self.inGame = True


    def run(self):

        if self.inGame:

            self.multiplayer.run()

        else:
            self.lobby.run()

    def createServer(self):
        self.killServer()
        self.game.server = Server()

        if self.game.server.bind():
            self.serverAvailable = True

        else:
            self.serverAvailable = False

    def updateState(self):
        self.state = self.game.client.state

    def clientConnect(self):

        if self.game.client == None and self.serverAvailable:
            self.game.client = Client(self)
            if self.game.client.connect():
                self.game.client.run()
                self.game.client.sendNickname()
            else:
                self.game.client = None
        else:
            print('[SERVER] Server already exist')
            pygame.event.post(pygame.event.Event(killServer))
            pygame.event.post(pygame.event.Event(backToMenu))


    def killServer(self):
        if self.game.server != None:
            self.game.server.shutServer()
            self.game.server = None

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

        # get the display surface
        self.screen = pygame.display.get_surface()
        self.background = pygame.image.load('assets/obstacles/map.png').convert_alpha()

        # create sprite groups
        self.group_objects = pygame.sprite.Group()
        self.group_players = pygame.sprite.Group()
        self.group_projectiles = pygame.sprite.Group()

        self.animation_player = multiplayer.game.animation

        # create map
        self.create_map()

        self.gui = Gui()
        self.debug = Debug(self.group_players)


    def create_map(self):
        index = 0

        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE

                if column == 'x':
                    Box((x, y), self.group_objects)
                if column == 'p':

                    if self.player_count > 0:
                        player = Player((x, y), [self.group_players, self.group_projectiles], self.animation_player, index)
                        self.player_count -= 1
                        index += 1
                        player.canMove = False

                if column == 'b':
                    Border((x, y), self.group_objects)

        self.group_players.sprites()[self.player_index].canMove = True

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

        #TODO send player positions 60 times per sec, not 60 * [number of players]

        infoToSend = {'index': self.player_index,
                      'rect': player.rect,
                      'rectHead': player.rectHead,
                      'angle': player.angleBody,
                      'angleHead': player.angleHead,
                      'frame': player.frame_index
                      }

        data_package = ['[GAME DATA]', infoToSend]
        self.multiplayer.game.client.send(data_package)

    def responseParser(self):

        response = self.multiplayer.game.client.response

        if response == None:
            pass

        else:

            for k, v in enumerate(response.items()):
                if v[1] != None:
                    package = v[1]
                    player = self.group_players.sprites()[int(k)]

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


