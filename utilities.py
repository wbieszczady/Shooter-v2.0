import pygame
from os import walk
from settings import *
import socket
import time

def import_folder(path) -> list:

    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            fullpath = path + '/' + image
            image_surf = pygame.image.load(fullpath).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


class Cooldown:
    def __init__(self):
        self.bTime = time.time()

    def update(self):
        self.nTime = time.time() - self.bTime

    def clear(self):
        self.bTime = time.time()

    def get(self):
        return self.nTime