from settings import *
import maps
from ray_casting import mapping
import math
import pygame
from numba import njit
import settings
import drawingclass

world_map = maps.map_call()[1]


@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    d_x, d_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(d_y, d_x) + math.pi

    sin_a = math.sin(cur_angle)
    cos_a = math.cos(cur_angle)
    # vert
    if cos_a >= 0:
        x = xm + tile
        dx = 1
    else:
        x = xm
        dx = -1
    for i in range(0, int(abs(d_x)) // tile):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * tile
    # hor
    if sin_a >= 0:
        y = ym + tile
        dy = 1
    else:
        y = ym
        dy = -1
    for i in range(0, int(abs(d_y)) // tile):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * tile
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing

    def intersection_object(self):
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda x: x.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                            obj.health -= storyteller.weapon_damage
                            print(obj.health)
                            if obj.health <= 0:
                                obj.is_dead = True
                                obj.blocked = None
                            self.drawing.shot_animation_trigger = False
                            break
                    break

    def acting_object(self):
        if self.player.action:
            for obj in sorted(self.sprites.list_of_objects, key=lambda x: x.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_acting:
                        if ray_casting_npc_player(obj.x, obj.y, world_map, self.player.pos):
                            storyteller.dialog_person = obj.name
                            self.player.action = False
                            settings.dialog_draw = True

    def npc_action(self):
        for i in self.sprites.list_of_objects:
            if i.flag == 'npc' and not i.is_dead:
                if ray_casting_npc_player(i.x, i.y, world_map, self.player.pos):
                    i.npc_action_trigger = True
                    self.npc_moving(i)
                else:
                    i.npc_action_trigger = False

    def npc_moving(self, obj):
        if obj.distance_to_sprite > tile:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def clear_objects(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    def play_music(self):
        pass
        # pygame.mixer.pre_init(44100, -16, 2, 2048)
        # pygame.mixer.init()
        # pygame.mixer.music.load('data/sounds/test_music/VasyaSong.mp3')
        # pygame.mixer.music.set_volume(0.07)
        # pygame.mixer.music.play(10)


