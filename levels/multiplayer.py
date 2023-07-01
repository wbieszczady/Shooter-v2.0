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

class Multiplayer:
    def __init__(self):

        self.lobby = Lobby()



    def run(self):

        self.lobby.run()

