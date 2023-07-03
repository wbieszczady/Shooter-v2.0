import pygame
from utilities import center_position, NavigationButton, set_position, CreateServerButton, JoinGameButton
from utilities import *
from gui import Gui



class MainMenu:
    def __init__(self):

        #common
        self.screen = pygame.display.get_surface()

        #singleplayer button
        self.image_singlePlayerNormal = pygame.image.load('assets/menu/singleplayer.png').convert_alpha()
        self.image_singlePlayerHover = pygame.image.load('assets/menu/singleplayer_hover.png').convert_alpha()
        self.rect_singlePlayer = self.image_singlePlayerNormal.get_rect()
        self.rect_singlePlayerPos = center_position(self.rect_singlePlayer)

        # multiplayer button
        self.image_multiPlayerNormal = pygame.image.load('assets/menu/multiplayer.png').convert_alpha()
        self.image_multiPlayerHover = pygame.image.load('assets/menu/multiplayer_hover.png').convert_alpha()
        self.rect_multiPlayer = self.image_multiPlayerNormal.get_rect()
        self.rect_multiPlayerPos = center_position(self.rect_multiPlayer, 0, 120)

        #title
        self.image_title = pygame.image.load('assets/menu/title.png').convert_alpha()
        self.rect_title = self.image_title.get_rect()
        self.rect_titlePos = center_position(self.rect_title, 0, -400)

        #gui (extension)
        self.gui = Gui()

    def run(self):

        self.image_singlePlayerFinal = NavigationButton(self.rect_singlePlayer, self.image_singlePlayerNormal, self.image_singlePlayerHover, 'singleplayer')
        self.image_multiPlayerFinal = NavigationButton(self.rect_multiPlayer, self.image_multiPlayerNormal, self.image_multiPlayerHover, 'multiplayer')

        self.screen.blit(self.image_singlePlayerFinal, self.rect_singlePlayerPos)
        self.screen.blit(self.image_multiPlayerFinal, self.rect_multiPlayerPos)

        self.screen.blit(self.image_title, (self.rect_titlePos[0], 0))

        self.gui.showMouse()


class Lobby:
    def __init__(self, level):

        #common
        self.screen = pygame.display.get_surface()
        self.level = level

        self.server_created = False
        self.game_joined = False


        #create server button
        self.image_create = pygame.image.load('assets/menu/createLobby.png').convert_alpha()
        self.image_create_hover = pygame.image.load('assets/menu/createLobby_hover.png').convert_alpha()
        self.rect_create = self.image_create.get_rect()
        self.rect_createPos = center_position(self.rect_create)

        #join game button
        self.image_join = pygame.image.load('assets/menu/joinGame.png').convert_alpha()
        self.image_join_hover = pygame.image.load('assets/menu/joinGame_hover.png').convert_alpha()
        self.rect_join = self.image_join.get_rect()
        self.rect_joinPos = center_position(self.rect_join, 0, -150)

        #back to menu button
        self.image_bMenu = pygame.image.load('assets/menu/backToMenu.png').convert_alpha()
        self.image_bMenu_hover = pygame.image.load('assets/menu/backToMenu_hover.png').convert_alpha()
        self.rect_bMenu = self.image_bMenu.get_rect()
        self.rect_bMenuPos = set_position(self.rect_bMenu, 30, 30)

        #gui
        self.gui = Gui()

    def button_backToMenu(self):
        self.image_bMenuFinal = NavigationButton(self.rect_bMenu, self.image_bMenu, self.image_bMenu_hover, 'mainMenu')
        self.screen.blit(self.image_bMenuFinal, self.rect_bMenuPos)
    def button_createServer(self):
        if not self.server_created:
            self.image_createFinal = CreateServerButton(self.rect_create, self.image_create, self.image_create_hover, self)
            self.screen.blit(self.image_createFinal, self.rect_createPos)

    def button_joinGame(self):
        if not self.game_joined:
            self.image_joinFinal = JoinGameButton(self.rect_join, self.image_join, self.image_join_hover, self)
            self.screen.blit(self.image_joinFinal, self.rect_joinPos)


    def run(self):

        self.button_backToMenu()

        self.button_joinGame()
        self.button_createServer()

        self.gui.gameMenu()
        self.gui.showMouse()


