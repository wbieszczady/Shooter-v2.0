import pygame
from utilities import center_position, NavigationButton
from animation import Animation
from settings import *
from tile import Border, Box
from player import Player
from gui import Gui
from network import Client
from threading import Thread
from levels.menu import Lobby
from server2 import Server

class Multiplayer:
    def __init__(self, server = None):

        self.networkServer = server
        self.networkClient = None

        self.lobby = Lobby(self)



    def run(self):

        self.lobby.run()

    def createLobbyServer(self):
        if self.networkServer == None:
            print('Server is created.')
            self.networkServer = Server()
        else:
            print('[!] Server is already created')
            self.networkServer.shutServer()
            self.networkServer = None

    def getServer(self):
        return self.networkServer


