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

def set_position(object, x, y):
    object.x, object.y = x, y
    return object.x, object.y

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

def getIPinput(keys):

    key = ''
    if keys[pygame.K_1]:
        key = '1'
    if keys[pygame.K_2]:
        key = '2'
    if keys[pygame.K_3]:
        key = '3'
    if keys[pygame.K_4]:
        key = '4'
    if keys[pygame.K_5]:
        key = '5'
    if keys[pygame.K_6]:
        key = '6'
    if keys[pygame.K_7]:
        key = '7'
    if keys[pygame.K_8]:
        key = '8'
    if keys[pygame.K_9]:
        key = '9'
    if keys[pygame.K_0]:
        key = '0'
    if keys[pygame.K_PERIOD]:
        key = '.'
    return key