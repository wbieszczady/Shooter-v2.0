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
            'rocket_impact': import_folder('assets/player/particles/rocket_impact'),
            'bullet': import_folder('assets/player/projectiles/bullet'),
            'bullet_impact': import_folder('assets/player/particles/bullet_impact'),
            'trail': import_folder('assets/player/particles/trail'),
            'rocket_trail': import_folder('assets/player/particles/rocket_trail')
        }

    def animation_player_move(self, index) -> list:
        animation_frames = self.frame_list[f'move{index}']
        return animation_frames

    def animation_player_rocket(self) -> list:
        animation_frames = self.frame_list['rocket']
        return animation_frames

    def animation_player_bullet(self) -> list:
        animation_frames = self.frame_list['bullet']
        return animation_frames

    def animation_particle_trail(self) -> list:
        animation_frames = self.frame_list['trail']
        return animation_frames

    def animation_particle_bullet_impact(self) -> list:
        animation_frames = self.frame_list['bullet_impact']
        return animation_frames

    def animation_particle_rocket_impact(self) -> list:
        animation_frames = self.frame_list['rocket_impact']
        return animation_frames

    def animation_particle_rocket_trail(self) -> list:
        animation_frames = self.frame_list['rocket_trail']
        return animation_frames