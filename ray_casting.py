import pygame as pg
from settings import *
import maps
from numba import njit
import numpy as np

world_map, world_width, world_height = maps.map_call()[1], maps.map_call()[2], maps.map_call()[3]


def ray_casting(player_pos, player_angle, w):
    world_map = maps.map_call()[1]
    return proj(player_pos, player_angle, world_map)


@njit(fastmath=True)
def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


@njit(fastmath=True)
def proj(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - half_fov
    for ray in range(num_rays):
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
        # proj
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % tile
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.000000001)
        proj_height = int(proj_coof / depth)
        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += delta_angle
    return casted_walls


def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.pos, player.angle, world_map)
    walls = []
    wall_hit = casted_walls[center_ray][0], casted_walls[center_ray][2]

    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > height:
            coeff = proj_height / height
            texture_height1 = texture_height / coeff
            wall_column = textures[texture].subsurface(offset * texture_scale,
                                                       half_texture_height - texture_height1 // 2,
                                                       texture_scale, texture_height1)
            wall_column = pygame.transform.scale(wall_column, (scale, height))
            wall_pos = (ray * scale, 0)
        else:
            wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
            wall_column = pygame.transform.scale(wall_column, (scale, proj_height * 2))
            wall_pos = (ray * scale, half_height - proj_height * 1.22)
        walls.append((depth, wall_column, wall_pos))
    return walls, wall_hit


def floor(posx, posy, rot, move, surf, s):
    # if move and s < 2:
    #     hres = 120  # horizontal resolution
    #     halfvres = 70  # vertical resolution/2
    #
    #     mod = hres / 60  # scaling factor (60° fov)
    #     frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
    #     sky = pg.image.load('data/textures/skybox.jpg')
    #     sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2))) / 255
    #     floor = pg.surfarray.array3d(pg.image.load('data/textures/Brick_texture.jpg')) / 255
    #
    #     frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod)
    #
    #     surf = pg.surfarray.make_surface(frame * 255)
    #     surf = pg.transform.scale(surf, (1200, 800))
    return 100000, surf, (0, 0)


def floor_settings(x, y, angle, last_x, last_y, last_angle, s, move):
    if x == last_x and y == last_y and angle == last_angle:
        move = 0
    else:
        s = s + 1 if s < 4 else 0
    return move, s


@njit()
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod):
    posy, posx = posy * 0.01, posx * 0.01
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:]
        for j in range(halfvres):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
            frame[i][halfvres * 2 - j - 1] = floor[xx][yy]

    return frame