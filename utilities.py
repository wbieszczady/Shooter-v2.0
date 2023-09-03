import pygame
from os import walk
from settings import *
import socket

backToMenu = pygame.USEREVENT + 1
killServer = pygame.USEREVENT + 2
clientDisconnect = pygame.USEREVENT + 3

def import_folder(path):

    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            fullpath = path + '/' + image
            image_surf = pygame.image.load(fullpath).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def NavigationButton(rect, img_normal, img_hover, nav):
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        image = img_hover
        if pygame.mouse.get_pressed()[0] == 1:

            for k, v in LEVELS.items():
                if k == nav:
                    LEVELS[k] = True
                else:
                    LEVELS[k] = False

            if nav == 'mainMenu':
                pygame.event.post(pygame.event.Event(backToMenu))

    else:
        image = img_normal

    return image

def CreateServerButton(rect, img_normal, img_hover, lobby):
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        image = img_hover
        if pygame.mouse.get_pressed()[0] == 1:


            lobby.level.createServer()
            lobby.level.clientConnect()

            lobby.stage = 2
    else:
        image = img_normal

    return image

def JoinGameButton(rect, img_normal, img_hover, lobby):
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        image = img_hover
        if pygame.mouse.get_pressed()[0] == 1:

            lobby.level.clientConnect()

            lobby.stage = 2

    else:
        image = img_normal

    return image