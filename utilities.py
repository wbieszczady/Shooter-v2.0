import pygame
from os import walk
from settings import *

backToMenu = pygame.USEREVENT + 1

def import_folder(path):

    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            fullpath = path + '/' + image
            image_surf = pygame.image.load(fullpath).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def center_position(object, vecX=0, vecY=0):
    object.x, object.y = WIDTH/2 - object.w/2 + vecX, HEIGHT/2 - object.h/2 + vecY
    return object.x, object.y

def NavigationButton(rect, img_normal, img_hover, isMainMenu):
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        image = img_hover
        if pygame.mouse.get_pressed()[0] == 1:
            if isMainMenu:
                LEVELS['mainMenu'] = True
                LEVELS['singleplayer'] = False
                pygame.event.post(pygame.event.Event(backToMenu))
                print('cleared')
            else:
                LEVELS['mainMenu'] = False
                LEVELS['singleplayer'] = True


    else:
        image = img_normal

    return image