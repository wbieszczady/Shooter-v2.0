import pygame
import pygame_widgets
from utilities import NavigationButton, CreateServerButton, JoinGameButton
from utilities import *
from gui import Gui
from pygame_widgets.button import Button



class MainMenu:
    def __init__(self, game):

        #common
        self.screen = pygame.display.get_surface()
        self.game = game


        self.widgets = []

        # #singleplayer button
        # self.image_singlePlayerNormal = pygame.image.load('assets/menu/singleplayer.png').convert_alpha()
        # self.image_singlePlayerHover = pygame.image.load('assets/menu/singleplayer_hover.png').convert_alpha()
        # self.rect_singlePlayer = self.image_singlePlayerNormal.get_rect()
        # self.rect_singlePlayerPos = center_position(self.rect_singlePlayer)
        #
        # # multiplayer button
        # self.image_multiPlayerNormal = pygame.image.load('assets/menu/multiplayer.png').convert_alpha()
        # self.image_multiPlayerHover = pygame.image.load('assets/menu/multiplayer_hover.png').convert_alpha()
        # self.rect_multiPlayer = self.image_multiPlayerNormal.get_rect()
        # self.rect_multiPlayerPos = center_position(self.rect_multiPlayer, 0, 120)
        #
        # #title
        # self.image_title = pygame.image.load('assets/menu/title.png').convert_alpha()
        # self.rect_title = self.image_title.get_rect()
        # self.rect_titlePos = center_position(self.rect_title, 0, -400)

    def run(self):
        self.b1 = Button(win=self.screen, x=0, y=3, width=300, height=80,
                         onClick=lambda: self.changeLevel('singleplayer'), text='Singleplayer', fontSize=36)
        self.b2 = Button(win=self.screen, x=0, y=90, width=300, height=80,
                         onClick=lambda: self.changeLevel('multiplayer'), text='Multiplayer', fontSize=36)

        self.widgets.append(self.b1)
        self.widgets.append(self.b2)

    def changeLevel(self, lvl):
        self.game.level = lvl

        for widget in self.widgets:
            widget.hide()

        self.widgets = []



class Lobby:
    def __init__(self, level):

        #TODO create textbox for IP connection and STARTGAME button

        #common
        self.screen = pygame.display.get_surface()
        self.level = level
        self.stage = 1


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

        #player list
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 40)

        self.image_playerPH = pygame.image.load('assets/menu/clientPlaceHolder.png').convert_alpha()
        self.rect_playerPH = self.image_playerPH.get_rect()
        self.rect_playerPH_pos = [center_position(self.rect_playerPH, 0, -200),
                                  center_position(self.rect_playerPH, 0, -70),
                                  center_position(self.rect_playerPH, 0, 60),
                                  center_position(self.rect_playerPH, 0, 190)]
        #gui
        self.gui = Gui()

    def button_backToMenu(self):
        self.image_bMenuFinal = NavigationButton(self.rect_bMenu, self.image_bMenu, self.image_bMenu_hover, 'mainMenu')
        self.screen.blit(self.image_bMenuFinal, self.rect_bMenuPos)
    def button_createServer(self):
        self.image_createFinal = CreateServerButton(self.rect_create, self.image_create, self.image_create_hover, self)
        self.screen.blit(self.image_createFinal, self.rect_createPos)

    def button_joinGame(self):
        self.image_joinFinal = JoinGameButton(self.rect_join, self.image_join, self.image_join_hover, self)
        self.screen.blit(self.image_joinFinal, self.rect_joinPos)

    def playerList(self):

        for pos in self.rect_playerPH_pos:
            self.screen.blit(self.image_playerPH, pos)

        if self.level.state != None:
            self.players = self.level.state[3]

            for k in self.players.keys():
                if self.players[k] != None:
                    index = int(k)

                    text = self.font.render(str(self.players[k]), False, (255, 255, 255))
                    self.screen.blit(text, self.rect_playerPH_pos[index])


    def runGame(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            msg = '[LOBBY END]'
            self.level.game.client.send(msg)
            self.stage = 3



    def run(self):

        self.button_backToMenu()

        if self.stage == 1:
            self.button_joinGame()
            self.button_createServer()
        elif self.stage == 2:
            self.runGame()
            self.playerList()
        elif self.stage == 3:
            pass


        self.gui.showMouse()


