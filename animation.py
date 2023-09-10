import pygame
from utilities import import_folder


class Animation:

    #TODO import all resources to this class
    def __init__(self):
        self.frame_list = {
            'move0': import_folder('assets/player/movement0'),
            'move1': import_folder('assets/player/movement1'),
            'move2': import_folder('assets/player/movement2'),
            'move3': import_folder('assets/player/movement3'),
            'rocket': import_folder('assets/player/projectiles/rocket'),
            'bullet': import_folder('assets/player/projectiles/bullet')
        }

    def animation_player_move(self, index):
        animation_frames = self.frame_list[f'move{index}']
        return animation_frames

    def animation_player_rocket(self):
        animation_frames = self.frame_list['rocket']
        return animation_frames

    def animation_player_bullet(self):
        animation_frames = self.frame_list['bullet']
        return animation_frames