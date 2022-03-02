import pygame
from settings import *


class Sprites:
    def __init__(self):
        self.srite_types = {
            'barrel': pygame.image.load('data/sprites/barrel.png').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel', True, (7.1, 2.1), 1.8, 0.4]),
            SpriteObject(self.sprite_types['barrel', True, (5.1, 2.1), 1.8, 0.4])
        ]

class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * tile, pos[1] * tile
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        pass