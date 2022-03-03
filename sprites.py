import pygame
from settings import *


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pygame.image.load('data/sprites/static/barrel.png').convert_alpha(),
            'kid': pygame.image.load('data/sprites/static/kid.png').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['barrel'], True, (5.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['kid'], True, (7, 4), 0, 1),
        ]

class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * tile, pos[1] * tile
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = (dx ** 2 + dy ** 2) ** 0.5

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        current_ray = center_ray + delta_rays
        distance_to_sprite *= math.cos(half_fov - current_ray * delta_angle)


        if 0 <= current_ray <= num_rays -1 and distance_to_sprite < walls[current_ray][0]:
            proj_height = int(proj_coof / distance_to_sprite * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            sprite_pos = (current_ray * scale - half_proj_height, half_height - half_proj_height + shift)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)