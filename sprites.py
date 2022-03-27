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
                'scale': (1, 0.6),
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'square': {
                'name': 'square',
                'sprite': pygame.image.load('data/sprites/npc/unfriendly/testsquare/default.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.5,
                'scale': (0.6, 0.6),
                'animation': [],
                'death_animation': deque([pygame.image.load(f'data/sprites/npc/unfriendly/testsquare/{i}.png')] for i in range(6)),
                'is_dead': None,
                'side': 40,
                'dead_shift': 0.5,
                'animation_dist': 800,
                'animation_speed': 20,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque([pygame.image.load(f'data/sprites/npc/unfriendly/testsquare/{i}.png').convert_alpha() for i in range(2)]),
                'is_acting': True,
                'health': 100
            },
            'fire': {
                'name': 'fire',
                'sprite':  pygame.image.load('data/sprites/unstatic/anim/base.png').convert_alpha(), # Всегда делать 8 текстурок, если меньше, то крашится
                'viewing_angles': False,
                'shift': 0.8,
                'scale': (1, 1),
                'animation': deque(
                     [pygame.image.load(f'data/sprites/unstatic/anim/{i}.png').convert_alpha() for i in range(12)]),
                'death_animation': deque(
                    [pygame.image.load(f'data/sprites/npc/unfriendly/testsquare/{i}.png')] for i in range(6)),
                'is_dead': 'immortal',
                'side': 30,
                'dead_shift': 0.8,
                'animation_dist': 800,
                'animation_speed': 2,
                'blocked': True,
                'flag': 'decor',
                'obj_action': deque([pygame.image.load(f'data/sprites/unstatic/anim/{i}.png').convert_alpha() for i in range(16)]),
                'is_acting': True,
                'health': None
            },
        }

        self.dict_of_objects = {
            0: [SpriteObject(self.sprite_parameters['fire'], (9, 4)),
                SpriteObject(self.sprite_parameters['square'], (7, 4)),],
            1: [SpriteObject(self.sprite_parameters['square'], (1, 1)),],
            2: [SpriteObject(self.sprite_parameters['fire'], (2, 3)),
                SpriteObject(self.sprite_parameters['square'], (5, 1)), ],
        }

        # for i in :
        #     list_of_objects.append(SpriteObject(self.sprite_parameters['sprite-barrel'],  (i[0] // 100, i[1] // 100)))
    @property
    def sprite_hit(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))



class SpriteObject:
    def __init__(self, parameters, pos):
        self.health = parameters['health']
        self.name = parameters['name']
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * tile, pos[1] * tile
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.is_acting = parameters['is_acting']
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'door_h' else self.x
        self.delete = False
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                    [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
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
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / delta_angle)
        self.current_ray = center_ray + delta_rays
        self.distance_to_sprite *= math.cos(half_fov - self.current_ray * delta_angle)

        fake_ray = self.current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and self.distance_to_sprite > 30:
            self.proj_height = min(int(proj_coof / self.distance_to_sprite * self.scale[0]), double_height)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_height = sprite_height // 2
            half_sprite_width = sprite_width // 2
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.shift

            if self.is_dead and self.is_dead != 'immortal':
                sprite_object = self.dead_anim()[0]
                shift = half_sprite_height * self.dead_shift
                sprite_height = int(sprite_height / 1.3)
            elif self.npc_action_trigger:
                sprite_object = self.npc_ai()
            else:
                self.object = self.visible()
                sprite_object = self.anim()


            #anim


            # scaling
            sprite_pos = (self.current_ray * scale - half_sprite_width, half_height - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def anim(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += double_pi
            self.theta = 360 - int(math.degrees(self.theta))
            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_position[angles]
        return self.object

    def dead_anim(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        else:
            self.delete = True
        return self.dead_sprite

    def npc_ai(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object
