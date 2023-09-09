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