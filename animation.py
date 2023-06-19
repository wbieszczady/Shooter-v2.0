import pygame
from utilities import import_folder


class Animation:
    def __init__(self):
        self.frame_list = {
            'move': import_folder('assets/player/movement'),




            'bullet': import_folder('assets/player/projectiles/bullet')
        }

    def animation_player_move(self):
        animation_frames = self.frame_list['move']
        return animation_frames

    def animation_player_bullet(self):
        animation_frames = self.frame_list['bullet']
        return animation_frames