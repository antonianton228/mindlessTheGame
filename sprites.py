import pygame
from settings import *
from collections import deque
from ray_casting import ray_casting



class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite-barrel':{
                'sprite': pygame.image.load('data/sprites/static/barrel.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.5,
                'scale': (1.2, 1.2),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'fire': {
                'sprite': pygame.image.load('data/sprites/unstatic/anim/base.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'animation': deque(
                    [pygame.image.load(f'data/sprites/unstatic/anim/{i}.png').convert_alpha() for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'elf': {
                'sprite': [pygame.image.load(f'data/sprites/unstatic/vert/elf/{i}.png').convert_alpha() for i in range(1, 6)],
                'viewing_angles': True,
                'shift': 1.8,
                'scale': (0.4, 0.4),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'floor': {
                'sprite': pygame.image.load('data/textures/grass.jpg').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.8,
                'scale': (1, 1),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'square': {
                'sprite': pygame.image.load('data/sprites/npc/unfriendly/testsquare/default.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.5,
                'scale': (0.4, 0.4),
                'animation': [],
                'death_animation': deque([pygame.image.load(f'data/sprites/npc/unfriendly/testsquare/{i}.png')] for i in range(6)),
                'is_death': None,
                'dead_shift': 0.5
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite-barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['sprite-barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['fire'], (9, 4)),
            SpriteObject(self.sprite_parameters['square'],  (7, 4)),


        ]
        # for i in :
        #     list_of_objects.append(SpriteObject(self.sprite_parameters['sprite-barrel'],  (i[0] // 100, i[1] // 100)))
    @property
    def sprite_hit(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))



class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.blocked = parameters['blocked']
        self.side = 30
        self.x, self.y = pos[0] * tile, pos[1] * tile
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 72)) for i in range(0, 360, 72)]
            self.sprite_position = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}




    @property
    def is_on_fire(self):
        if center_ray - self.side // 2 < self.current_ray < center_ray + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None
    @property
    def pos(self):
        return self.x - self.side // 2 , self.y - self.side // 2




    def object_locate(self, player):


        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = (dx ** 2 + dy ** 2) ** 0.5

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += double_pi

        delta_rays = int(gamma / delta_angle)
        self.current_ray = center_ray + delta_rays
        self.distance_to_sprite *= math.cos(half_fov - self.current_ray * delta_angle)

        fake_ray = self.current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(proj_coof / self.distance_to_sprite * self.scale), double_height)
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.shift

            if self.viewing_angles:
                if self.theta < 0:
                    self.theta += double_pi
                self.theta = 360 - int(math.degrees(self.theta))
                for angles in self.sprite_angles:
                    if self.theta in angles:
                        self.object = self.sprite_position[angles]
                        break
            #anim
            sprite_object = self.object
            if self.animation and self.distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            sprite_pos = (self.current_ray * scale - half_proj_height, half_height - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (self.proj_height, self.proj_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)