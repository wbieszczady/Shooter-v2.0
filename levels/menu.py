import pygame
from utilities import center_position, NavigationButton, set_position, getIPinput
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
    def __init__(self):

        #common
        self.screen = pygame.display.get_surface()

        #create server button
        self.image_create = pygame.image.load('assets/menu/createLobby.png').convert_alpha()
        self.rect_create = self.image_create.get_rect()
        self.rect_createPos = center_position(self.rect_create)

        #join game button


        #back to menu button
        self.image_bMenu = pygame.image.load('assets/menu/backToMenu.png').convert_alpha()
        self.image_bMenu_hover = pygame.image.load('assets/menu/backToMenu_hover.png').convert_alpha()
        self.rect_bMenu = self.image_bMenu.get_rect()
        self.rect_bMenuPos = set_position(self.rect_bMenu, 30, 30)

        #gui
        self.gui = Gui()


    def run(self):
        self.image_bMenuFinal = NavigationButton(self.rect_bMenu, self.image_bMenu, self.image_bMenu_hover, 'mainMenu')

        self.screen.blit(self.image_create, self.rect_createPos)
        self.screen.blit(self.image_bMenuFinal, self.rect_bMenuPos)

        self.gui.showMouse()


