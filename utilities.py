import pygame
from os import walk
from settings import *


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

def NavigationButton(rect, img_normal, img_hover, settings, isMainMenu):
    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        image = img_hover
        if pygame.mouse.get_pressed()[0] == 1:
            settings.set_MAIN_MENU(isMainMenu)
    else:
        image = img_normal

    return image