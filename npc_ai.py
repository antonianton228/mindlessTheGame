from settings import *
from maps import world_map
from ray_casting import mapping
import math
import pygame
from numba import njit

@njit(fastmath=True, cash=True)
def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    d_x, d_y = ox - npc_x, oy-npc_y
    cur_angle = math.atan2(d_y, d_x)
    sin_a = math.sin(cur_angle)
    cos_a = math.cos(cur_angle)
    # vert
    if cos_a >= 0:
        x = xm + tile
        dx = 1
    else:
        x = xm
        dx = -1
    for i in range(0, world_width, tile):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            texture_v = world_map[tile_v]
            break
        x += dx * tile
    # hor
    if sin_a >= 0:
        y = ym + tile
        dy = 1
    else:
        y = ym
        dy = -1
    for i in range(0, world_height, tile):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            texture_h = world_map[tile_h]
            break
        y += dy * tile